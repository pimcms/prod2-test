from netforce.model import Model, fields, get_model
from netforce import access
import time


class Settings(Model):
    _name = "shopee.settings"
    _fields = {
        "default_uom_id": fields.Many2One("uom","Default UoM"),
        "order_auto_copy_to_sale": fields.Boolean("Auto Copy Shopee Order to Sale Order when Syncing"),
        "order_auto_copy_to_picking": fields.Boolean("Auto Copy Shopee Order to Goods Issue when Syncing"),
        "order_auto_complete_picking": fields.Boolean("Auto Complete Goods Issue when Syncing"),
        "auto_refresh_tokens": fields.Boolean("Auto Refresh Token"),
    }
    
    def read(self, ids, field_names=None, load_m2o=True, load_all_trans=False, get_time=False, context={}):
        res = self.search([["id","in",ids]])
        if len(res) == 0:
            defaults = self.default_get()
            self.create(defaults)
        return super().read(ids, field_names=field_names, load_m2o=load_m2o, load_all_trans=load_all_trans, get_time=get_time, context=context) 

Settings.register()