from openerp import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _name = "account.analytic.line"
    _inherit = "account.analytic.line"

    def _get_sale_order_line(self, vals=None):
        result = dict(vals or {})
        so_line = result.get('so_line', False) or self.so_line
        if not so_line and self.account_id and self.product_id and self.product_id.invoice_policy in ('cost', 'order') and self.product_id.track_service != 'task':
            so_lines = self.env['sale.order.line'].search([
                ('order_id.project_id', '=', self.account_id.id),
                ('state', '=', 'sale'),
                ('product_id', '=', self.product_id.id)])
            # Use the existing SO line only if the unit prices are the same, otherwise we create
            # a new line
            for line in so_lines:
                if line.product_id.invoice_policy != 'cost' or (line.product_id.invoice_policy == 'cost' and line.price_unit == self._get_invoice_price(line.order_id)):
                    result.update({'so_line': line.id})
                    so_line = line
                    break

            else:
                # This will trigger the creation of a new SO line
                so_line = False

        if not so_line and self.account_id and self.product_id and self.product_id.invoice_policy == 'cost':
            order_line_vals = self._get_sale_order_line_vals()
            if order_line_vals:
                so_line = self.env['sale.order.line'].create(order_line_vals)
                so_line._compute_tax_id()
                result.update({'so_line': so_line.id})

        return result