from odoo import _, models, fields, api
import base64
import xlrd
import io
import csv
from io import BytesIO
from odoo.http import request
import sys
import json
import logging
from datetime import date
import xlsxwriter
from datetime import datetime
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

sys.setrecursionlimit(10000)  # To allow a higher recursion depth


class ImportData(models.Model):
    _name = 'custom.import.demo'
    _description = 'Import Data'
    _rec_name = 'beneficiary_name'
    _sql_constraints = [
        ('unique_beneficiary_name', 'unique(beneficiary_name)', 'Beneficiary name must be unique!'),
    ]

    beneficiary_name = fields.Char(string="Benificiary Name")

    # beneficiary_name = fields.Many2one('bank.detail', string='Beneficiary Name', )
    beneficiary_bank = fields.Char(string="Beneficiary Bank")
    beneficiary_branch = fields.Char(string="Beneficiary Branch / IFSC Code")
    beneficiary_acc_no = fields.Char(string="Beneficiary Account No")
    kotak_non_kotak = fields.Char(string="Kotak Non KotakBank")


@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        name = vals.get('beneficiary_name')
        branch = vals.get('beneficiary_branch')
        acc_no = vals.get('beneficiary_acc_no')
        bank_type = vals.get('kotak_non_kotak')

        if name and isinstance(name, str):
            existing = self.env['custom.import.demo'].search([
                ('beneficiary_name', '=', name)
            ], limit=1)
            print("111111111111111111111", existing)

            if existing:
                raise ValidationError(_("Beneficiary name '%s' already exists!") % name)

            # Create new record in custom.import.demo
            new_demo = self.env['custom.import.demo'].create({
                'beneficiary_name': name,
                'beneficiary_branch': branch,
                'beneficiary_acc_no': acc_no,
                'kotak_non_kotak': bank_type,
            })

            # Link newly created record
            vals['beneficiary_name'] = new_demo.id
            print("222222222222222222222222222", existing)

    return super(BankDetail, self).create(vals_list)

