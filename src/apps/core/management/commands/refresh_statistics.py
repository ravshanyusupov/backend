import asyncio

from django.core.management.base import BaseCommand, CommandParser

from src.apps.statistics.models import StatisticData
from src.apps.dictionary.models import Region, District
from src.apps.statistics.data.dashboard import (
    get_data_for_cec_user,
    get_data_for_region_user,
    get_data_for_district_user,
)
from src.apps.statistics.data.within import (
    get_data_within_district,
    get_data_within_region,
    get_data_for_cec_by_percent,
    get_data_for_cec_by_products,
    get_data_for_cec_by_storage_place,
    get_data_for_cec_by_year,
)


class Command(BaseCommand):
    help = "Refreshes data for processing and using it in Excel files"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-a", "--all", action="store_true", help="Execute all functions"
        )
        parser.add_argument(
            "-rdc",
            "--dashboard_cec",
            action="store_true",
            help="Refresh Dashboard data for CEC",
        )
        parser.add_argument(
            "-rdr",
            "--dashboard_region",
            action="store_true",
            help="Refresh Dashboard data for Region",
        )
        parser.add_argument(
            "-rdd",
            "--dashboard_district",
            action="store_true",
            help="Refresh Dashboard data for District",
        )
        parser.add_argument(
            "-rwd",
            "--within_district",
            action="store_true",
            help="Refresh data for Within District",
        )
        parser.add_argument(
            "-rwr",
            "--within_region",
            action="store_true",
            help="Refresh data for Within REgion",
        )
        parser.add_argument(
            "-rwrper",
            "--within_republic_percent",
            action="store_true",
            help="Refresh data for Within Republic Percentage",
        )
        parser.add_argument(
            "-rwrpro",
            "--within_republic_product",
            action="store_true",
            help="Refresh data for Within Republic Product",
        )
        parser.add_argument(
            "-rwrs",
            "--within_republic_storage",
            action="store_true",
            help="Refresh data for Within Republic Storage",
        )
        parser.add_argument(
            "-rwry",
            "--within_republic_year",
            action="store_true",
            help="Refresh data for Within Republic Year",
        )

    def refresh_dashboard_cec(self):
        data = asyncio.run(get_data_for_cec_user())
        StatisticData.objects.update_or_create(
            name="Dashboard_data_for_CEC",
            defaults={"data": data},
        )

    def refresh_dashboard_region(self):
        all_regions = Region.objects.all()
        for region in all_regions:
            data = asyncio.run(get_data_for_region_user(region.id))
            StatisticData.objects.update_or_create(
                name=f"Dashboard_data_for_region_{region.id}",
                defaults={"data": data},
            )

    def refresh_dashboard_district(self):
        all_districts = District.objects.all()
        for district in all_districts:
            data = asyncio.run(get_data_for_district_user(district.id))
            StatisticData.objects.update_or_create(
                name=f"Dashboard_data_for_district_{district.id}",
                defaults={"data": data},
            )

    def refresh_within_district(self):
        all_districts = District.objects.all()
        for district in all_districts:
            data = asyncio.run(get_data_within_district(district.id))
            StatisticData.objects.update_or_create(
                name=f"Data_for_within_district_{district.id}",
                defaults={"data": data},
            )

    def refresh_within_region(self):
        all_regions = Region.objects.all()
        for region in all_regions:
            data = asyncio.run(get_data_within_region(region.id))
            StatisticData.objects.update_or_create(
                name=f"Data_for_within_region_{region.id}",
                defaults={"data": data},
            )

    def refresh_within_republic_percent(self):
        data = asyncio.run(get_data_for_cec_by_percent())
        StatisticData.objects.update_or_create(
            name="Data_for_within_republic_percent",
            defaults={"data": data},
        )

    def refresh_within_republic_product(self):
        data = asyncio.run(get_data_for_cec_by_products())
        StatisticData.objects.update_or_create(
            name="Data_for_within_republic_product",
            defaults={"data": data},
        )

    def refresh_within_republic_storage(self):
        data = asyncio.run(get_data_for_cec_by_storage_place())
        StatisticData.objects.update_or_create(
            name="Data_for_within_republic_storage",
            defaults={"data": data},
        )

    def refresh_within_republic_year(self):
        data = asyncio.run(get_data_for_cec_by_year())
        StatisticData.objects.update_or_create(
            name="Data_for_within_republic_year",
            defaults={"data": data},
        )

    def handle(self, *args, **kwargs):
        if kwargs["dashboard_cec"] or kwargs["all"]:
            self.refresh_dashboard_cec()
        if kwargs["dashboard_region"] or kwargs["all"]:
            self.refresh_dashboard_region()
        if kwargs["dashboard_district"] or kwargs["all"]:
            self.refresh_dashboard_district()
        if kwargs["within_district"] or kwargs["all"]:
            self.refresh_within_district()
        if kwargs["within_region"] or kwargs["all"]:
            self.refresh_within_region()
        if kwargs["within_republic_percent"] or kwargs["all"]:
            self.refresh_within_republic_percent()
        if kwargs["within_republic_product"] or kwargs["all"]:
            self.refresh_within_republic_product()
        if kwargs["within_republic_storage"] or kwargs["all"]:
            self.refresh_within_republic_storage()
        if kwargs["within_republic_year"] or kwargs["all"]:
            self.refresh_within_republic_year()

        self.stdout.write(self.style.SUCCESS("Done!"))
