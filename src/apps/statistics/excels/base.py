import io

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
from django.http import HttpResponse
from django.utils import timezone


class BaseExcelReport:
    def __init__(self, sheet_name='Sheet1', for_c5=None, for_d5=None):
        self.output = io.BytesIO()
        self.workbook = xlsxwriter.Workbook(self.output, {'in_memory': True})
        self.worksheet = self.workbook.add_worksheet(sheet_name)
        self.title_format = self.workbook.add_format({'size': 13, 'bold': True, 'align': 'center', 'valign': 'vcenter','border': 1, 'text_wrap': True})
        self.header_format = self.workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter','border': 1, 'text_wrap': True, 'bg_color': '#e2f0da'})
        self.usual_format = self.workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
        self.total_format = self.workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'num_format': '### ### ### ### ##0'})
        self.by_year_product_format = self.workbook.add_format({'valign': 'vcenter', 'border': 3})
        self.by_year_category_format = self.workbook.add_format({'bold': True, 'valign': 'vcenter', 'border': 1})
        self.by_year_header_format = self.workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        self.by_year_header_format.set_text_wrap()
        self.header_format.set_text_wrap()
        self.usual_format.set_text_wrap()
        self.total_format.set_text_wrap()
        self.for_c5 = for_c5
        self.for_d5 = for_d5
        self.colors = ['#F1F7B7', '#F2E6ED', '#CEDCED', '#E8E8E8', '#CCCCCC', '#B0E899', '#fceed7']

    def set_title(self, title, format=None, start_cell='C3', end_cell='M3'):
        merged_cell_range = f'{start_cell}:{end_cell}'
        self.worksheet.merge_range(merged_cell_range, title, format)

    def get_column_letter(self, col_idx):
        letters = ''
        while col_idx:
            col_idx, remainder = divmod(col_idx - 1, 26)
            letters = chr(65 + remainder) + letters
        return letters
    
    def get_format_with_bg_color(self, color_index):
        bg_color = self.colors[color_index % len(self.colors)]
        format = self.workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter','border': 1, 'text_wrap': True, 'bg_color': bg_color})
        format.set_text_wrap()
        return format

    def set_headers(self, for_b5, start_row=5, format=None, for_c5=None, for_d5=None):
        self.worksheet.merge_range('A5:A7', '№', format)
        self.worksheet.set_column('A:A', 5)
        self.worksheet.merge_range(f'B{start_row}:B{start_row + 2}', for_b5, format)
        if self.for_c5 or for_c5:
            self.worksheet.merge_range(f'C{start_row}:C{start_row + 2}', self.for_c5 or for_c5, format)
        if self.for_d5 or for_d5:
            self.worksheet.merge_range(f'D{start_row}:D{start_row + 2}', self.for_d5 or for_d5, format)
    
    def write_totals(self, start_row, last_row, product_col_indices, times_per_product=1):
        total_row = last_row + 1

        if not self.for_c5 and not self.for_d5:
            self.worksheet.write(total_row, 1, "Jami:", self.total_format)
        else:
            merge_start = 1
            merge_end = 3 if self.for_d5 else 2
            self.worksheet.merge_range(total_row, merge_start, total_row, merge_end, "Jami:", self.total_format)

        for _, col_index in product_col_indices.items():
            for i in range(times_per_product):
                start_cell = xl_rowcol_to_cell(start_row, col_index + i)
                end_cell = xl_rowcol_to_cell(total_row - 1, col_index + i)
                self.worksheet.write_formula(total_row, col_index + i, f"=SUM({start_cell}:{end_cell})", self.total_format)


    def close(self):
        self.workbook.close()
        self.output.seek(0)

    def last_updated_at(self):
        pass

    def get_http_response(self, filename_prefix):
        response = HttpResponse(
            self.output.read(), content_type='application/ms-excel')
        now = timezone.now()
        filename = f'{filename_prefix}_{now.strftime("%Y-%m-%d_%H-%M")}.xlsx'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        self.output.close()
        return response
    