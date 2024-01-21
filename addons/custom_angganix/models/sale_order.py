from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    request_vendor = fields.Many2one('res.partner', string='Request Vendor', help='Vendor for the purchase order')
    no_kontrak = fields.Char(string='No Kontrak', help='Contract number for the purchase order')
    with_po = fields.Boolean(string='With PO', help='Check if linked with purchase order')
    purchase_orders = fields.One2many('purchase.order', 'sale_order_id', string='Purchase Orders')
    
    def create_sales_po(self):
        sale_order = self
        request_vendor = sale_order.request_vendor
        no_kontrak = sale_order.no_kontrak
        
        po_vals = {
            'partner_id': request_vendor.id,
            'origin': sale_order.name,
            'sale_order_id': sale_order.id,
            'partner_ref': no_kontrak
        }
        
        new_po = self.env["purchase.order"].create(po_vals)
        
        for sale_order_line in sale_order.order_line:
            po_line_vals = {
                'order_id': new_po.id,
                'product_id': sale_order_line.product_id.id,
                'name': sale_order_line.name,
                'product_qty': sale_order_line.product_uom_qty,
                'product_uom': sale_order_line.product_uom.id,
                'price_unit': sale_order_line.price_unit
            }
            
            self.env["purchase.order.line"].create(po_line_vals)
        
        sale_order.write({'with_po': True})
        
        return {
            'name': 'Purchase Order',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'res_id': new_po.id,
            'view_mode': 'form',
            'view_id': self.env.ref('purchase.purchase_order_form').id,
            'view_type': 'form',
            'target': 'current'
        }
        
    def action_confirm(self):
        for order in self:
            print(f"Checking No Kontrak: {order.no_kontrak}")
            if order.no_kontrak:
                existing_order = self.search([('no_kontrak', '=', order.no_kontrak), ('id', '!=', order.id)])
                if existing_order:
                    raise ValidationError('No Kontrak sudah pernah diinputkan sebelumnya...!')
        return super().action_confirm()

    def import_so_lines(self):
        wizard = self.env['import.so.lines.wizard'].create({})
        return {
            'name': 'Import Sale Order Lines',
            'type': 'ir.actions.act_window',
            'res_model': 'import.so.lines.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'view_id': self.env.ref('custom_angganix.import_so_lines_wizard_form_view').id,
            'view_type': 'form',
            'target': 'new',
        }


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
        
