# stock_traceability_extension/models/stock_picking.py
from odoo import models, fields, api
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_validate(self):
        # Antes de validar el picking de salida, se controla que la cantidad solicitada
        # no supere la disponible según el propietario y la ubicación.
        for move in self.move_lines:
            if self.picking_type_id.code == 'outgoing':
                domain = [
                    ('product_id', '=', move.product_id.id),
                    ('location_id', '=', move.location_id.id),
                    ('owner_id', '=', self.owner_id.id),
                ]
                quant = self.env['stock.quant'].search(domain, limit=1)
                if not quant or move.product_uom_qty > quant.quantity:
                    raise UserError("La cantidad solicitada para el producto '%s' excede la cantidad disponible en la ubicación (%s) para el propietario seleccionado." % (move.product_id.display_name, quant.quantity or 0))
        return super(StockPicking, self).action_validate()
