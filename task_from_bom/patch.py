from openerp.osv import osv


class procurement_order(osv.osv):
    _name = "procurement.order"
    _inherit = "procurement.order"

    def _run(self, cr, uid, procurement, context=None):
        if self._is_procurement_task(cr, uid, procurement, context=context) and not procurement.task_id:
            # If the SO was confirmed, cancelled, set to draft then confirmed, avoid creating a new
            # task.
            if procurement.sale_line_id:
                #get the product for each existing task linked to this SO-Line, don't recreate a task if there is already a so-line procurement linked to this product.
                existing_task = self.pool['project.task'].search(
                    cr, uid, [('sale_line_id', '=', procurement.sale_line_id.id)],
                    context=context
                )
                task_products = [task.procurement_id.product_id for task in self.pool['project.task'].browse(cr, uid, existing_task, context=context)]

                if procurement.product_id in task_products:
                    return existing_task

            # create a task for the procurement
            return self._create_service_task(cr, uid, procurement, context=context)
        return super(procurement_order, self)._run(cr, uid, procurement, context=context)