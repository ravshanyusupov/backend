from collections import Counter

from src.apps.statistics.excels.base import BaseExcelReport


class WithinDistrict(BaseExcelReport):
    def __init__(self, data, region_name, district_name):
        super().__init__(
            sheet_name='Tuman miqyosida', 
            for_c5='Balansda saqlovchi,\n inventar raqami',
            for_d5="Ma'sul shaxs\n(F.I.Sh. passport yoki\nID-karta raqami)"
            )
        self.data = data
        self.region_name = region_name
        self.district_name = district_name
        self.processed_products = set()


    def within_district(self, start_row=4, format=None):
        col_index = 4
        processed_categories = set()
        product_col_indices = {}
        
        all_responsible_persons = set()
        last_row = start_row + 3
        col_of_address = col_index
        responsible_persons_start_row = last_row
        inventory_counter = 1
        color_index = 0

        if self.data.get('products'):
            storage_places = self.data['products']
            for product in self.data['products']:
                address = product['address']
                for person in product['responsible_persons']:
                    all_responsible_persons.add(person)

                for category in product['category_names']:
                    category_format = self.get_format_with_bg_color(color_index)
                    category_name = category["category_name"]
                    amount_of_products = 0
                    items = category['items']
                    product_col_index = col_index

                    for item in items:
                        product_name = item['product_name']
                        if product_name not in self.processed_products:
                            self.worksheet.merge_range(start_row + 1, product_col_index, start_row + 2, product_col_index, product_name, category_format)
                            self.processed_products.add(product_name)
                            product_col_indices[product_name] = product_col_index
                            product_col_index += 1
                            amount_of_products += 1

                    if category_name not in processed_categories:
                        if product_col_index - col_index < 2 or amount_of_products < 2:
                            self.worksheet.write(start_row, col_index, category_name, category_format)
                        else:
                            self.worksheet.merge_range(start_row, col_index, start_row, product_col_index - 1, category_name, category_format)
                        processed_categories.add(category_name)

                    col_index = product_col_index
                    color_index += 1
                start_row += 1

            last_row = responsible_persons_start_row
            for product in self.data['products']:
                address = product['address']
                for category in product['category_names']:
                    items = category['items']

                    for item in items:
                        if item['inventory_count'] and item['inventory_number']:
                            inventory_count = item['inventory_count']
                            inventory_number = item['inventory_number']
                            product_name = item['product_name']

                            self.worksheet.write(last_row, col_of_address - 3, address, self.usual_format)
                            self.worksheet.write(last_row, col_of_address - 2, inventory_number, self.usual_format)
                            self.worksheet.write(last_row, 0, inventory_counter, self.usual_format)
                            for product in self.processed_products:
                                if product == product_name:
                                    self.worksheet.write(last_row, product_col_indices[product], inventory_count, self.usual_format)
                                else:
                                    self.worksheet.write(last_row, product_col_indices[product], None, self.usual_format)

                            last_row += 1
                            inventory_counter += 1

            keys_list = [key for d in storage_places for key in d]
            address_count = Counter(keys_list)['address']
            resp_persons = ", \n".join(all_responsible_persons)
            if address_count > 1:
                self.worksheet.merge_range(responsible_persons_start_row, 3, last_row - 1, 3, resp_persons, self.usual_format)
            elif address_count == 1:
                self.worksheet.write(responsible_persons_start_row, 3, resp_persons, self.usual_format)        
            self.write_totals(7, last_row - 1, product_col_indices)


    def generate_report(self):
        self.set_headers(for_b5=f'Saqlash joyi\n(manzili)', format=self.header_format)
        self.within_district(format=self.header_format)
        self.worksheet.autofit()
        end_cell_for_title = self.get_column_letter(len(self.processed_products) + 4 if self.processed_products else 8)
        self.set_title(
            f"{self.region_name.capitalize()} {self.district_name}da saqlanayotgan saylov jihozlari to'g'risida ma'lumot", 
            format=self.title_format, 
            start_cell='A2', 
            end_cell=f'{end_cell_for_title}3')
        self.close()
