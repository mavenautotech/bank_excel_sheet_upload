# -*- coding: utf-8 -*-
{
    'name': " Excel Upload",
    'summary': "Download XLSX files from the bank detail sheet download files.",
    'description': """
    Benificiary bank detail XLSX Download.
    """,
    'author': "Maven",
    'website': "https://mavenautotech.com/",
    'category': 'Transportation',
    'version': '16',
    'depends': ['base', 'web'],
    'license': 'LGPL-3',
    'data': [
        "data/seq.xml",
        'security/ir.model.access.csv',
        'views/bank_detail_view.xml',
        'views/import_data_view1.xml',

    ],
    'post_init_hook': '_update_date_format',

}
