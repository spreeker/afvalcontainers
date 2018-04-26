"""
Copy raw data into django api models
"""

import random
import argparse
import models
import logging
from sqlalchemy.sql import select
from sqlalchemy import bindparam

log = logging.getLogger(__name__)


INSERT_WELLS = """
INSERT INTO afvalcontainers_well (
    id,
    serial_number,
    id_number,
    owner,
    containers_bron,
    created_at,
    warranty_date,
    operational_date,
    placing_date,
    active,
    geometrie,
    address
)
SELECT
    id,
    data->>'serial_number' as serial_number,
    data->>'id_number' as id_number,
    CAST(data->>'owner' as jsonb) as owner,
    CAST(data->>'containers' as jsonb) as containers_bron,
    CAST(data->>'created_at' as timestamp) as created_at,
    CAST(data->>'warranty_date' as timestamp) as warranty_date,
    CAST(data->>'operational_date' as timestamp) as operational_date,
    CAST(data->>'placing_date' as timestamp) as placing_date,
    CAST(data->>'active' as bool) as active,
    ST_SetSRID(
        ST_POINT(
            CAST(data->'location'->'position'->>'longitude' as float),
            CAST(data->'location'->'position'->>'latitude' as float)
        ), 4326) as geometrie,
    CAST(data->'location'->>'address' as jsonb) as address
    FROM bammens_well_raw;
"""  # noqa


INSERT_CONTAINERS = """
INSERT INTO afvalcontainers_container (
    id,
    id_number,
    serial_number,
    owner,
    created_at,
    warranty_date,
    operational_date,
    placing_date,
    active,
    waste_type,
    waste_name,
    container_type_id
)
SELECT
    id,
    data->>'id_number' as id_number,
    data->>'serial_number' as serial_number,
    CAST(data->>'owner' as jsonb) as owner,
    CAST(data->>'created_at' as timestamp) as created_at,
    CAST(data->>'warranty_date' as timestamp) as warranty_date,
    CAST(data->>'operational_date' as timestamp) as operational_date,
    CAST(data->>'placing_date' as timestamp) as placing_date,
    CAST(data->>'active' as bool) as active,
    CAST(data->>'waste_type' as int) as waste_type,
    data->>'waste_name' as waste_name,
    CAST(data->>'container_type' as int) as waste_type
    FROM bammens_container_raw;
"""  # noqa


INSERT_TYPES = """
INSERT INTO afvalcontainers_containertype
SELECT id, data->>'name', CAST("data"->>'volume' as INT)
FROM bammens_containertype_raw
"""

CREATE_CONTAINER_VIEW = """
CREATE OR REPLACE VIEW container_locations AS
SELECT
    c.id,
    c.id_number,
    c.serial_number,
    c.active,
    c.operational_date,
    c.placing_date,
    c.owner,
    c.waste_type,
    c.waste_name,
    c.container_type_id,
    w.stadsdeel,
    w.buurt_code,
    w.geometrie,
    CAST(w.address->>'summary' as text)
FROM afvalcontainers_container c, afvalcontainers_well w
WHERE c.well_id = w.id
"""

WASTE_DESCRIPTIONS = {
    1:  "Rest",
    2:  "Glas",
    3:  "Glas",
    6:  "Papier",
    5:  "Wat is dit?",
    7:  "Textiel",
    9:  "Wormen",
    14: "We weten het niet",
    17: "geen idee",
    20: "Glas",
    25: "Plastic",
    31: "Blipvert",
    -1: "Unkown",
    None: "Unknown",
}


def update_types():
    sql = INSERT_TYPES
    # session.execute("TRUNCATE TABLE afvalcontainers_containertype")
    session.execute(sql)
    session.commit()


def update_containers():
    sql = INSERT_CONTAINERS
    # session.execute("TRUNCATE TABLE afvalcontainers_container;")
    session.execute(sql)
    session.commit()


def update_wells():
    insert = INSERT_WELLS
    # session.execute("TRUNCATE TABLE afvalcontainers_well")
    session.execute(insert)
    session.commit()


def create_container_view():
    create_view = CREATE_CONTAINER_VIEW
    session.execute(create_view)
    session.commit()


def validate_timestamps(item):
    """We recieve invalid timestamps
    so we clean them up here.
    """
    timestamp_keys = (
        "created_at",
        "placing_date",
        "warranty_date",
        "operational_date")

    for key in timestamp_keys:
        date = item.get(key)
        if not date:
            continue

        invalid = False
        # d2 = dateparser.parse(date)
        # d = parser.parse(date)
        if date.startswith('000'):
            invalid = True
        elif date.startswith('-0'):
            invalid = True
        elif date.startswith('-10'):
            invalid = True
        if invalid:
            log.error("Invalid %s %s %s", key, date, item["id"])
            item[key] = None

    return item


def cleanup_dates(endpoint):
    """
    If some bad dates slipped into the
    json. We can clean it up.
    """
    conn = engine.connect()
    dbitem = models.ENDPOINT_MODEL[endpoint]

    s = select([dbitem])
    results = conn.execute(s)
    cleaned = []
    for row in results:
        data = validate_timestamps(row[2])
        new = {'id': row[0], 'scraped_at': row[1], 'data': data}
        cleaned.append(new)

    upd_stmt = (
        dbitem.__table__.update()
        .where(dbitem.id == bindparam('id'))
        .values(id=bindparam('id'))
    )
    conn.execute(upd_stmt, cleaned)


