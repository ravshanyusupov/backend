import os
import json
import logging

from django.core.management.base import BaseCommand

from src.apps.dictionary.models import Region, District, BuildingCategory
from src.apps.inventory.models import Category, Product

logger = logging.getLogger(__name__)

BASE_STATIC = "src/static_data/"


class Command(BaseCommand):
    help = "Populate database with result.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "-rd",
            "--regions_districts",
            action="store_true",
            help="Populates database with Regions and Districts",
        )
        parser.add_argument(
            "-bc",
            "--building_categories",
            action="store_true",
            help="Populates database with Building Categories",
        )
        parser.add_argument(
            "-cp",
            "--categories_products",
            action="store_true",
            help="Populates database with Categories and Products",
        )
        parser.add_argument(
            "-a",
            "--all_fields",
            action="store_true",
            help="Execute all functions",
        )

    def create_regions_districts(self):
        json_file = os.path.join(BASE_STATIC, "result.json")
        with open(json_file) as file:
            data = json.load(file)
        for region_data in data:
            region, created = Region.objects.update_or_create(
                name_uz=region_data["region"]["name_uz"],
                defaults={
                    "name_ru": region_data["region"]["name_ru"],
                    "name_uz": region_data["region"]["name_uz"],
                },
            )
            for item in region_data["districts"]:
                District.objects.update_or_create(
                    name_uz=item["name_uz"],
                    region=region,
                    defaults={
                        "name_ru": item["name_ru"],
                        "name_uz": item["name_uz"],
                    },
                )

    def create_building_categories(self, modelName, filename):
        with open(os.path.join(BASE_STATIC, filename)) as file:
            data = json.load(file)
        for items in data:
            modelName.objects.update_or_create(
                name_uz=items["name_uz"],
                defaults={"name_ru": items["name_ru"], "name_uz": items["name_uz"]},
            )

    def create_categories_products(self, modelName1, modelName2, filename):
        with open(os.path.join(BASE_STATIC, filename)) as file:
            data = json.load(file)
        for category_data in data:
            category, created = modelName1.objects.update_or_create(
                name_uz=category_data["categories"]["name_uz"],
                defaults={
                    "name_ru": category_data["categories"]["name_ru"],
                    "name_uz": category_data["categories"]["name_uz"],
                },
            )
            for products in category_data["categories"]["products"]:
                modelName2.objects.update_or_create(
                    name_uz=products["name_uz"],
                    category=category,
                    defaults={
                        "name_ru": products["name_ru"],
                        "name_uz": products["name_uz"],
                    },
                )

    def handle(self, *args, **kwargs):
        if kwargs["regions_districts"] or kwargs["all_fields"]:
            self.create_regions_districts()
        if kwargs["building_categories"] or kwargs["all_fields"]:
            self.create_building_categories(
                BuildingCategory, "building_categories.json"
            )
        if kwargs["categories_products"] or kwargs["all_fields"]:
            self.create_categories_products(
                Category, Product, "categories_products.json"
            )

        self.stdout.write(self.style.SUCCESS("Done!"))
