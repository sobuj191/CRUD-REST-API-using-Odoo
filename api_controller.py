from odoo import http
from odoo.http import request, Response
import json


class PartnerAPI(http.Controller):

    @http.route('/api/partners', auth="public", type='http', methods=['GET'], csrf=False)
    def get_partners(self, **kwargs):
        partners = request.env['res.partner'].sudo().search([])
        data = [{'id': rec.id, 'name': rec.name, 'email': rec.email} for rec in partners]
        return Response(json.dumps(data), content_type="application/json", status=200)

    @http.route('/api/partners/<int:partner_id>', auth="public", type='http', methods=['GET'], csrf=False)
    def get_partner(self, partner_id, **kwargs):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner.exists():
            return Response(json.dumps({'error': 'Partner not found'}), content_type="application/json", status=404)
        data = {'id': partner.id, 'name': partner.name, 'email': partner.email}
        return Response(json.dumps(data), content_type="application/json", status=200)


    @http.route('/api/partners', auth="public", type='json', methods=['POST'], csrf=False)
    def create_partner(self, **val):
        data = request.jsonrequest

        if not data.get('name') or not data.get('email'):
            return Response(json.dumps({'error': 'Missing required fields'}),
                            content_type="application/json", status=400)

        partner = request.env['res.partner'].sudo().create({
            'name': data['name'],
            'email': data['email']
        })
        return {'id': partner.id, 'name': partner.name,
                'email': partner.email}

    @http.route('/api/partners/<int:partner_id>', auth="public", type='json', methods=['PUT'], csrf=False)
    def update_partner(self, partner_id):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner.exists():
            return {'error': 'Partner not found'}, 404
        data = request.jsonrequest
        if not data:
            return {'error': 'Invalid JSON request'}, 400
        partner.sudo().write(data)
        return {'message': 'Partner updated successfully', 'updated_data': data}, 200

    @http.route('/api/partners/<int:partner_id>', auth="public", type='http', methods=['DELETE'], csrf=False)
    def delete_partner(self, partner_id, **kwargs):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner.exists():
            return Response(json.dumps({'error': 'Partner not found'}), content_type="application/json", status=404)

        partner.unlink()
        return Response(json.dumps({'message': 'Partner deleted successfully'}), content_type="application/json",
                        status=200)
