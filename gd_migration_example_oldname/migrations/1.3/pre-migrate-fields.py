from openerp import SUPERUSER_ID
from openerp.modules.registry import RegistryManager

def migrate(cr, installed_version):
    """Migrate :: rename relation table"""
    #import pdb
    #pdb.set_trace()
    update_query = """
                ALTER TABLE x_product_product_res_partner_rel
                RENAME TO gn_product_product_res_partner_rel;
            """ % ()
    cr.execute(update_query)


    #Other example: this is to uninstall the module with the name "module_name" at module installation

    #registry = RegistryManager.get(cr.dbname)
    #modobj = registry['ir.module.module']
    #module_ids = modobj.search(cr, SUPERUSER_ID, [
    #    ('name', 'in', [
    #        '*module_name*',
    #    ])
    #])
    #if module_ids:
    #    modobj.module_uninstall(cr, SUPERUSER_ID, module_ids)