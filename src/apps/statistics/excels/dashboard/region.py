from src.apps.statistics.excels.base import BaseExcelReport


class RegionUserReport(BaseExcelReport):
    def __init__(self, data):
        for_c5 = "Ma'sul shaxs\n(F.I.Sh. passport yoki\nID-karta raqami)"
        super().__init__(sheet_name="Viloyat", for_c5=for_c5)
        self.data = data
        self.processed_products = set()

    def dynamic_values_for_region(self, start_row=4, region_start_row=7, format=None):
        col_index = 3
        processed_categories = {}
        areas = []
        product_col_indices = {}
        responsible_persons_row = region_start_row
        last_row = region_start_row
        color_index = 0

        for index_number, product in enumerate(self.data.get("products", []), start=1):
            resp_pers = product.get("responsible_persons", [])
            area_name = product.get("district_name_uz", "")
            areas.append(area_name)

            full_names = ", \n".join(
                f"{person.get('first_name', '')} {person.get('last_name', '')} {person.get('middle_name', '')} ({person.get('passport_serial', '')})"
                for person in resp_pers
            )

            self.worksheet.write(
                responsible_persons_row, 2, full_names, self.usual_format
            )
            last_row = responsible_persons_row

            self.worksheet.write(
                responsible_persons_row, 0, index_number, self.usual_format
            )
            self.worksheet.write(
                responsible_persons_row, 1, area_name, self.usual_format
            )

            for category in product.get("categories", []):
                category_format = self.get_format_with_bg_color(color_index)
                category_name = category.get("category_name_uz", "")
                product_col_index = col_index
                amount_of_products = 0

                items = category.get("items", [])

                for item in items:
                    product_name = item.get("product_name_uz", "")
                    inventory_count = item.get("inventory_count", 0)
                    unique_product_name = (product_name, category_name)

                    if unique_product_name not in self.processed_products:
                        self.worksheet.merge_range(
                            start_row + 1,
                            product_col_index,
                            start_row + 2,
                            product_col_index,
                            product_name,
                            category_format,
                        )
                        self.processed_products.add(unique_product_name)
                        product_col_indices[unique_product_name] = product_col_index
                        product_col_index += 1
                        amount_of_products += 1

                    region_row = responsible_persons_row
                    self.worksheet.write(
                        region_row,
                        product_col_indices[unique_product_name],
                        inventory_count,
                        self.usual_format,
                    )

                if category_name not in processed_categories:
                    if product_col_index - col_index < 2 or amount_of_products < 2:
                        self.worksheet.write(
                            start_row, col_index, category_name, category_format
                        )
                    else:
                        self.worksheet.merge_range(
                            start_row,
                            col_index,
                            start_row,
                            product_col_index - 1,
                            category_name,
                            category_format,
                        )
                    processed_categories[category_name] = (
                        col_index,
                        product_col_index - 1,
                    )

                col_index = product_col_index
                color_index += 1

            responsible_persons_row = last_row + 1

        self.write_totals(region_start_row, last_row, product_col_indices)

    def generate_report(self):
        self.set_headers(for_b5="Tuman/Shahar nomi", format=self.header_format)
        self.dynamic_values_for_region(format=self.header_format)
        self.worksheet.autofit()
        end_cell_for_region_title = self.get_column_letter(
            len(self.processed_products) + 3 if self.processed_products else 4
        )
        region_name = self.data.get("region_name_uz", "")
        self.set_title(
            f"{region_name.capitalize()}da saqlanayotgan saylov jihozlari to'g'risida ma'lumot",
            format=self.title_format,
            start_cell="A2",
            end_cell=f"{end_cell_for_region_title}3",
        )
        self.close()
