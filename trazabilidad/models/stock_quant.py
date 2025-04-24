# stock_traceability_extension/models/stock_quant.py
from odoo import models, fields, api
from datetime import datetime

class StockQuant(models.Model):
    _inherit = "stock.quant"

    # Campo almacenado: días que lleva en la ubicación
    days_in_location = fields.Integer(string="Días en Ubicación", compute="_compute_days_in_location", store=True)
    
    # Se utiliza el mismo campo 'date_in_location' que se propaga desde stock.move
    date_in_location = fields.Datetime(string="Fecha de ingreso", readonly=True, copy=False)

    @api.depends('date_in_location')
    def _compute_days_in_location(self):
        current_datetime = fields.Datetime.now()
        for quant in self:
            if quant.date_in_location:
                diff = (fields.Datetime.from_string(current_datetime) - fields.Datetime.from_string(quant.date_in_location)).days
                quant.days_in_location = diff
            else:
                quant.days_in_location = 0

