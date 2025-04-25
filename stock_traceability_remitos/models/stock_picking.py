# stock_traceability_remitos/models/stock_picking.py
from odoo import models, fields, api
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Campo computado: Productos permitidos en base a la ubicación de origen y el propietario (si se define)
    allowed_product_ids = fields.Many2many(
        'product.product',
        string="Productos Permitidos",
        compute="_compute_allowed_product_ids"
    )

    @api.depends('location_id', 'owner_id')
    def _compute_allowed_product_ids(self):
        for picking in self:
            domain = [('location_id', '=', picking.location_id.id)]
            if picking.owner_id:
                domain.append(('owner_id', '=', picking.owner_id.id))
            # Se consulta el modelo stock.quant y se extrae el listado de productos
            quants = self.env['stock.quant'].search(domain)
            picking.allowed_product_ids = quants.mapped('product_id')

    def button_validate(self):
        # Validar que en cada línea no se solicite mover una cantidad superior a la disponible.
        for move in self.move_ids_without_package:
            if move.product_uom_qty > move.available_qty:
                raise UserError(
                    "La cantidad a mover (%s) es mayor que la cantidad disponible (%s) para el producto '%s' en la ubicación '%s'."
                    % (move.product_uom_qty, move.available_qty, move.product_id.display_name, self.location_id.name)
                )
        return super(StockPicking, self).button_validate()
