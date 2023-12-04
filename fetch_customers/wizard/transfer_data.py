from odoo import models, fields, http
import xmlrpc.client


class DatabaseConnectionWizard(models.TransientModel):
    _name = 'database.connection.wizard'
    _description = 'Database Connection Wizard'

    def _get_current_url_path(self):
        base_url = http.request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        return base_url.split('//')[0]+ \
            base_url.split(':')[1]+':'

    source_url = fields.Char(string='Source Odoo URL', required=True,
                             default=_get_current_url_path)
    source_db = fields.Char(string='Source Database Name', required=True)
    source_username = fields.Char(string='Source Username', required=True)
    source_password = fields.Char(string='Source Password', required=True)

    def _get_current_url(self):
        base_url = http.request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        return base_url

    target_url = fields.Char(string='Target Odoo URL',
                             default=lambda self: self._get_current_url(),
                             required=True)
    target_db = fields.Char(string='Target Database Name', required=True)
    target_username = fields.Char(string='Target Username', required=True)
    target_password = fields.Char(string='Target Password', required=True)

    def connect_databases(self):
        source_url = self.source_url
        source_db = self.source_db
        source_username = self.source_username
        source_password = self.source_password

        target_url = self.target_url
        target_db = self.target_db
        target_username = self.target_username
        target_password = self.target_password

        try:
            source_common = xmlrpc.client.ServerProxy(
                f'{source_url}/xmlrpc/2/common')
            source_models = xmlrpc.client.ServerProxy(
                f'{source_url}/xmlrpc/2/object')
            source_uid = source_common.authenticate(source_db, source_username,
                                                    source_password, {})

            target_common = xmlrpc.client.ServerProxy(
                f'{target_url}/xmlrpc/2/common')
            target_models = xmlrpc.client.ServerProxy(
                f'{target_url}/xmlrpc/2/object')
            target_uid = target_common.authenticate(target_db, target_username,
                                                    target_password, {})

            transferred_record_ids = set()

            db_1_partners = source_models.execute_kw(
                source_db, source_uid, source_password, 'res.partner',
                'search_read',
                [[]],
                {
                    'fields': [
                        'name', 'function', 'phone', 'mobile', 'email',
                        'website',
                        'title',
                        'lang', 'category_id', 'street', 'street2', 'zip',
                        'city',
                        'country_id',
                        'state_id', 'image_128', 'avatar_128'
                    ],
                    'context': {'lang': 'en_US'}
                }
            )

            for partner in db_1_partners:
                domain = [
                    '|',
                    '|',
                    ('name', '=', partner['name']),
                    ('email', '=', partner['email']),
                    ('phone', '=', partner['phone'])
                ]

                existing_records = target_models.execute_kw(
                    target_db, target_uid, target_password, 'res.partner',
                    'search_read',
                    [domain],
                    {'fields': ['id']}
                )

                if not existing_records and partner[
                                            'id'] not in transferred_record_ids:
                    new_partner = {
                        'name': partner['name'],
                        'function': partner['function'],
                        'phone': partner['phone'],
                        'mobile': partner['mobile'],
                        'email': partner['email'],
                        'website': partner['website'],
                        'title': partner['title'],
                        'lang': partner['lang'],
                        'street': partner['street'],
                        'street2': partner['street2'],
                        'zip': partner['zip'],
                        'city': partner['city'],
                        'country_id': partner['country_id'][0] if partner[
                            'country_id'] else False,
                        'state_id': partner['state_id'][0] if partner[
                            'state_id'] else False,
                        'image_128': partner['image_128'],
                        'avatar_128': partner['avatar_128'],
                    }

                    try:
                        target_models.execute_kw(target_db, target_uid,
                                                 target_password, 'res.partner',
                                                 'create',
                                                 [new_partner])
                        transferred_record_ids.add(partner['id'])
                    except Exception as e:
                        with open('error_log.txt', 'a') as log_file:
                            log_file.write(
                                f"Error transferring record {partner['id']}: {e}\n")

            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        except Exception as e:
            raise models.UserError(f'Error connecting to databases: {e}')
