#!/bin/sh

# for local development fill in your user name and load
# your datapunt ssh key in the docker-compose.

set -e
set -u
set -x

DIR="$(dirname $0)"

dc() {
	docker-compose $*
}

# load BGT objects of everything on the ground.
dc exec -T database update-table.sh basiskaart BGT_OWGL_verkeerseiland bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_OWGL_berm bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_OTRN_open_verharding bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_OTRN_transitie bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_WGL_fietspad bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_WGL_voetgangersgebied bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_WGL_voetpad bgt afvalcontainers spreeker

dc exec -T database update-table.sh basiskaart BGT_WGL_parkeervlak bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_WGL_rijbaan_lokale_weg bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_WGL_rijbaan_regionale_weg bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_WGL_woonerf bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_BTRN_groenvoorziening bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_OTRN_onverhard bgt afvalcontainers spreeker
dc exec -T database update-table.sh basiskaart BGT_OTRN_erf bgt afvalcontainers spreeker
