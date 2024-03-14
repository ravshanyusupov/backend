from asgiref.sync import sync_to_async
from datetime import datetime

from xlsxwriter.utility import xl_rowcol_to_cell, xl_col_to_name
from django.db.models import Min, Max

from src.apps.statistics.excels.base import BaseExcelReport
from src.apps.dictionary.models import Year


class WithinRepublicYear(BaseExcelReport):
    def __init__(self, data_for_by_year):
        super().__init__()
        self.data_for_by_year = data_for_by_year
        self.written_products = set()
        self.written_regions = 0

    def set_headers_for_by_year(self):
        self.worksheet.merge_range('A4:A5', 'Jixozlar nomi', self.by_year_header_format)
        self.worksheet.merge_range('B4:B5', '  yil   ', self.by_year_header_format)
        self.worksheet.merge_range('C4:C5', 'narxi', self.by_year_header_format)
    
    def dynamic_values_for_by_year(self):
        col = 3
        row = 5
        written_categories = set()
        column_totals = {}
        year_price_totals = {}
        inv_row = 6

        if self.data_for_by_year.get('products'):
            for i, product in enumerate(self.data_for_by_year['products']):
                inv_row = 6
                if i == len(self.data_for_by_year['products']):
                    region = 'JAMI:'
                else:
                    region = product['region']
                    region = region.capitalize()

                self.worksheet.merge_range(3, col, 3, col+1, region, self.by_year_header_format)
                self.worksheet.write(4, col, 'soni', self.by_year_header_format)
                self.worksheet.write(4, col+1, 'summa', self.by_year_header_format)
                self.written_regions += 1

                for category in product['categories']:
                    category_name = category['category_name']
                    if category_name not in written_categories:
                        self.worksheet.write(row, 0, category_name, self.by_year_category_format)
                        written_categories.add(category_name)
                        row += 1

                    for product_name_id, year_price_count in category['items'].items():
                        product_name, product_id = product_name_id.split('_')

                        if product_id not in self.written_products:
                            self.written_products.add(product_id)
                            
                            if len(year_price_count) > 1:
                                self.worksheet.merge_range(row, 0, row+len(year_price_count)-1, 0, product_name, self.by_year_product_format)
                            elif len(year_price_count) == 0:
                                self.worksheet.write(row, 0, product_name, self.by_year_product_format)
                                self.worksheet.write(row, 1, " ", self.by_year_product_format)
                                self.worksheet.write(row, 2, 0, self.by_year_product_format)
                                row += 1
                            else:
                                self.worksheet.write(row, 0, product_name, self.by_year_product_format)

                            year_price_count.sort(key=lambda x: x['year'])

                            for item in year_price_count:
                                self.worksheet.write(row, 1, item['year'], self.usual_format)
                                self.worksheet.write(row, 2, item['price'], self.by_year_product_format)
                                year_price_totals[item['year']] = year_price_totals.get(item['year'], 0) + item['price']
                                row += 1

                        year_price_count.sort(key=lambda x: x['year'])
                        if len(year_price_count) >= 1:
                            for item in year_price_count:
                                self.worksheet.write(inv_row, col, item['inventory_count'], self.by_year_product_format)
                                sum_of_price_and_count = item['price'] * item['inventory_count']
                                self.worksheet.write(inv_row, col+1, sum_of_price_and_count, self.by_year_product_format)
                                if item['year'] not in column_totals:
                                    column_totals[item['year']] = {}
                                column_totals[item['year']][col] = column_totals[item['year']].get(col, 0) + item['inventory_count']
                                column_totals[item['year']][col+1] = column_totals[item['year']].get(col+1, 0) + sum_of_price_and_count
                                inv_row += 1
                        else:
                            self.worksheet.write(inv_row, col, 0, self.by_year_product_format)
                            self.worksheet.write(inv_row, col+1, 0, self.by_year_product_format)
                            inv_row += 1
                    inv_row += 1
                col += 2
        
            length_of_years = len(column_totals.keys()) if len(column_totals.keys()) > 2 else 3
            self.worksheet.merge_range(row, 0, row+length_of_years-1, 0, "YILLAR KESIMIDA\n JAMI:", self.total_format)
            for year, column_dict in column_totals.items():
                self.worksheet.write(inv_row-1, 1, year, self.by_year_header_format)
                for column, total in column_dict.items():
                    self.worksheet.write(inv_row-1, column, total, self.total_format)
                self.worksheet.write(inv_row-1, 2, year_price_totals[year], self.total_format)
                inv_row += 1
            
            key_length = len(column_totals.keys())
            total_row_dict = {key_length > 2: inv_row - 1, key_length == 2: inv_row, key_length == 1: inv_row + 1}
            total_row = total_row_dict.get(True, inv_row + 2)
            self.worksheet.merge_range(total_row, 0, total_row, 1, "HAMMASI:", self.total_format)
            start_row = 7
            end_row = total_row - length_of_years
            max_length = 0
            self.worksheet.write_formula(total_row, 2, f'=SUM({xl_col_to_name(2)}{start_row}:{xl_col_to_name(2)}{end_row})', self.total_format)
            for col_vertically in range(3, col, 2):

                soni_formula = f'=SUM({xl_col_to_name(col_vertically)}{start_row}:{xl_col_to_name(col_vertically)}{end_row})'
                self.worksheet.write_formula(total_row, col_vertically, soni_formula, self.total_format)

                summa_formula = f'=SUM({xl_col_to_name(col_vertically+1)}{start_row}:{xl_col_to_name(col_vertically+1)}{end_row})'
                self.worksheet.write_formula(total_row, col_vertically+1, summa_formula, self.total_format)
            
                length = len(f"=SUM({start_row}:{end_row})")
                if length > max_length:
                    max_length = length
            self.worksheet.set_column(2, col+1, max_length)

            start_row = 6
            end_row = total_row + 1
            end_col = col

            self.worksheet.merge_range(3, col, 3, col+1, 'JAMI:', self.by_year_header_format)
            self.worksheet.write(4, col, 'soni', self.by_year_header_format)
            self.worksheet.write(4, col+1, 'summa', self.by_year_header_format)

            for row_horizontally in range(start_row, end_row):
                cells = []
                for col_horizontally in range(3, end_col, 2):
                    cell = xl_rowcol_to_cell(row_horizontally, col_horizontally)
                    cells.append(cell)
                formula = f'=SUM({",".join(cells)})'
                self.worksheet.write_formula(row_horizontally, end_col, formula, self.total_format)

            for row_horizontally in range(start_row, end_row):
                cells = []
                for col_horizontally in range(4, end_col, 2):
                    cell = xl_rowcol_to_cell(row_horizontally, col_horizontally)
                    cells.append(cell)
                formula = f'=SUM({",".join(cells)})'
                self.worksheet.write_formula(row_horizontally, end_col + 1, formula, self.total_format)            
    
    async def generate_report(self):
        self.set_headers_for_by_year()
        self.dynamic_values_for_by_year()
        self.worksheet.autofit()
        end_cell_for_year_title = self.get_column_letter(5 + self.written_regions * 2 if self.written_regions != 0 else 3)
        result = await sync_to_async(Year.objects.aggregate)(Min('year'), Max('year'))
        if result['year__min'] and result['year__max']:
            min_year = result['year__min']
            max_year = result['year__max']
        else:
            min_year = max_year = datetime.now().year
        self.set_title(
            f"Xududlarga {min_year}-{max_year} yillarda bo'lib o'tgan saylovlarda yetkazib berilgan saylov jihozlari to'g'risida\n MA'LUMOT", 
            format=self.title_format,
            start_cell='A1', 
            end_cell=f'{end_cell_for_year_title}2'
            )
        self.close()
        