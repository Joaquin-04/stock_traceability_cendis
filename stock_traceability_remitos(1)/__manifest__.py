# stock_traceability_remitos/__manifest__.py
{
    "name": "Stock Traceability Remitos",
    "version": "1.0",
    "summary": "Restringe la entrega/movimiento de productos en remitos basados en ubicación y propietario.",
    "description": """
        Este módulo extiende la funcionalidad de los remitos (pickings) para:
         - Restringir la entrega o movimiento de productos a la cantidad disponible
           en la ubicación (location_id) del remito.
         - Permitir que las líneas de picking muestren solo los productos disponibles en la ubicación,
           filtrando por propietario si se selecciona (campo owner_id en el remito).
         - Agregar en cada línea un campo 'Cantidad Disponible' que se calcula dinámicamente
           consultando stock.quant mediante read_group, sin duplicar información.
        La solución está diseñada para que funcione en remitos internos, de salida y, a futuro,
        en el módulo de código de barras.
    """,
    "author": "Tu Empresa",
    "category": "Inventory",
    "website": "https://tuempresa.com",
    "license": "LGPL-3",
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
        #"views/stock_picking_views.xml",
    ],
    "installable": True,
    "application": False,
}
