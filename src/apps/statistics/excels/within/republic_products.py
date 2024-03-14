from src.apps.statistics.excels.dashboard.cec import CECUserReport


class WithinRepublicProducts(CECUserReport):
    def __init__(self, data_for_by_products):
        super().__init__(data_for_by_products, sheet_name='Sheet1')
        self.data_for_by_products = data_for_by_products

    def generate_report(self):
        self.dynamic_values_for_cec(format=self.header_format)
        self.set_headers(for_b5="Xududlar nomi", format=self.header_format)
        self.worksheet.autofit()
        unique_product_names = set()
        for products in self.data_for_by_products.get('products', []):
            for categories in products.get('categories', []):
                for items in categories.get('items', []):
                    unique_product_names.add(items.get('product_id', ''))
                
        end_cell_for_by_products_title = self.get_column_letter(len(unique_product_names) + 2 if unique_product_names else 3)
        self.set_title(
            "Xududlarda saqlanayotgan saylov jihozlari haqida MA'LUMOT", 
            format=self.title_format, 
            start_cell='A2', 
            end_cell=f'{end_cell_for_by_products_title}3'
            )
        self.close()


    