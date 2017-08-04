from odoo import api, fields, models, _

class MovementType(models.Model):
    _name = "account.move.type"

    name = fields.Char(string='Movement Type')
    user_type_ids = fields.Many2many('account.account.type', string='User Type')
    set = fields.Char(string='Variation-Detail Set')
    code = fields.Char(string='Code')

class AccountMove(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    movement_type_id = fields.Many2one('account.move.type', string='Movement Type')
    set = fields.Char(related='movement_type_id.set', string='Variation-Detail Set')
    code = fields.Char(related='movement_type_id.code', string='Code')

class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    user_type_id = fields.Many2one(related='account_id.user_type_id')
    movement_type_id = fields.Many2one('account.move.type', string='Movement Type', domain="[('user_type_ids','in',user_type_id)]")
    set = fields.Char(related='movement_type_id.set', string='Variation-Detail Set')
    code = fields.Char(related='movement_type_id.code', string='Code')
