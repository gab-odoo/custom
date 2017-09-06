from openerp import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
#
#    gn_date = fields.Date(string='gn Date', oldname='x_date')
    gn_bool_t = fields.Boolean(string='gn Date', oldname='x_bool_t')

#    gn_date2 = fields.Date(string='gn Date2', oldname='x_date2')
#    gn_product_ids = fields.Many2many('product.product','gn_product_product_res_partner_rel', 'res_partner_id', 'product_product_id', string='Products', oldname='x_product_ids')


#class ProductProduct(models.Model):
#    _inherit = 'product.product'

#    gn_partner_ids = fields.Many2many('res.partner','gn_product_product_res_partner_rel','product_product_id','res_partner_id', string='Partners', oldname='x_partner_ids')