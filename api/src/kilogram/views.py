"""View Kilogram measurement data.

This data and models are in their own Kilogram database!!
"""


from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.geos import Polygon
from rest_framework.serializers import ValidationError
from django.conf import settings

# Create your views here.

from datapunt_api.rest import DatapuntViewSet
from datapunt_api import bbox
from datapunt_api.pagination import HALPagination

from kilogram.models import KilogramWeighMeasurement
from kilogram.serializers import KilogramSerializer
from kilogram.serializers import KilogramDetailSerializer

from kilogram.models import SiteFractieStatWeek
from kilogram.models import SiteFractieStatMonth
from kilogram.models import BuurtFractieStatMonth
from kilogram.models import BuurtFractieStatWeek

from kilogram.serializers import SiteFractieStatWeekSerializer
from kilogram.serializers import SiteFractieStatMonthSerializer
from kilogram.serializers import BuurtFractieStatWeekSerializer
from kilogram.serializers import BuurtFractieStatMonthSerializer


class KiloPager(HALPagination):
    """Site objects are rather "heavy" so put limits on pagination."""

    page_size = 100
    max_page_size = 9000

#

# def buurt_choices():
#     options = Buurten.objects.values_list('vollcode', 'naam')
#     return [(c, '%s (%s)' % (n, c)) for c, n in options]


class KilogramFilter(FilterSet):
    id = filters.CharFilter()
    in_bbox = filters.CharFilter(method='in_bbox_filter', label='bbox')
    detailed = filters.BooleanFilter(method='detailed_filter', label='detailed view')

    weigh_at_gt = filters.DateTimeFilter('weigh_at', lookup_expr='gt')
    weigh_at_lt = filters.DateTimeFilter('weigh_at', lookup_expr='lt')

    location = filters.CharFilter(
        method="locatie_filter", label='x,y,r')

    fractie = filters.ChoiceFilter(
        choices=settings.WASTE_CHOICES, label='waste name')

    # stadsdeel = filters.ChoiceFilter(choices=STADSDELEN)
    # buurt_code = filters.ChoiceFilter(choices=buurt_choices)

    class Meta(object):
        model = KilogramWeighMeasurement
        fields = (
            "id",
            "seq_id",
            "fractie",
            "weigh_at",
            "weigh_at_gt",
            "weigh_at_lt",
            "stadsdeel",
            "buurt_code",
            "site_id",
            "first_weight",
            "second_weight",
            "net_weight",
            "in_bbox",
            "location",
            "detailed",
            "valid",
        )

    def in_bbox_filter(self, qs, name, value):
        bbox_values, err = bbox.valid_bbox(value)
        lat1, lon1, lat2, lon2 = bbox_values
        poly_bbox = Polygon.from_bbox((lon1, lat1, lon2, lat2))

        if err:
            raise ValidationError(f"bbox invalid {err}:{bbox_values}")
        return qs.filter(geometrie__bboverlaps=(poly_bbox))

    def locatie_filter(self, qs, name, value):
        point, radius = bbox.parse_xyr(value)
        return qs.filter(
            well__geometrie__dwithin=(point, radius))

    def detailed_filter(self, qs, name, valie):
        return qs


class KilogramView(DatapuntViewSet):
    """View of container weigh measurements.

    source: kilogram.nl

    extract all examples measurements:

    https://api.data.amsterdam.nl/afval/kilogram/?page_size=100

    parameter ?detailed=1  Will give you geometry and extra information

    """

    serializer_class = KilogramSerializer
    serializer_detail_class = KilogramDetailSerializer
    bbox_filter_field = 'geometrie'
    filter_backends = (DjangoFilterBackend,)
    filter_class = KilogramFilter

    def get_queryset(self):
        """
        """
        queryset = (
            KilogramWeighMeasurement.objects.all()
            .order_by("-weigh_at")
        )
        if not settings.TESTING:
            queryset = queryset.using('kilogram')

        return queryset


class WeighDataSiteWeekView(DatapuntViewSet):
    """Weekly Site Faction statistics."""

    queryset = (
        SiteFractieStatWeek.objects.all()
        .order_by('-year')
        .order_by('-week')
        .prefetch_related("site")
    )

    pagination_class = KiloPager

    serializer_class = SiteFractieStatWeekSerializer
    serializer_detail_class = SiteFractieStatWeekSerializer
    filter_backends = (DjangoFilterBackend,)


class WeighDataSiteMonthView(DatapuntViewSet):
    """
    """
    queryset = (
        SiteFractieStatMonth.objects.all()
        .order_by('-year')
        .order_by('-month')
        .prefetch_related("site")
    )

    pagination_class = KiloPager

    serializer_class = SiteFractieStatMonthSerializer
    serializer_detail_class = SiteFractieStatMonthSerializer
    filter_backends = (DjangoFilterBackend,)


class WeighDataBuurtWeekView(DatapuntViewSet):
    """
    """
    queryset = (
        BuurtFractieStatWeek.objects.all()
        .order_by('-year')
        .order_by('-week')
        .prefetch_related("buurt")
    )

    pagination_class = KiloPager
    serializer_class = BuurtFractieStatWeekSerializer
    serializer_detail_class = BuurtFractieStatWeekSerializer
    filter_backends = (DjangoFilterBackend,)


class WeighDataBuurtMonthView(DatapuntViewSet):
    """
    """
    queryset = (
        BuurtFractieStatMonth.objects.all()
        .order_by('year')
        .order_by('month')
        .prefetch_related("buurt")
    )

    pagination_class = KiloPager

    filter_fields = (
        'buurt',
        'month', 'year')
    serializer_class = BuurtFractieStatMonthSerializer
    serializer_detail_class = BuurtFractieStatMonthSerializer
    filter_backends = (DjangoFilterBackend,)
