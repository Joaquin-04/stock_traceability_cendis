# stock_traceability_remitos/models/stock_move.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)  # Logger para depuración


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


    def _get_validation_locations_from_quant(self):
        """Obtiene las ubicaciones desde los stock.quant de las líneas.
        
        Reglas:
        - Si las líneas tienen `location_id`.
        - Si no hay `location_id`, usa `self.location_id`.
        """
        locations = self.env['stock.location']
        for line in self.move_line_ids:
            _logger.warning(f"linea {line} Desde: {line.location_id.name}")
            if line.location_id:
                _logger.warning(
                    "Línea ID %s: Quant encontrado en ubicación %s",
                    line.id, line.location_id.display_name
                )
                locations |= line.location_id
        if not locations:
            _logger.warning(
                "Movimiento ID %s: Sin location_id. Usando ubicación de origen: %s",
                self.id, self.location_id.display_name
            )
            locations = self.location_id
        return locations


    