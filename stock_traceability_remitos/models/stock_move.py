# stock_traceability_remitos/models/stock_move.py
from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    # Campo computado: Cantidad disponible del producto en la ubicación del remito
    available_qty = fields.Float(
        string="Cantidad Disponible", 
        compute="_compute_available_qty", 
        help="Cantidad calculada a partir de los registros en stock.quant según la ubicación y, si aplica, el propietario."
    )
    # Campo computed, obtenido del remito donde se encuentra la línea
    allowed_product_ids = fields.Many2many(
        'product.product',
        string="Productos Permitidos",
        compute="_compute_allowed_product_ids"
    )

    @api.depends('picking_id.allowed_product_ids')
    def _compute_allowed_product_ids(self):
        for move in self:
            move.allowed_product_ids = move.picking_id.allowed_product_ids

    @api.depends('product_id', 'picking_id.location_id', 'picking_id.owner_id')
    def _compute_available_qty(self):
        for move in self:
            domain = [('product_id', '=', move.product_id.id),
                      ('location_id', '=', move.picking_id.location_id.id)]
            if move.picking_id.owner_id:
                domain.append(('owner_id', '=', move.picking_id.owner_id.id))
            # Utilizamos read_group para sumar las cantidades en stock.quant
            result = self.env['stock.quant'].read_group(domain, ['quantity'], [])
            move.available_qty = result[0]['quantity'] if result else 0

    