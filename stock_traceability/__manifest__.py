# stock_traceability/__manifest__.py
{
    'name': 'Stock Traceability Dynamic',
    'version': '1.0',
    'summary': 'Búsqueda dinámica de productos en stock por almacén, ubicación y propietario',
    'description': """
        Este módulo permite, mediante un wizard, filtrar y agrupar los productos que 
        hay en stock según el almacén, la ubicación y el propietario especificado. 
        Se basa en una búsqueda dinámica en stock.quant sin duplicar información.
    """,
    'author': 'Tu Empresa',
    'category': 'Inventory',
    'website': 'https://tuempresa.com',
    'license': 'LGPL-3',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_traceability_wizard_views.xml',
    ],
    'installable': True,
    'application': True,
}
