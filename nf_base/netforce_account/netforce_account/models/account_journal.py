# Copyright (c) 2012-2015 Netforce Co. Ltd.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

from netforce.model import Model, fields


class Journal(Model):
    _name = "account.journal"
    _string = "Journal"
    #_key = ["code"]
    _fields = {
        "name": fields.Char("Name", required=True, search=True),
        "sequence_id": fields.Many2One("sequence", "Sequence", multi_company=True),
        "comments": fields.One2Many("message", "related_id", "Comments"),
        "active": fields.Boolean("Active"),
        "code": fields.Char("Code", search=True),
        "type": fields.Selection([["sale","Sales"],["purchase","Purchases"],["pay_in","Receipts"],["pay_out","Disbursements"],["general","General"],["close","Fiscal Year Closing"],["other","Other"]],"Journal Type"),
    }
    _defaults = {
        "active": True,
    }

Journal.register()
