from src.apps.statistics.excels.base import BaseExcelReport


class CECUserReport(BaseExcelReport):
    def __init__(self, data, sheet_name='Respublika'):
        super().__init__(sheet_name)
        self.data = data
        self.processed_products = set()

    def dynamic_values_for_cec(self, start_row=4, region_start_row=7, format=None):
        col_index = 2
        processed_categories = {}
        regions = []
        product_col_indices = {}
        last_row = region_start_row
        color_index = 0

        for place_number, product in enumerate(self.data.get('products', []), start=1):
            region = product.get('region_name_uz', '')
            if region not in regions:
                regions.append(region)
                self.worksheet.write(last_row, 0, place_number, self.usual_format)
                self.worksheet.write(last_row, 1, region.capitalize(), self.usual_format)

            for category in product.get('categories', []):
                category_format = self.get_format_with_bg_color(color_index)
                category_name = category.get('category_name_uz', '')
                product_col_index = col_index
                amount_of_products = 0

                for item in category.get('items', []):
                    product_name = item.get('product_name_uz', '')
                    inventory_count = item.get('inventory_count', 0)
                    if item.get('product_id'):
                        product_id = item.get('product_id', 0)
                    else:
                        product_id = (product_name, category_name)

                    if product_id not in self.processed_products:
                        self.worksheet.merge_range(start_row + 1, product_col_index, start_row + 2, product_col_index, product_name, category_format)
                        self.processed_products.add(product_id)
                        product_col_indices[product_id] = product_col_index
                        product_col_index += 1
                        amount_of_products += 1

                    region_row = last_row
                    self.worksheet.write(region_row, product_col_indices[product_id], inventory_count, self.usual_format)

                if category_name not in processed_categories:
                    if product_col_index - col_index < 2 or amount_of_products < 2:
                        self.worksheet.write(start_row, col_index, category_name, category_format)
                    else:
                        self.worksheet.merge_range(start_row, col_index, start_row, product_col_index - 1, category_name, category_format)
                    processed_categories[category_name] = (col_index, product_col_index - 1)

                col_index = product_col_index
                color_index += 1

            last_row += 1

        self.write_totals(region_start_row, last_row - 1, product_col_indices)
    
    def generate_report(self):
        self.set_headers(for_b5="Xududlar nomi", format=self.header_format)
        self.dynamic_values_for_cec(format=self.header_format)
        self.worksheet.autofit()
        end_cell_for_cec_title = self.get_column_letter(len(self.processed_products) + 2 if len(self.processed_products) else 3)
        self.set_title(
            "Xududlarda saqlanayotgan saylov jihozlari haqida ma'lumot",
            format=self.title_format, 
            start_cell='A2', 
            end_cell=f'{end_cell_for_cec_title}3')
        self.close()