def add_waste_name_to_data(data):
    """Try to determine what kind of waste goes into container
    """
    waste_name = WASTE_DESCRIPTIONS[data.get('waste_type', -1)]
    data['waste_name'] = waste_name
    return data


def add_waste_name():
    conn = engine.connect()
    dbitem = models.ENDPOINT_MODEL['containers']

    s = select([dbitem])
    results = conn.execute(s)
    cleaned = []
    for row in results:
        data = add_waste_name_to_data(row[2])
        new = {'id': row[0], 'scraped_at': row[1], 'data': data}
        cleaned.append(new)

    upd_stmt = (
        dbitem.__table__.update()
        .where(dbitem.id == bindparam('id'))
        .values(id=bindparam('id'))
    )
    conn.execute(upd_stmt, cleaned)


LINK_SQL = """
UPDATE afvalcontainers_container bc
SET well_id = wlist.id
FROM (
    SELECT ww.id, ww.cid::int from  (
        SELECT w.id, jsonb_array_elements_text(w.containers_bron) AS cid
        FROM afvalcontainers_well w) as  ww) as wlist
WHERE wlist.cid = bc.id
"""

UPDATE_BUURT = """
UPDATE {target_table} tt
SET buurt_code = b.vollcode
FROM (SELECT * from buurt_simple) as b
WHERE ST_DWithin(b.wkb_geometry, tt.geometrie, 0)
"""

UPDATE_STADSDEEL = """
UPDATE {target_table} tt
SET stadsdeel = s.code
FROM (SELECT * from stadsdeel) as s
WHERE ST_DWithin(s.wkb_geometry, tt.geometrie, 0)
"""


def link_containers_to_wells():
    sql = LINK_SQL
    session.execute(sql)
    session.commit()


def link_gebieden():
    sql = UPDATE_BUURT
    target_table = 'afvalcontainers_well'
    u_sql = UPDATE_STADSDEEL.format(target_table=target_table)
    session.execute(u_sql)
    session.commit()

    target_table = 'afvalcontainers_well'
    u_sql = UPDATE_BUURT.format(target_table=target_table)
    session.execute(u_sql)
    session.commit()


OPTIONS = {
    "container_types": update_types,
    "containers": update_containers,
    "wells": update_wells,
}

TABLE_COUNTS = [
    ('afvalcontainers_well', 12000),
    ('afvalcontainers_container', 12000),
    ('afvalcontainers_containertype', 200),
    ('container_locations', 12000),
]


def validate_counts():
    """
    """
    failed = False

    for tablename, target_count in TABLE_COUNTS:
        sql = f"select count(*) from {tablename}"
        data = session.execute(sql).fetchall()

        table_count = data[0][0]
        if table_count < target_count:
            failed = True
            log.error('\n\n\n FAILED Count %s %d is not > %d \n\n',
                      tablename, table_count, target_count)
        else:
            log.info('Count OK %s %d > %d',
                     tablename, table_count, target_count)

    if failed:
        raise ValueError('Table counts not at target!')


def main():
    if args.link_gebieden:
        link_gebieden()
        return
    if args.validate:
        validate_counts()
        return
    if args.geoview:
        create_container_view()
        return
    if args.wastename:
        add_waste_name()
        return
    if args.link_containers:
        link_containers_to_wells()
        return
    if args.cleanup:
        if args.endpoint:
            endpoint = args.endpoint[0]
            cleanup_dates(endpoint)
        else:
            for endpoint in OPTIONS.items():
                cleanup_dates(endpoint)
        return

    if args.endpoint:
        endpoint = args.endpoint[0]
        OPTIONS[endpoint]()
    else:
        for func in OPTIONS.items():
            func()


if __name__ == "__main__":
    desc = "Copy data into django."
    inputparser = argparse.ArgumentParser(desc)

    inputparser.add_argument(
        "endpoint",
        type=str,
        default="",
        choices=list(OPTIONS.keys()),
        help="Provide Endpoint to scrape",
        nargs=1,
    )

    inputparser.add_argument(
        "--link_gebieden", action="store_true",
        default=False, help="Voeg stadsdeel / buurt to aan datasets"
    )

    inputparser.add_argument(
        "--validate", action="store_true",
        default=False, help="Validate counts to check import was OK"
    )

    inputparser.add_argument(
        "--geoview", action="store_true",
        default=False, help="Geoview containers"
    )

    inputparser.add_argument(
        "--cleanup", action="store_true",
        default=False, help="Cleanup"
    )

    inputparser.add_argument(
        "--wastename", action="store_true",
        default=False, help="Add waste name to containers"
    )

    inputparser.add_argument(
        "--link_containers", action="store_true",
        default=False, help="Cleanup"
    )

    args = inputparser.parse_args()

    engine = models.make_engine()
    session = models.set_session(engine)

    main()

    session.close()
