# stock_traceability_extension/models/stock_traceability_wizard.py
from odoo import models, fields, api

class StockTraceabilityWizard(models.TransientModel):
    _name = "stock.traceability.wizard"
    _description = "Wizard para filtrar stock por almacén, ubicación y propietario"

    warehouse_id = fields.Many2one('stock.warehouse', string="Almacén", required=True)
    location_id = fields.Many2one('stock.location', string="Ubicación", required=True)
    owner_id = fields.Many2one('res.partner', string="Propietario", required=True)

    stock_line_ids = fields.One2many('stock.traceability.wizard.line', 'wizard_id', string="Productos disponibles", readonly=True)

    def action_search_stock(self):
        StockQuant = self.env['stock.quant']
        domain = [
            ('location_id', '=', self.location_id.id),
            ('owner_id', '=', self.owner_id.id),
        ]
        quants = StockQuant.search(domain)
        lines = []
        for quant in quants:
            lines.append((0, 0, {
                'product_id': quant.product_id.id,
                'available_qty': quant.quantity,
                'days_in_location': quant.days_in_location,
            }))
        self.stock_line_ids = lines
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.traceability.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def action_confirm_extraction(self):
        # Aquí se programaría la lógica para crear movimientos de salida (o actualizar un picking)
        # con base en la selección. Por ejemplo, podrías asignar estas líneas a un picking ya creado.
        return {'type': 'ir.actions.act_window_close'}

class StockTraceabilityWizardLine(models.TransientModel):
    _name = "stock.traceability.wizard.line"
    _description = "Línea de productos disponibles en el wizard de trazabilidad"

    wizard_id = fields.Many2one('stock.traceability.wizard', string="Wizard")
    product_id = fields.Many2one('product.product', string="Producto")
    available_qty = fields.Float(string="Cantidad Disponible")
    days_in_location = fields.Integer(string="Días en Ubicación")
