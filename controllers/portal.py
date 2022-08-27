# -*- coding: utf-8 -*-
from odoo import http, SUPERUSER_ID
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class PayslipPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'payslip_count' in counters:
            payslip_count = request.env['hr.payslip'].search_count(
                self._get_payslips_domain()) if request.env[
                'hr.payslip'].check_access_rights(
                'read', raise_exception=False) else 0
            values['payslip_count'] = payslip_count
        return values

    # checking domain: user & payslips_state
    def _get_payslips_domain(self):
        return [('employee_id.user_id', '=', request.uid),
                ('state', 'in', ('verify', 'done', 'cancel'))]

    @http.route(['/my/payslips'], type='http', auth="user", website=True)
    def portal_my_payslips(self):
        user = request.env.user
        domain = self._get_payslips_domain()
        payslips = request.env['hr.payslip'].search(domain)
        values = {
            'payslips': payslips,
            'page_name': 'payslip',
        }
        return request.render("website_employee_payslip.portal_my_payslips",
                              values)

    @http.route(['/print/report/<int:payslip_id>'], type='http', auth="user",
                website=True)
    def payslip_report(self, payslip_id):
        payslip = request.env['hr.payslip'].search(
            [('employee_id.user_id', '=', request.env.user.id),
             ('state', 'in', ('verify', 'done')),
             ('id', '=', payslip_id)])
        value = {
            'payslip': payslip
        }
        pdf = request.env.ref(
            'website_employee_payslip.report_payslip').with_context(
            value)._render_qweb_pdf([payslip])[0]
        pdfhttpheaders = [('Content-Type', 'application/pdf'),
                          ('Content-Length', len(pdf)),
                          ]
        return request.make_response(pdf, headers=pdfhttpheaders)
