from src.apps.statistics.excels.base import BaseExcelReport


class WithinRegion(BaseExcelReport):
    def __init__(self, data, region_name):
        super().__init__(sheet_name='Viloyat')
        self.data = data
        self.region_name = region_name
        self.processed_products = set()

    def within_region(self, start_row=4, format=None):
        col_index = 2
        processed_categories = {}
        districts = []
        product_col_indices = {}
        last_row = start_row + 3
        color_index = 0
        
        for place_number, (district_name, district_data) in enumerate(self.data.items(), start=1):
            if district_name not in districts:
                districts.append(district_name)
                self.worksheet.write(last_row, 0, place_number, self.usual_format)
                self.worksheet.write(last_row, 1, district_name, self.usual_format)
                last_row += 1

            for category_item in district_data['category_items']:
                category_format = self.get_format_with_bg_color(color_index)
                category_name = category_item['category_name']
                amount_of_products = 0
                product_col_index = col_index

                for item in category_item['items']:
                    product_name = item['product_name']
                    inventory_count = item['inventory_count']

                    if product_name not in self.processed_products:
                        self.worksheet.merge_range(start_row + 1, product_col_index, start_row + 2, product_col_index, product_name, category_format)
                        self.processed_products.add(product_name)
                        product_col_indices[product_name] = product_col_index
                        product_col_index += 1
                        amount_of_products += 1

                    self.worksheet.write(last_row - 1, product_col_indices[product_name], inventory_count, self.usual_format)

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
        self.set_headers(for_b5=f'Tuman nomi*', format=self.header_format)
        self.within_region(format=self.header_format)
        self.worksheet.autofit()
        end_cell_for_title = self.get_column_letter(len(self.processed_products) + 2 if self.processed_products else 3)
        self.set_title(
            f"{self.region_name.capitalize()}da saqlanayotgan saylov jihozlari to'g'risida ma'lumot", 
            format=self.title_format, 
            start_cell='A2', 
            end_cell=f'{end_cell_for_title}3')
        self.close()