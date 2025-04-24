# stock_traceability_extension/__manifest__.py
{
    'name': 'Stock Traceability Extension',
    'version': '1.1',
    'summary': 'Extensión para mayor trazabilidad en inventarios por propietario, ubicación y almacén',
    'description': """
        Este módulo extiende la funcionalidad de Odoo 17 para agregar trazabilidad completa:
        
        - Registro de la fecha de ingreso de cada producto a una ubicación.
        - Cálculo de los días que lleva un producto en la ubicación.
        - Reportes e historial de ingresos y salidas por propietario y ubicación.
        - Restricción en los pickings para extraer solo productos disponibles según almacén, ubicación y propietario.
        - Wizard para facilitar la extracción de productos.
    """,
    'author': 'Tu Empresa',
    'category': 'Inventory',
    'website': 'https://tuempresa.com',
    'license': 'LGPL-3',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_traceability_views.xml',
        'views/stock_traceability_wizard_views.xml',
        # 'data/stock_traceability_demo.xml',  # Descomentar si se requieren datos demo
    ],
    'installable': True,
    'application': True,
}
