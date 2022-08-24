from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers import portal


class PayslipPortal(portal.CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        user = request.env.user
        print(user)
        payslips = request.env['hr.employee'].search([('id', '=', user.employee_id.id)])
        print(payslips.payslip_count)
        if 'payslip_count' in counters:
            values['payslip_count'] = payslips.payslip_count
            print('va:', values)
        return values

    # Payslip Table Values
    @http.route(['/my/payslip'], type='http', auth="user", website=True)
    def payslip_records(self):
        user = request.env.user
        print(user)
        payslips = request.env['hr.payslip'].search([('employee_id.user_id', '=', user.id)])
        print('p:', payslips)
        print(self)
        values = {
            'payslips': payslips,
        }
        print(values)
        return request.render("payslip_portal.payslip_portal_template", values)

    # Payslip Report Values
    @http.route(['/print/report'], type='http', auth="user", website=True)
    def payslip_report(self):
        user = request.env.user
        payslip_id = request.env['hr.payslip'].search([('employee_id.user_id', '=', user.id)])
        print(payslip_id)
        value = {
            'payslip': payslip_id
        }
        return request.render("payslip_portal.payslip_report", value)
