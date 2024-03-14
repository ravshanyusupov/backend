from src.apps.statistics.excels.base import BaseExcelReport


class WithinRepublicPercent(BaseExcelReport):
    def __init__(self, data_for_by_percent):
        super().__init__()
        self.data_for_by_percent = data_for_by_percent
        self.processed_products = set()


    def dynamic_values_for_percent(self, start_row=4, region_start_row=7):
        regions = []
        processed_categories = set()
        product_col_indices = {}
        cabinets_inventory_counts = {}
        cabinet_rooms = set()
        region_inventory_counts = {}
        cabinet_rooms_str = ""
        substring = "Yashirin ovoz berish kabinalari".lower()
        special_category_name = None
        special_category_format = self.header_format
        last_row = 7
        product_col_index = 3
        color_index = 0

        for index_number, product in enumerate(self.data_for_by_percent.get('products', []), start=1):
            region = product.get('region', '')
            precincts_count = product.get('precincts_count', 0)
            if region not in regions:
                regions.append(region)
                total_inventory_count = 0
                cabinets_inventory_counts = {}
                self.worksheet.write(region_start_row, 0, index_number, self.usual_format)
                self.worksheet.write(region_start_row, 1, region.capitalize(), self.usual_format)
                self.worksheet.write(region_start_row, 2, precincts_count, self.usual_format)

            product_col_index = 3
            last_row = region_start_row

            special_items = []
            for category in product.get('categories', []):
                category_format = self.get_format_with_bg_color(color_index)
                category_name = category.get('category_name', '')
                if substring in category_name.lower():
                    special_category_name = category_name
                    
                    for product_name, items in category.get('items', {}).items():
                        inventory_count = items[0]["inventory_counts"]
                        if "xonali kabinalar" in product_name:
                            cabinets_inventory_counts[product_name] = cabinets_inventory_counts.get(product_name, 0) + inventory_count
                            cabinet_rooms.add(product_name.split()[0])
                            region_inventory_counts[region] = region_inventory_counts.get(region, 0) + inventory_count
                        else:
                            special_items.append((product_name, items))
                    continue
                col_index = product_col_index
                color_index += 1

                for product_name, items in category.get('items', {}).items():
                    inventory_count = items[0]["inventory_counts"]
                    product_id = items[0]["product_id"]
                    
                    if product_id not in self.processed_products:
                        self.worksheet.write(start_row + 2, product_col_index, 'soni', category_format)
                        self.worksheet.write(start_row + 2, product_col_index + 1, ' %  ', category_format)
                        self.worksheet.merge_range(start_row + 1, product_col_index, start_row + 1, product_col_index + 1, product_name, category_format)
                        self.processed_products.add(product_id)
                        product_col_indices[product_name] = product_col_index
                    percentage = round(inventory_count / precincts_count * 100) if precincts_count else 0
                    self.worksheet.write(last_row, product_col_index, inventory_count, self.usual_format)
                    self.worksheet.write(last_row, product_col_index + 1, f"  {percentage} % ", self.usual_format)
                    product_col_index += 2


                if category_name not in processed_categories:
                    if product_col_index - col_index == 0:
                        self.worksheet.write(start_row, col_index, category_name, category_format)
                    else:
                        self.worksheet.merge_range(start_row, col_index, start_row, product_col_index - 1, category_name, category_format)
                    processed_categories.add(category_name)

            special_category_format = self.get_format_with_bg_color(len(processed_categories))
            if special_category_name and special_category_name not in processed_categories and special_items:
                length = len(special_items) + 2
                self.worksheet.merge_range(start_row, product_col_index, start_row, product_col_index + length, special_category_name, special_category_format)
                processed_categories.add(special_category_name)
            elif special_category_name and special_category_name not in processed_categories:
                self.worksheet.merge_range(start_row, product_col_index, start_row, product_col_index + 1, special_category_name, special_category_format)
                processed_categories.add(special_category_name)

            for product_name, items in special_items:
                inventory_count = items[0]["inventory_counts"]
                if product_name not in self.processed_products:
                    self.worksheet.write(start_row + 2, product_col_index, 'soni', special_category_format)
                    self.worksheet.write(start_row + 2, product_col_index + 1, ' %  ', special_category_format)
                    self.worksheet.merge_range(start_row + 1, product_col_index, start_row + 1, product_col_index + 1, product_name, special_category_format)
                    self.processed_products.add(product_name)
                    product_col_indices[product_name] = product_col_index
                percentage = round(inventory_count / precincts_count * 100) if precincts_count else 0
                self.worksheet.write(last_row, product_col_index, inventory_count, self.usual_format)
                self.worksheet.write(last_row, product_col_index + 1, f"  {percentage} % ", self.usual_format)
                product_col_index += 2

            if cabinet_rooms:
                
                cabinet_rooms_sorted = sorted(cabinet_rooms)
                cabinet_rooms_str = ', '.join(map(str, cabinet_rooms_sorted))
                if f"{cabinet_rooms_str} xonali kabinalar" not in self.processed_products:
                    self.worksheet.merge_range(start_row + 1, product_col_index, start_row + 1, product_col_index + 1, f"{cabinet_rooms_str} xonali kabinalar", special_category_format)
                    self.worksheet.write(start_row + 2, product_col_index, 'soni', special_category_format)
                    self.worksheet.write(start_row + 2, product_col_index + 1, ' %  ', special_category_format)
                    self.processed_products.add(f"{cabinet_rooms_str} xonali kabinalar")
                total_inventory_count = sum(cabinets_inventory_counts.values())
                percentage = round(total_inventory_count / precincts_count * 100) if precincts_count else 0
                self.worksheet.write(last_row, product_col_index, region_inventory_counts.get(region, 0), self.usual_format)
                self.worksheet.write(last_row, product_col_index + 1, f"  {percentage} % ", self.usual_format)

            region_start_row += 1

        total_row = last_row + 1
        self.worksheet.write(total_row, 1, "Jami: ", self.total_format)
        formula_for_precints = f'=SUM(C{region_start_row - len(regions) + 1}:C{total_row})'
        self.worksheet.write_formula(total_row, 2, formula_for_precints, self.total_format)

        range_for_loop = product_col_index + 2 if cabinet_rooms else product_col_index + 1
        for i, col_index in enumerate(range(4, range_for_loop, 2)):
            column_letter = chr(68 + i*2)
            start_row = region_start_row - len(regions) + 1
            end_row = region_start_row
            formula = f'=SUM({column_letter}{start_row}:{column_letter}{end_row})'
            self.worksheet.write_formula(total_row, col_index-1, formula, self.total_format)

        for i, col_index in enumerate(range(4, range_for_loop, 2)):
            column_letter = chr(68 + i*2)
            formula = f'=IF(C{total_row + 1}=0, 0, IF({column_letter}{total_row + 1}=0, 0, ROUND({column_letter}{total_row + 1}/C{total_row + 1}*100, 0)))'
            self.worksheet.write_formula(total_row, col_index, f'{formula}&" %"', self.total_format)


    def generate_report(self):
        self.dynamic_values_for_percent()
        self.set_headers(for_b5="Xududlar nomi", for_c5="Uchastkalar\n soni", format=self.header_format)
        self.worksheet.autofit()
        length_for_title = len(self.processed_products) * 2
        end_cell_for_title = self.get_column_letter(length_for_title + 3 if length_for_title else 5)
        self.set_title(
            "Xudularda saqlanayotgan saylov jihozlari haqida\n MA'LUMOT", 
            format=self.title_format, 
            start_cell='A2', 
            end_cell=f'{end_cell_for_title}3'
            )
        self.close()


    