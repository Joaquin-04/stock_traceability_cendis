# stock_traceability_remitos/models/stock_picking.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging

_logger = logging.getLogger(__name__)  # Logger para depuración

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
        """Valida los movimientos considerando el location_id de las líneas.(stock.move.line)"""
        # Validar que en cada línea no se solicite mover una cantidad superior a la disponible.
        _logger.warning("=== Inicio de validación para el picking: %s ===", self.name)
        
        if self.picking_type_code != 'incoming':
            for move in self.move_ids_without_package:
                # Obtener ubicaciones relevantes: quant de move.line o location del move
                locations = move._get_validation_locations_from_quant()
                _logger.warning(
                    "Movimiento ID %s - Ubicaciones validadas: %s",
                    move.id, locations.mapped('display_name')
                )

                # Obtener todos los quants en las ubicaciones
                domain = [
                    ('product_id', '=', move.product_id.id),
                    ('location_id', 'in', locations.ids)
                ]
                if move.picking_id.owner_id:
                    domain.append(('owner_id', '=', move.picking_id.owner_id.id))
                
                quants = self.env['stock.quant'].search(domain)
                available_qty_physical = sum(quants.mapped('inventory_quantity_auto_apply'))  # <--- Cambio clave
                
                _logger.warning(
                    "[CANTIDAD FÍSICA] Producto: %s | En ubicaciones %s: %s",
                    move.product_id.display_name,
                    locations.mapped('display_name'),
                    available_qty_physical
                )

                if move.product_uom_qty > available_qty_physical:
                    raise UserError(
                        "La cantidad a mover (%s) es mayor que la cantidad disponible (%s) para el producto '%s' en la ubicación '%s'."
                        % (move.product_uom_qty, move.available_qty, move.product_id.display_name, self.location_id.name)
                    )
                    
        _logger.warning("=== Validación exitosa para el picking: %s ===", self.name)

        #raise UserError("Veamos el log papa")
        return super(StockPicking, self).button_validate()




