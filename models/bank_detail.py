from odoo import api, fields, http, models
from datetime import date
from odoo import _, models, fields, api
import base64
import xlrd
import io
from io import BytesIO
from odoo.http import request
import sys
import json
import logging
import xlsxwriter
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

sys.setrecursionlimit(10000)  # To allow a higher recursion depth


class BankDetail(models.Model):
    _name = 'bank.detail'
    _description = 'Bank Detail'
    _rec_name = 'beneficiary_name'

    name = fields.Char(string='Bank Sequence No', default='New')
    bank_detail_lines = fields.One2many('bank.detail.line', 'bank_detail_id', string='Bank Detail Lines')
    payment_type = fields.Char(string="Payment Type", compute='_compute_payment_type', readonly=True)
    beneficiary_name = fields.Many2one('custom.import.demo', string="Beneficiary Name")
    beneficiary_bank = fields.Char(string="Beneficiary Bank")
    beneficiary_branch = fields.Char(string="Beneficiary Branch / IFSC Code",
                                     related='beneficiary_name.beneficiary_branch', readonly=True)
    beneficiary_acc_no = fields.Char(string="Beneficiary Account No", related='beneficiary_name.beneficiary_acc_no',
                                     readonly=True)
    kotak_non_kotak = fields.Char(string="Bank Type", related='beneficiary_name.beneficiary_acc_no', readonly=True)
    amount = fields.Float(string="Amount", required=True)
    debit_narration = fields.Char(string="Debit Narration")
    credit_narration = fields.Char(string="Credit Narration")

    client_code = fields.Char(default="MAVEN70", readonly=True)
    product_code = fields.Char(default="VPAY", readonly=True)
    payment_ref_no = fields.Char(string="Payment Ref No")
    payment_date = fields.Date(string="Payment Date", default=date.today(), readonly=True)
    instrument_date = fields.Date(string="Instrument Date")
    dr_ac_no = fields.Char(default="9998010676", readonly=True, store=True)

    bank_code_indicator = fields.Char(default="M", readonly=True)
    beneficiary_code = fields.Char(string="Beneficiary Code")

    location = fields.Char(string="Location")
    print_location = fields.Char(string="Print Location")
    instrument_number = fields.Char(string="Instrument Number")
    ben_add1 = fields.Char(string="Ben Add1")
    ben_add2 = fields.Char(string="Ben Add2")
    ben_add3 = fields.Char(string="Ben Add3")
    ben_add4 = fields.Char(string="Ben Add4")

    beneficiary_email = fields.Char(string="Beneficiary Email")
    beneficiary_mobile = fields.Char(string="Beneficiary Mobile")

    payment_details1 = fields.Char(string="Payment Details1")
    payment_details2 = fields.Char(string="Payment Details2")
    payment_details3 = fields.Char(string="Payment Details3")
    payment_details4 = fields.Char(string="Payment Details4")

    enrichment_1 = fields.Char(string="Enrichment 1")
    enrichment_2 = fields.Char(string="Enrichment 2")
    enrichment_3 = fields.Char(string="Enrichment 3")
    enrichment_4 = fields.Char(string="Enrichment 4")
    enrichment_5 = fields.Char(string="Enrichment 5")
    enrichment_6 = fields.Char(string="Enrichment 6")
    enrichment_7 = fields.Char(string="Enrichment 7")
    enrichment_8 = fields.Char(string="Enrichment 8")
    enrichment_9 = fields.Char(string="Enrichment 9")
    enrichment_10 = fields.Char(string="Enrichment 10")
    enrichment_11 = fields.Char(string="Enrichment 11")
    enrichment_12 = fields.Char(string="Enrichment 12")
    enrichment_13 = fields.Char(string="Enrichment 13")
    enrichment_14 = fields.Char(string="Enrichment 14")
    enrichment_15 = fields.Char(string="Enrichment 15")
    enrichment_16 = fields.Char(string="Enrichment 16")
    enrichment_17 = fields.Char(string="Enrichment 17")
    enrichment_18 = fields.Char(string="Enrichment 18")
    enrichment_19 = fields.Char(string="Enrichment 19")
    enrichment_20 = fields.Char(string="Enrichment 20")

    total_amount = fields.Float(
        string="Total Amount",
        compute="_compute_total_line_amount",
        store=True,
    )

    def print_excel(self):
        """Generate and Download an XLS file."""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Data')

        # Write headers
        headers = [
            'Client Code', 'Product Code', 'Payment Type', 'Payment Ref No', 'Payment Date',
            'Instrument Date', 'Dr Ac No', 'Amount', 'Bank Code Indicator', 'Beneficiary Code', 'Beneficiary Name',
            'Beneficiary Bank', 'Beneficiary Branch / IFSC Code', 'Beneficiary Account No', 'Location',
            'Print Location',
            'Instrument Number', 'Ben Add1', 'Ben Add2', 'Ben Add3', 'Ben Add4', 'Beneficiary Email',
            'Beneficiary Mobile', 'Debit Narration', 'Credit Narration', 'Payment Details1', 'Payment Details2',
            'Payment Details3', 'Payment Details4', 'Enrichment 1', 'Enrichment 2', 'Enrichment 3', 'Enrichment 4',
            'Enrichment 5', 'Enrichment 6', 'Enrichment 7', 'Enrichment 8', 'Enrichment 9', 'Enrichment 10',
            'Enrichment 11', 'Enrichment 12', 'Enrichment 13', 'Enrichment 14', 'Enrichment 15', 'Enrichment 16',
            'Enrichment 17', 'Enrichment 18', 'Enrichment 19', 'Enrichment 20',
        ]

        # Write headers to the first row
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # Date format for Excel
        date_format = workbook.add_format({'num_format': 'DD/MM/YYYY'})
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA", date_format)

        # Define a helper function to write the data
        def write_field(col, value, is_date=False):
            # If value is zero and it's an integer field, write as blank (None)
            if isinstance(value, int) and value == 0:
                worksheet.write_blank(row, col, None)
            elif is_date:
                # If the value is a date, write it with the custom date format
                worksheet.write(row, col, value, date_format)
            else:
                worksheet.write(row, col, value)

        row = 1
        for record in self:
            # Now write all your fields to the corresponding column
            for orderline in record.bank_detail_lines:  # Assuming orderlines is a related field
                write_field(0, orderline.client_code)
                write_field(1, orderline.product_code)
                write_field(2, orderline.line_beneficiary_payment_type)
                write_field(3, orderline.payment_ref_no)
                write_field(4, orderline.payment_date, is_date=True)
                write_field(5, orderline.instrument_date)
                write_field(6, orderline.dr_ac_no)
                write_field(7, orderline.line_beneficiary_amount)
                write_field(8, orderline.bank_code_indicator)
                write_field(9, orderline.beneficiary_code)
                write_field(10, orderline.line_beneficiary_name.beneficiary_name if isinstance(
                    orderline.line_beneficiary_name,
                    models.Model) and orderline.line_beneficiary_name else orderline.line_beneficiary_name or '')

                # write_field(10, orderline.beneficiary_name.beneficiary_name if orderline.beneficiary_name else '')
                write_field(11, orderline.line_beneficiary_bank)
                write_field(12, orderline.line_beneficiary_branch)
                write_field(13, orderline.line_beneficiary_acc_no)
                write_field(14, orderline.location)
                write_field(15, orderline.print_location)
                write_field(16, orderline.instrument_number)
                write_field(17, orderline.ben_add1)
                write_field(18, orderline.ben_add2)
                write_field(19, orderline.ben_add3)
                write_field(20, orderline.ben_add4)
                write_field(21, orderline.beneficiary_email)
                write_field(22, orderline.beneficiary_mobile)
                write_field(23, orderline.line_debit_narration)
                write_field(24, orderline.line_credit_narration)
                write_field(25, orderline.payment_details1)
                write_field(26, orderline.payment_details2)
                write_field(27, orderline.payment_details3)
                write_field(28, orderline.payment_details4)
                write_field(29, orderline.enrichment_1)
                write_field(30, orderline.enrichment_2)
                write_field(31, orderline.enrichment_3)
                write_field(32, orderline.enrichment_4)
                write_field(33, orderline.enrichment_5)
                write_field(34, orderline.enrichment_6)
                write_field(35, orderline.enrichment_7)
                write_field(36, orderline.enrichment_8)
                write_field(37, orderline.enrichment_9)
                write_field(38, orderline.enrichment_10)
                write_field(39, orderline.enrichment_11)
                write_field(40, orderline.enrichment_12)
                write_field(41, orderline.enrichment_13)
                write_field(42, orderline.enrichment_14)
                write_field(43, orderline.enrichment_15)
                write_field(44, orderline.enrichment_16)
                write_field(45, orderline.enrichment_17)
                write_field(46, orderline.enrichment_18)
                write_field(47, orderline.enrichment_19)
                write_field(48, orderline.enrichment_20)

                row += 1

            workbook.close()
            file_data = base64.b64encode(output.getvalue())
            output.close()

            # Get today's date in YYYY-MM-DD format
            today_str = date.today().strftime('%d%m%Y')
            file_name = f'PAYMENT{today_str}.xlsx'

            # Create attachment
            attachment = self.env['ir.attachment'].create({
                'name': file_name,
                'type': 'binary',
                'datas': file_data,
                'store_fname': file_name,
                'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            })

            # Return file download action
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
            }

    @api.depends('beneficiary_name', 'amount')
    def _compute_payment_type(self):
        # Determine payment type
        if self.beneficiary_name.kotak_non_kotak == 'KOTAK MAHINDRA BANK':
            self.payment_type = 'IFT'
        elif self.beneficiary_name.kotak_non_kotak:
            if self.amount <= 200000:
                self.payment_type = 'NEFT'
            else:
                self.payment_type = 'RTGS'
        else:
            self.payment_type = False

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('bank.detail') or 'BANK000'
        return super(BankDetail, self).create(vals)

    def action_add_line_and_clear(self):
        for record in self:
            if not record.beneficiary_name:
                raise ValidationError("Please fill all required fields before adding a line.")

            if not record.amount or record.amount <= 0:
                raise ValidationError("Amount is mandatory and must be greater than 0 to add a line.")

            record.bank_detail_lines.create({
                'bank_detail_id': record.id,
                'line_beneficiary_name': record.beneficiary_name.beneficiary_name,
                'line_beneficiary_branch': record.beneficiary_branch,
                'line_beneficiary_acc_no': record.beneficiary_acc_no,
                'line_beneficiary_payment_type': record.payment_type,
                'line_debit_narration': record.debit_narration,
                'line_credit_narration': record.credit_narration,
                'line_payment_date': record.payment_date,
                'line_beneficiary_amount': record.amount,
            })

            # Clear fields
            record.write({
                'beneficiary_name': False,
                'beneficiary_branch': False,
                'beneficiary_acc_no': False,
                'payment_type': False,
                'kotak_non_kotak': False,
                'debit_narration': False,
                'credit_narration': False,
                'amount': False,
            })


    @api.depends('bank_detail_lines.line_beneficiary_amount')
    def _compute_total_line_amount(self):
        for record in self:
            record.total_amount = sum(
                float(amount or 0.0) for amount in record.bank_detail_lines.mapped('line_beneficiary_amount')
            )


class BankDetailLine(models.Model):
    _name = 'bank.detail.line'
    _description = 'Bank Detail Lines'
    _order = "id desc"

    bank_detail_id = fields.Many2one('bank.detail', string="Bank Record")
    client_code = fields.Char(default="MAVEN70", readonly=True)
    product_code = fields.Char(default="VPAY", readonly=True)
    payment_ref_no = fields.Char(string="Payment Ref No")
    payment_date = fields.Date(string="Payment Date", default=date.today())
    instrument_date = fields.Date(string="Instrument Date")
    dr_ac_no = fields.Char(default="9998010676", readonly=True)
    amount = fields.Float(string="Amount")

    bank_code_indicator = fields.Char(default="M", readonly=True)
    beneficiary_code = fields.Char(string="Beneficiary Code")
    location = fields.Char(string="Location")
    print_location = fields.Char(string="Print Location")
    instrument_number = fields.Char(string="Instrument Number")
    ben_add1 = fields.Char(string="Ben Add1")
    ben_add2 = fields.Char(string="Ben Add2")
    ben_add3 = fields.Char(string="Ben Add3")
    ben_add4 = fields.Char(string="Ben Add4")
    beneficiary_email = fields.Char(string="Beneficiary Email")
    beneficiary_mobile = fields.Char(string="Beneficiary Mobile")
    payment_details1 = fields.Char(string="Payment Details1")
    payment_details2 = fields.Char(string="Payment Details2")
    payment_details3 = fields.Char(string="Payment Details3")
    payment_details4 = fields.Char(string="Payment Details4")

    enrichment_1 = fields.Char(string="Enrichment 1")
    enrichment_2 = fields.Char(string="Enrichment 2")
    enrichment_3 = fields.Char(string="Enrichment 3")
    enrichment_4 = fields.Char(string="Enrichment 4")
    enrichment_5 = fields.Char(string="Enrichment 5")
    enrichment_6 = fields.Char(string="Enrichment 6")
    enrichment_7 = fields.Char(string="Enrichment 7")
    enrichment_8 = fields.Char(string="Enrichment 8")
    enrichment_9 = fields.Char(string="Enrichment 9")
    enrichment_10 = fields.Char(string="Enrichment 10")
    enrichment_11 = fields.Char(string="Enrichment 11")
    enrichment_12 = fields.Char(string="Enrichment 12")
    enrichment_13 = fields.Char(string="Enrichment 13")
    enrichment_14 = fields.Char(string="Enrichment 14")
    enrichment_15 = fields.Char(string="Enrichment 15")
    enrichment_16 = fields.Char(string="Enrichment 16")
    enrichment_17 = fields.Char(string="Enrichment 17")
    enrichment_18 = fields.Char(string="Enrichment 18")
    enrichment_19 = fields.Char(string="Enrichment 19")
    enrichment_20 = fields.Char(string="Enrichment 20")

    line_beneficiary_name = fields.Char(string="Benificiary Name", readonly=True)
    line_beneficiary_bank = fields.Char(string="Beneficiary Bank")
    line_beneficiary_branch = fields.Char(string="Beneficiary Branch / IFSC Code", readonly=True)
    line_beneficiary_acc_no = fields.Char(string="Beneficiary Account No", readonly=True)
    line_beneficiary_payment_type = fields.Char(string="Payment Type", readonly=True)
    line_debit_narration = fields.Char(string="Debit Narration")
    line_credit_narration = fields.Char(string="Credit Narration")
    line_payment_date = fields.Char(string="Payment Date")
    line_beneficiary_amount = fields.Char(string="Amount",readonly=True, default=0.0)

    # @api.ondelete(at_uninstall=False)
    def _unlink_record(self):
        for record in self:
            l = []
            l.append(record.id)
            query = 'DELETE FROM bank_detail_line WHERE bank_detail_id = %s'
            self.env.cr.execute(query, (l))
