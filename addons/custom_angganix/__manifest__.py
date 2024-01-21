{
    'name': 'Custom Angganix',
    'description': 'Menghubungkan module Sale dan Purchase',
    'version': '1.0',
    'author': 'Angga NIX',
    'category': 'Integration',
    'depends': ['base', 'sale', 'purchase'],
    'data': [
        'views/sales_order_form.xml',
        'views/import_so_lines_wizard.xml',
        'data/data.xml'
    ],
    'assets': {
        'web.assets_common': [
            'custom_angganix/static/src/js/get_import_template.js'
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True
}
