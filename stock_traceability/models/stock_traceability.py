# stock_traceability/models/stock_traceability.py
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockTraceabilityWizard(models.TransientModel):
    _name = 'stock.traceability.wizard'
    _description = 'Wizard de trazabilidad dinámica de stock'

    warehouse_id = fields.Many2one('stock.warehouse', string='Almacén', required=True)
    location_id = fields.Many2one('stock.location', string='Ubicación', required=True)
    owner_id = fields.Many2one(
        'res.partner', 
        string='Propietario', 
        domain="[('x_studio_propietario', '=', True)]", 
        required=True
    )

    # Este campo mostrará las líneas con los productos y la cantidad agregada
    stock_line_ids = fields.One2many(
        'stock.traceability.wizard.line', 
        'wizard_id', 
        string="Productos Disponibles", 
        readonly=True
    )

    def action_search_stock(self):
        _logger.warning(f"*"*100)
        _logger.warning(f"action_search_stock ")
        StockQuant = self.env['stock.quant']
        # Construir el dominio basado en la ubicación y el propietario
        domain = [
            ('location_id', '=', self.location_id.id),
            ('owner_id', '=', self.owner_id.id),
        ]
        # Agrupar por producto. En caso de requerir usar también el lote, se puede agregar al grupo.
        grouping = ['product_id']
        # Obtenemos la suma de las cantidades agrupada por producto
        result = StockQuant.read_group(domain, ['quantity:sum'], grouping)

        _logger.warning(f" result: {result} ")
        # Eliminar líneas existentes en el wizard (si hubiera)
        self.stock_line_ids.unlink()
        lines = []
        for data in result:
            # data['product_id'] es una tupla (id, nombre)
            product_id = data.get('product_id')[0] if data.get('product_id') else False
            _logger.warning(f" product_id: {product_id} ")
            qty = data.get('quantity')
            _logger.warning(f" qty: {qty} ")
            if qty>=0:
                lines.append({
                    'wizard_id': self.id,
                    'product_id': product_id,
                    'available_qty': qty,
                })
                _logger.warning(f" lines: {lines} ")
        # Crear registros en el One2many
        self.stock_line_ids = [(0, 0, line) for line in lines]
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.traceability.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

class StockTraceabilityWizardLine(models.TransientModel):
    _name = 'stock.traceability.wizard.line'
    _description = 'Línea del wizard de trazabilidad'

    wizard_id = fields.Many2one('stock.traceability.wizard', string='Wizard', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Producto', required=True)
    available_qty = fields.Float(string='Cantidad Disponible', required=True)
