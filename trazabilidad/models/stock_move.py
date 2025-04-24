# stock_traceability_extension/models/stock_move.py
from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    # Campo para registrar la fecha en que el producto ingresa a la ubicación
    date_in_location = fields.Datetime(string="Fecha de ingreso en ubicación", readonly=True, copy=False)

    
    
    @api.model
    def create(self, vals):
        # Ejemplo: Para movimientos de entrada se registra la fecha actual
        picking_type = self.env['stock.picking.type'].browse(vals.get('picking_type_id', False))
        if picking_type and picking_type.code in ['incoming', 'internal']:
            vals['date_in_location'] = fields.Datetime.now()
        return super(StockMove, self).create(vals)

    def write(self, vals):
        # Si se actualiza la ubicación, se puede reiniciar la fecha de ingreso
        if 'location_id' in vals:
            vals['date_in_location'] = fields.Datetime.now()
        return super(StockMove, self).write(vals)


