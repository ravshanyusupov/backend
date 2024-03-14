from src.apps.statistics.excels.base import BaseExcelReport


class WithinRepublicStorage(BaseExcelReport):
    def __init__(self, data_for_by_storage_place):
        super().__init__()
        self.data_for_by_storage_place = data_for_by_storage_place
        self.processed_products = set()


    def dynamic_values_for_cec_by_storage_place(self, start_row=4, region_start_row=7):
        col_index = 2
        processed_categories = {}
        self.processed_buildings = []
        regions = []
        product_col_indices = {}
        last_row = region_start_row
        building_col_index = col_index
        color_index = 0

        for product in self.data_for_by_storage_place.get('products', []):
            region = product.get('region', '')
            if region not in regions:
                regions.append(region)
                self.worksheet.write(last_row, 0, len(regions), self.usual_format)
                self.worksheet.write(last_row, 1, region.capitalize(), self.usual_format)
                inventory_index = 2

            for category in product.get('categories', []):
                category_format = self.get_format_with_bg_color(color_index)
                length_of_buildings_for_categories = 0
                category_name = category.get('category_name', '')
                product_col_index = col_index
                amount_of_products = 0

                for product_name, items in category.get('items', {}).items():
                    category['items'][product_name] = items
                    product_id = [item['product_id'] for item in items]
                    region_row = last_row

                    if product_id[0] not in self.processed_products:
                        length_of_buildings_for_products = 0
                        self.processed_buildings = []

                        for item in items:
                            building_category = item["building_category"]
                            if building_category not in self.processed_buildings:
                                building_category_splitted = ' '.join([word if len(word) <= 4 else word + '\n' for word in building_category.split()]).rstrip('\n')
                                self.worksheet.write(start_row + 2, building_col_index, building_category_splitted, category_format)
                                self.processed_buildings.append(building_category)
                                building_col_index += 1
                                length_of_buildings_for_products += 1
                                length_of_buildings_for_categories += 1

                        length_of_buildings_for_products = length_of_buildings_for_products if length_of_buildings_for_products > 0 else 1
                        
                        if length_of_buildings_for_products < 2:
                            self.worksheet.write(start_row + 1, product_col_index, product_name, category_format)
                        else:
                            self.worksheet.merge_range(start_row + 1, product_col_index, start_row + 1, product_col_index + length_of_buildings_for_products - 1, product_name, category_format)
                        self.processed_products.add(product_id[0])
                        amount_of_products += 1
                        product_col_indices[product_id[0]] = product_col_index
                        product_col_index += length_of_buildings_for_products

                    for item in items:
                        inventory_count = item["inventory_counts"]
                        self.worksheet.write(region_row, inventory_index, inventory_count, self.usual_format)
                        inventory_index += 1

                if category_name not in processed_categories:
                    length_of_buildings_for_categories = length_of_buildings_for_categories if length_of_buildings_for_categories > 0 else amount_of_products
                    if product_col_index - col_index == 0 or length_of_buildings_for_categories == 1:
                        self.worksheet.write(start_row, col_index, category_name, category_format)
                    else:
                        self.worksheet.merge_range(start_row, col_index, start_row, product_col_index - 1, category_name, category_format)
                    processed_categories[category_name] = (col_index, product_col_index - 1)

                col_index = product_col_index
                color_index += 1
            last_row += 1

        self.write_totals(region_start_row, last_row - 1, product_col_indices, times_per_product = len(self.processed_buildings) if self.processed_buildings else 1)

    def generate_report(self):
        self.dynamic_values_for_cec_by_storage_place()
        self.set_headers(for_b5="Xududlar nomi", format=self.header_format)
        self.worksheet.autofit()
        length_for_title_for_by_storage_place = len(self.processed_products) * len(self.processed_buildings) if len(self.processed_buildings) > 0 else len(self.processed_products)
        end_cell_for_by_storage_place_title = self.get_column_letter(length_for_title_for_by_storage_place + 2 if self.processed_products else 3)
        self.set_title(
            "Xududlarda saqlanayotgan saylov jihozlari haqida\n MA'LUMOT", 
            format=self.title_format, 
            start_cell='A2', 
            end_cell=f'{end_cell_for_by_storage_place_title}3'
            )
        self.close()


    