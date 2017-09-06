from openerp import SUPERUSER_ID
from openerp.modules.registry import RegistryManager

def migrate(cr, installed_version):
    """Migrate :: copy x_date field content to gn_date"""
    #import pdb
    #pdb.set_trace()
    update_query = """
                UPDATE res_partner
                SET gn_date = x_date
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