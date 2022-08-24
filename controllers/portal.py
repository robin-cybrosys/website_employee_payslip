# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request


class PortalPayslip(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'payslip_count' in counters:
            payslip_count = request.env['hr.payslip'].search_count(
                self._get_payslips_domain()) if request.env[
                'hr.payslip'].check_access_rights(
                'read', raise_exception=False) else 0
            values['payslip_count'] = payslip_count
        return values

    # ------------------------------------------------------------
    # Payslips
    # ------------------------------------------------------------

    # checking user & payslips
    def _get_payslips_domain(self):
        return [('employee_id.user_id', '=', request.uid),
                ('state', 'in', ('verify', 'done'))]

    def _invoice_get_page_view_values(self, payslip, access_token, **kwargs):
        values = {
            'page_name': 'payslip',
            'payslip': payslip,
        }
        return self._get_page_view_values(payslip, access_token, values,
                                          'my_invoices_history', False,
                                          **kwargs)

    @http.route(['/my/payslips', '/my/payslips/page/<int:page>'], type='http',
                auth="user", website=True)
    def portal_my_invoices(self, date_begin=None):
        values = self._prepare_portal_layout_values()
        hr_payslip = request.env['hr.payslip']

        domain = self._get_payslips_domain()
        # content according to pager and archive selected
        payslips = hr_payslip.search(domain, limit=self._items_per_page)
        # request.session['my_payroll_history'] = payslips.ids[:100]

        values.update({
            'date': date_begin,
            'payslips': payslips,
            'page_name': 'payslip',
            'default_url': '/my/payslips',
        })
        return request.render("website_employee_payslip.portal_my_payslips",
                              values)

    @http.route(['/print/report'], type='http', auth="user", website=True)
    def payslip_report(self):
        user = request.env.user
        payslip_id = request.env['hr.payslip'].search(
            [('employee_id.user_id', '=', user.id)])
        print(payslip_id)
        value = {
            'payslip': payslip_id
        }
        return request.render("website_employee_payslip.report_payslip", value)

    # @http.route(['/my/payslips/<int:invoice_id>'], type='http', auth="public",
    #             website=True)
    # def portal_my_invoice_detail(self, invoice_id, access_token=None,
    #                              report_type=None, download=False, **kw):
    #     try:
    #         invoice_sudo = self._document_check_access('hr.payslip', invoice_id,
    #                                                    access_token)
    #     except (AccessError, MissingError):
    #         return request.redirect('/my')
    #
    #     if report_type in ('html', 'pdf', 'text'):
    #         return self._show_report(model=invoice_sudo,
    #                                  report_type=report_type,
    #                                  report_ref='account.account_invoices',
    #                                  download=download)
    #
    #     values = self._invoice_get_page_view_values(invoice_sudo, access_token,
    #                                                 **kw)
    #     return request.render("account.portal_invoice_page", values)

    # ------------------------------------------------------------
    # My Home
    # ------------------------------------------------------------

    # def details_form_validate(self, data):
    #     error, error_message = super(PortalAccount, self).details_form_validate(
    #         data)
    #     # prevent VAT/name change if payslips exist
    #     partner = request.env['res.users'].browse(request.uid).partner_id
    #     if not partner.can_edit_vat():
    #         if 'vat' in data and (data['vat'] or False) != (
    #                 partner.vat or False):
    #             error['vat'] = 'error'
    #             error_message.append(
    #                 _('Changing VAT number is not allowed once payslips have been issued for your account. Please contact us directly for this operation.'))
    #         if 'name' in data and (data['name'] or False) != (
    #                 partner.name or False):
    #             error['name'] = 'error'
    #             error_message.append(
    #                 _('Changing your name is not allowed once payslips have been issued for your account. Please contact us directly for this operation.'))
    #         if 'company_name' in data and (data['company_name'] or False) != (
    #                 partner.company_name or False):
    #             error['company_name'] = 'error'
    #             error_message.append(
    #                 _('Changing your company name is not allowed once payslips have been issued for your account. Please contact us directly for this operation.'))
    #     return error, error_message
