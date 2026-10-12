# Copyright 2026 BADEP Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_ca_neq = fields.Char(
        string="NEQ",
        copy=False,
        index="btree_not_null",
        help="Québec enterprise number (Numéro d'entreprise du Québec) issued by "
        "the Registraire des entreprises. 10 digits.",
    )
    l10n_ca_corp_number = fields.Char(
        string="Federal Corporation No.",
        copy=False,
        index="btree_not_null",
        help="Corporation number issued by Corporations Canada (CBCA), "
        "e.g. 1234567-8.",
    )
    l10n_ca_state_code = fields.Char(
        related="state_id.code", string="Province Code", readonly=True
    )

    @api.constrains("l10n_ca_neq")
    def _check_l10n_ca_neq(self):
        for company in self.filtered("l10n_ca_neq"):
            if not re.fullmatch(r"\d{10}", company.l10n_ca_neq):
                raise ValidationError(
                    _("The NEQ must have exactly 10 digits (e.g. 1234567890).")
                )

    @api.constrains("l10n_ca_corp_number")
    def _check_l10n_ca_corp_number(self):
        for company in self.filtered("l10n_ca_corp_number"):
            if not re.fullmatch(r"\d{7}-\d", company.l10n_ca_corp_number):
                raise ValidationError(
                    _(
                        "The federal corporation number must look like "
                        "1234567-8 (7 digits, a dash, 1 check digit)."
                    )
                )
