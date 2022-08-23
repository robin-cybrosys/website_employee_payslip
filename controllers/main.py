from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):
    @http.route(['/appointment'], type='http', auth="public", website=True)
    def appointment(self):
        patient_card = request.env['hospital.management'].sudo().search([])
        doctor_id = request.env['hr.employee'].sudo().search(
            [('job_id', '=', 'Doctor')])
        values = {}
        values.update({
            'patients': patient_card,
            'doctors': doctor_id
        })
        print(values,"valll")
        return request.render(
            "website_hospital_appointment.online_appointment_form", values)

    @http.route(['/appointment/submit'], type='http', auth='public',
                website=True)
    def appointment_submit(self, **post):
        patient = int(post['patient_id'])
        doctor = int(post['doctor_id'])
        date = post.get('appointment_date')
        print(patient, doctor, date)
        appointments = request.env['hospital.appointment'].sudo().search([])
        appointments.create({
            'patient_card_id': patient,
            'date': date,
            'doctor_id': doctor,
        })
        vals = {
            'appointments': appointments,
        }
        return request.render(
            "website_hospital_appointment.appointment_creation_success", vals)

    # create patient card if it's not existing
    @http.route(['/appointment/card/create'], type='http', auth='public',
                website=True)
    def create_card(self):
        patient = request.env['res.partner'].sudo().search([])
        values = {}
        values.update({
            'patients': patient
        })
        return request.render(
            "website_hospital_appointment.card_creation_form", values)

    # card submit button
    @http.route(['/appointment/card/submit'], type='http', auth='public',
                website=True)
    def appointment_card_submit(self, **post):
        patient_card = int(post['partner_id'])
        dob = str(post.get('date_of_birth'))
        email = post.get('email')
        phone = post.get('phone')
        card = request.env['hospital.management'].sudo().search([])
        card.create({
            'patient_id': patient_card,
            'dob': dob,
            'email': email,
            'patient_phone': phone,
        })
        vals = {
            'card': card,
        }
        return request.render(
            "website_hospital_appointment.card_creation_success",
            vals)
