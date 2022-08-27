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
    'depends': ['base', 'website', 'hr', 'hr_payroll_community'],
    'data': [
        'views/report_payslip_templates.xml',
        'views/employee_portal_template.xml',
        # 'views/test.xml',
        # 'views/appointments_webpage_template.xml',
    ],
}
