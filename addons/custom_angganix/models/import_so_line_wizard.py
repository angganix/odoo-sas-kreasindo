import base64
import csv
import logging
import io
import base64
from odoo import models, fields, _

_logger = logging.getLogger(__name__)

class ImportSOLinesWizard(models.TransientModel):
    _name = 'import.so.lines.wizard'
    _description = 'Import Sale Order Lines Wizard'

    attachment = fields.Binary(string='Attachment', required=True)
    attachment_filename = fields.Char(string='Attachment Filename')

    def generate_template(self):
        template_content = "Product Code,Qty,Unit Price\n"

        attachment_vals = {
            'name': 'import_template.csv',
            'datas': base64.b64encode(template_content.encode('utf-8')),
            'store_fname': 'import_template.csv',
            'res_model': 'import.so.lines.wizard',
            'res_id': self.id,
        }
        attachment = self.env['ir.attachment'].create(attachment_vals)

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'new',
        }

    def import_so_lines(self):
        if not self.attachment:
            return self._display_notification(_('Error'), _('Please select a file for import.'), 'danger')

        if not self._is_valid_file_format():
            return self._display_notification(_('Error'), _('Invalid file format. Please upload .xls, .xlsx, or .csv files.'), 'danger')

        csv_data = base64.b64decode(self.attachment)
        csv_reader = self._read_csv_or_excel(csv_data)

        sale_order = self.env['sale.order'].browse(self._context.get('active_id'))

        if type(csv_reader) is list:
            for row in csv_reader:
                product_code = row.get('Product Code')
                qty = float(row.get('Qty', 0.0))
                unit_price = float(row.get('Unit Price', 0.0))
                
                print

                sale_order_line_vals = {
                    'order_id': sale_order.id,
                    'product_id': self._get_or_create_product(product_code),
                    'product_uom_qty': qty,
                    'price_unit': unit_price,
                }

                self.env['sale.order.line'].create(sale_order_line_vals)
                
            _logger.info("Imported sale order lines from file")
            return self._display_notification(_('Import Successful'), _('Sale order lines imported successfully.'))
            return { 
                'type': 'ir.actions.act_window_close', 
                'params': { 
                    'delay': 4000
                }
            }

    def _get_or_create_product(self, product_code):
        product = self.env['product.product'].search([('default_code', '=', product_code)], limit=1)

        if not product:
            product = self.env['product.product'].create({
                'default_code': product_code,
            })

        return product.id

    def _is_valid_file_format(self):
        allowed_formats = {'xls', 'xlsx', 'csv'}
        file_extension = self._get_file_extension().lower()
        return file_extension in allowed_formats

    def _read_csv_or_excel(self, file_data):
        file_extension = self._get_file_extension().lower()

        if file_extension == 'csv':
            try:
                csv_reader = csv.DictReader(io.StringIO(file_data.decode('utf-8')), delimiter=',')
                return list(csv_reader)
            except csv.Error:
                csv_reader = csv.DictReader(io.StringIO(file_data.decode('utf-8')), delimiter=';')
                return list(csv_reader)
        elif file_extension in {'xls', 'xlsx'}:
            return self._read_excel(file_data)


    def _read_excel(self, file_data):
        xls_data = io.BytesIO(file_data)
        xls_reader = csv.DictReader(io.TextIOWrapper(xls_data, encoding='latin-1'), delimiter='\t')
        try:
            return list(xls_reader)
        except csv.Error as e:
            _logger.error(f"Error reading Excel file: {e}")
            return self._display_notification(_('Error'), _(f'Error reading Excel file: {e}.'), 'danger')

    def _get_file_extension(self):
        return self.attachment_filename.split('.')[-1]

    def _display_notification(self, title, message, notification_type='info'):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'sticky': False,
                'type': notification_type,
                'delay': 0
            }
        }
    
