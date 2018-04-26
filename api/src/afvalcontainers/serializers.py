# import json
# import logging

from rest_framework import serializers

from datapunt_api.rest import DisplayField
from datapunt_api.rest import HALSerializer
from datapunt_api.rest import RelatedSummaryField
from afvalcontainers.models import Container
from afvalcontainers.models import Well
from afvalcontainers.models import ContainerType


class WellSerializer(HALSerializer):
    _display = DisplayField()

    containers = RelatedSummaryField()

    class Meta(object):
        model = Well
        fields = [
            "_links",
            "_display",
            "id",
            "id_number",
            "serial_number",
            "buurt_code",
            "stadsdeel",
            "geometrie",
            "created_at",
            "warranty_date",
            "operational_date",
            "containers",
            "address",
        ]


class ContainerTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContainerType
        fields = '__all__'


class ContainerSerializer(HALSerializer):
    _display = DisplayField()

    container_type = ContainerTypeSerializer()

    # well = WellSerializer()

    class Meta(object):
        model = Container
        fields = [
            "_links",
            "_display",
            "id",
            "id_number",
            "owner",
            "active",
            "waste_type",
            "waste_name",
            "container_type",
            "warranty_date",
            "operational_date",
            "placing_date",
            "well",
        ]


class TypeSerializer(HALSerializer):
    _display = DisplayField()

    class Meta(object):
        model = ContainerType
        fields = ["_links", "_display", "id", "name", "volume"]
