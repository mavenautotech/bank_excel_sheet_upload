from odoo import models, fields, api
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

_logger = logging.getLogger(__name__)

sys.setrecursionlimit(10000)  # To allow a higher recursion depth


class ResLang(models.Model):
    _inherit = "res.lang"

    date_format = fields.Char(default="%d/%m/%Y")

    @api.model
    def _update_date_format(self):
        """Ensure all existing languages have the correct date format."""
        languages = self.search([])
        for lang in languages:
            if lang.date_format != "%d/%m/%Y":
                lang.write({'date_format': "%d/%m/%Y"})  # Use write() to trigger update

    @api.model
    def create(self, vals):
        """Ensure date_format is always set to %d/%m/%Y on creation."""
        vals["date_format"] = "%d/%m/%Y"
        return super(ResLang, self).create(vals)

    def write(self, vals):
        """Prevent users from changing the date format."""
        if "date_format" in vals:
            vals["date_format"] = "%d/%m/%Y"
        return super(ResLang, self).write(vals)

    @api.model
    def init(self):
        """Automatically update date format when the module is installed."""
        self._update_date_format()
