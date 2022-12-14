# Copyright (c) 2012-2017 Netforce Software Co. Ltd.
# All Rights Reserved.
#
# This file is part of Netforce
# (see https://netforce.com/).

from netforce.model import Model, fields, get_model
from netforce.access import get_active_company
from datetime import *
from dateutil.relativedelta import *
from collections import defaultdict
from pprint import pprint


class ReportDepSchedule(Model):
    _name = "report.dep.schedule"
    _transient = True
    _fields = {
        "date_from": fields.Date("From", required=True),
        "date_to": fields.Date("To", required=True),
        "track_id": fields.Many2One("account.track.categ", "Tracking"),
    }

    _defaults = {
        "date_from": lambda *a: date.today().strftime("%Y-01-01"),
        "date_to": lambda *a: (date.today() + relativedelta(day=31)).strftime("%Y-%m-%d"),
    }

    def get_report_data(self, ids, context={}):
        company_id = get_active_company()
        comp = get_model("company").browse(company_id)
        if ids:
            params = self.read(ids, load_m2o=False)[0]
        else:
            params = self.default_get(load_m2o=False, context=context)
        date_from = params["date_from"]
        date_to = params["date_to"]
        track_id = params.get("track_id")
        assets = {}
        cond = [["state", "=", "registered"]]
        if track_id:
            cond.append(["track_id", "=", track_id])
        for asset in get_model("account.fixed.asset").search_browse(cond, context={"date": date_from}):
            vals = {
                "asset_id": asset.id,
                "asset_name": asset.name,
                "asset_number": asset.number,
                "type_name": asset.type_id.name,
                "rate": asset.dep_rate,
                "purchase_price": asset.price_purchase,
                "purchase_date": asset.date_purchase,
                "book_val_from": asset.book_val,
                "track_id": asset.track_id.id,
            }
            assets[asset.id] = vals
        for asset in get_model("account.fixed.asset").search_browse(cond, context={"date": date_to}):
            vals = assets[asset.id]
            vals["book_val_to"] = asset.book_val
            vals["accum_dep"] = vals["book_val_from"] - vals["book_val_to"]
        lines = sorted(assets.values(), key=lambda v: (v["type_name"], v["asset_name"]))
        groups = []
        cur_group = None
        for line in lines:
            if not cur_group or line["type_name"] != cur_group["type_name"]:
                cur_group = {
                    "type_name": line["type_name"],
                    "lines": [],
                }
                groups.append(cur_group)
            cur_group["lines"].append(line)
        for group in groups:
            group.update({
                "total_book_val_from": sum([l["book_val_from"] for l in group["lines"]]),
                "total_accum_dep": sum([l["accum_dep"] for l in group["lines"]]),
                "total_book_val_to": sum([l["book_val_to"] for l in group["lines"]]),
            })
        pprint(groups)
        data = {
            "company_name": comp.name,
            "date_from": date_from,
            "date_to": date_to,
            "groups": groups,
            "total_book_val_from": sum([l["book_val_from"] for l in lines]),
            "total_accum_dep": sum([l["accum_dep"] for l in lines]),
            "total_book_val_to": sum([l["book_val_to"] for l in lines]),
        }
        return data

ReportDepSchedule.register()
