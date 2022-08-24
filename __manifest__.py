# -*- coding: utf-8 -*-
{
    'name': "Website Employee Payslip",
    'application': "True",
    'author': "R",
    'website': "http://www.cybrosys.com",
    'sequence': "-1",
    'licence': "LGPL-3",
    'category': 'Uncategorized',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website', 'hr', 'hr_payroll_community'],

    # always loaded
    'data': [
        'views/employee_portal_template.xml',
        'views/report_payslip_templates.xml',
        # 'views/appointments_page.xml',
        # 'views/appointments_webpage_template.xml',
    ],
}
