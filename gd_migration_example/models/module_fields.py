from openerp import models, fields, api, _

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    gn_date = fields.Date(string='gn Date')

    @api.multi
    def my_test_function(self):
        raise Warning("Test")