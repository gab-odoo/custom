import time
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp.tools import float_is_zero
import openerp.addons.decimal_precision as dp
from openerp.tools import float_compare
from openerp.tools.translate import _

class account_asset_asset(osv.osv):
    _inherit = 'account.asset.asset'

    def _compute_board_amount(self, cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=None):
        #by default amount = 0
        amount = 0
        if i == undone_dotation_number:
            amount = residual_amount
        else:
            if asset.method == 'linear':
                amount = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
                if asset.prorata:
                    amount = amount_to_depr / asset.method_number
                    if i == 1:
                        purchase_date = datetime.strptime(asset.purchase_date, '%Y-%m-%d')
                        if asset.method_period % 12 != 0:
                            # Calculate depreciation for remaining days in the month
                            # Example: asset value of 120, monthly depreciation, 12 depreciations
                            #    (120 (Asset value)/ (12 (Number of Depreciations) * 1 (Period Length))) /  31 (days of month) * 12 (days to depreciate in purchase month)
                            month_days = calendar.monthrange(purchase_date.year, purchase_date.month)[1]
                            days = month_days - purchase_date.day + 1
                            amount = (amount_to_depr / (asset.method_number * asset.method_period)) / month_days * days
                        else:
                            # Calculate depreciation for remaining days in the year
                            # Example: asset value of 120, yearly depreciation, 12 depreciations
                            #    (120 (Asset value)/ (12 (Number of Depreciations) * 1 (Period Length, in years))) /  365 (days of year) * 75 (days to depreciate in purchase year)
                            fy = self.pool.get('account.fiscalyear').find(cr, uid, dt=depreciation_date,
                                                                          context=context)
                            fy_date_end = datetime.strptime(
                                self.pool.get('account.fiscalyear').browse(cr, uid, fy, context=context).date_stop,
                                '%Y-%m-%d')
                            year_days = 366 if purchase_date.year % 4 == 0 else 365
                            days = (fy_date_end - depreciation_date).total_seconds() / 3600 / 24 + 1
                            amount = (amount_to_depr / (asset.method_number * (asset.method_period / 12))) / year_days * days
            elif asset.method == 'degressive':
                amount = residual_amount * asset.method_progress_factor
                if asset.prorata:
                    if i == 1:
                        purchase_date = datetime.strptime(asset.purchase_date, '%Y-%m-%d')
                        if asset.method_period % 12 != 0:
                            month_days = calendar.monthrange(purchase_date.year, purchase_date.month)[1]
                            days = month_days - purchase_date.day + 1
                            amount = (residual_amount * asset.method_progress_factor) / month_days * days
                        else:
                            year_days = 366 if purchase_date.year % 4 == 0 else 365
                            days = year_days - float(depreciation_date.strftime('%j')) + 1
                            amount = (residual_amount * asset.method_progress_factor * (asset.method_period / 12)) / year_days * days
        return amount

    def compute_depreciation_board(self, cr, uid, ids, context=None):
        depreciation_lin_obj = self.pool.get('account.asset.depreciation.line')
        currency_obj = self.pool.get('res.currency')
        for asset in self.browse(cr, uid, ids, context=context):
            if asset.value_residual == 0.0:
                continue
            posted_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_check', '=', True)],order='depreciation_date desc')
            old_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_id', '=', False)])
            if old_depreciation_line_ids:
                depreciation_lin_obj.unlink(cr, uid, old_depreciation_line_ids, context=context)

            amount_to_depr = residual_amount = asset.value_residual
            if asset.prorata:
                depreciation_date = datetime.strptime(self._get_last_depreciation_date(cr, uid, [asset.id], context)[asset.id], '%Y-%m-%d')
            else:
                # depreciation_date = 1st January of purchase year
                purchase_date = datetime.strptime(asset.purchase_date, '%Y-%m-%d')
                #if we already have some previous validated entries, starting date isn't 1st January but last entry + method period
                if (len(posted_depreciation_line_ids)>0):
                    last_depreciation_date = datetime.strptime(depreciation_lin_obj.browse(cr,uid,posted_depreciation_line_ids[0],context=context).depreciation_date, '%Y-%m-%d')
                    depreciation_date = (last_depreciation_date+relativedelta(months=+asset.method_period))
                else:
                    depreciation_date = datetime(purchase_date.year, 1, 1)
            day = depreciation_date.day
            month = depreciation_date.month
            year = depreciation_date.year
            total_days = (year % 4) and 365 or 366

            precision_digits = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
            undone_dotation_number = self._compute_board_undone_dotation_nb(cr, uid, asset, depreciation_date, total_days, context=context)
            for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                i = x + 1
                amount = self._compute_board_amount(cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=context)
                if float_is_zero(amount, precision_digits=precision_digits):
                    continue
                residual_amount -= amount
                if asset.prorata:
                    if depreciation_date != datetime.strptime(asset.purchase_date,'%Y-%m-%d'):
                        try:
                            fy = self.pool.get('account.fiscalyear').find(cr, uid, dt=depreciation_date, context=context)
                            depreciation_date = datetime.strptime(
                                self.pool.get('account.fiscalyear').browse(cr, uid, fy, context=context).date_start,'%Y-%m-%d')
                            day = depreciation_date.day
                            month = depreciation_date.month
                            year = depreciation_date.year
                        except:
                            pass
                vals = {
                     'amount': amount,
                     'asset_id': asset.id,
                     'sequence': i,
                     'name': str(asset.id) +'/' + str(i),
                     'remaining_value': residual_amount,
                     'depreciated_value': (asset.purchase_value - asset.salvage_value) - (residual_amount + amount),
                     'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                }
                depreciation_lin_obj.create(cr, uid, vals, context=context)
                # Considering Depr. Period as months
                depreciation_date = (datetime(year, month, day) + relativedelta(months=+asset.method_period))
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year
        return True