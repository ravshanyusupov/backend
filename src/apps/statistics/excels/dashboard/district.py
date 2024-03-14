from src.apps.statistics.excels.base import BaseExcelReport


class DistrictUserReport(BaseExcelReport):
    def __init__(self, data):
        for_c5 = 'Saqlash joyi\n(manzili)'
        super().__init__(sheet_name='Tuman-Shahar', for_c5=for_c5)
        self.data = data

    def dynamic_values_for_district(self, start_row=4, district_start_row=7):
        col_index = 3
        processed_products = set()
        processed_categories = {}
        districts = []
        product_col_indices = {}
        last_row = district_start_row
        color_index = 0

        if self.data.get('storage_place_products'):
            address_count = sum('address' in product for product in self.data['storage_place_products'])
            full_names = ", \n".join(
                f"{person.get('first_name', '')} {person.get('last_name', '')} {person.get('middle_name', '')} ({person.get('passport_serial', '')})"
                for person in self.data['responsible_persons']
            )
            if address_count > 1:
                self.worksheet.merge_range(
                    district_start_row, 1, district_start_row + address_count - 1, 1, full_names, self.usual_format
                )
            elif address_count <= 1:
                self.worksheet.write(district_start_row, 1, full_names, self.usual_format)

            for place_number, storage_place in enumerate(self.data.get('storage_place_products', []), start=1):
                address = storage_place.get('address', '')
                if address not in districts:
                    districts.append(address)
                    length_of_districts = len(districts) - 1
                    self.worksheet.write(district_start_row + length_of_districts, 0, place_number, self.usual_format)
                    self.worksheet.write(district_start_row + length_of_districts, 2, address, self.usual_format)
                    last_row += 1

                for category in storage_place.get('category_items', []):
                    category_format = self.get_format_with_bg_color(color_index)
                    category_name = category.get('category_name_uz', '')
                    amount_of_products = 0
                    product_col_index = col_index

                    items = category.get('items', [])

                    for item in items:
                        product_name = item.get('product_name_uz', '')
                        inventory_count = item.get('inventory_count', 0)
                        unique_product_naming = (product_name, category_name)

                        if unique_product_naming not in processed_products:
                            self.worksheet.merge_range(start_row + 1, product_col_index, start_row + 2, product_col_index, product_name, category_format)
                            processed_products.add(unique_product_naming)
                            product_col_indices[unique_product_naming] = product_col_index
                            product_col_index += 1
                            amount_of_products += 1

                        district_row = district_start_row + districts.index(address)
                        self.worksheet.write(district_row, product_col_indices[unique_product_naming], inventory_count, self.usual_format)

                    if category_name not in processed_categories:
                        if product_col_index - col_index < 2 or amount_of_products < 2:
                            self.worksheet.write(start_row, col_index, category_name, category_format)
                        else:
                            self.worksheet.merge_range(start_row, col_index, start_row, product_col_index - 1, category_name, category_format)
                        processed_categories[category_name] = (col_index, product_col_index - 1)

                    col_index = product_col_index
                    color_index += 1

            self.write_totals(7, last_row - 1, product_col_indices)
    
    def generate_report(self):
        self.set_headers(for_b5="Ma'sul shaxs\n(F.I.Sh. passport yoki\nID-karta raqami)", format=self.header_format)
        self.dynamic_values_for_district()
        self.worksheet.autofit()
        self.close()