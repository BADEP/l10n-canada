# Copyright 2026 BADEP Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import re

from stdnum.ca import bn as ca_bn

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


def _digits(value):
    return re.sub(r"[\s.-]", "", value or "")


def _normalize_neq(value):
    number = _digits(value)
    if not re.fullmatch(r"\d{10}", number):
        raise ValueError
    return number


def _normalize_bn(value):
    """9-digit CRA Business Number (without the program account suffix)."""
    number = _digits(value)
    if len(number) != 9:
        raise ValueError
    return ca_bn.validate(number)


def _normalize_corp_number(value):
    match = re.fullmatch(r"(\d{7})(\d)", _digits(value))
    if not match:
        raise ValueError
    return f"{match.group(1)}-{match.group(2)}"


def _normalize_rq_id(value):
    number = _digits(value)
    if not re.fullmatch(r"\d{10}", number):
        raise ValueError
    return number


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
    l10n_ca_bn = fields.Char(
        string="BN",
        copy=False,
        index="btree_not_null",
        help="9-digit Business Number issued by the Canada Revenue Agency. "
        "The GST/HST account (BN + RT 0001) goes in the Tax ID field.",
    )
    l10n_ca_rq_id = fields.Char(
        string="Revenu Québec ID",
        copy=False,
        index="btree_not_null",
        help="10-digit Revenu Québec identification number (NI), shared by the "
        "IC, RS and TQ files. The QST account (NI + TQ 0001) goes in the "
        "PST number field.",
    )

    @api.model
    def _l10n_ca_id_normalizers(self):
        return {
            "l10n_ca_neq": _normalize_neq,
            "l10n_ca_corp_number": _normalize_corp_number,
            "l10n_ca_bn": _normalize_bn,
            "l10n_ca_rq_id": _normalize_rq_id,
        }

    @api.model
    def _l10n_ca_normalize_vals(self, vals):
        vals = dict(vals)
        for fname, normalize in self._l10n_ca_id_normalizers().items():
            value = vals.get(fname)
            if not value:
                vals[fname] = False
                continue
            try:
                vals[fname] = normalize(value)
            except Exception as e:  # noqa: BLE001
                raise ValidationError(
                    _(
                        "%(label)s “%(value)s” is not valid.",
                        label=self._fields[fname]._description_string(self.env),
                        value=value,
                    )
                ) from e
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        fnames = self._l10n_ca_id_normalizers()
        vals_list = [
            self._l10n_ca_normalize_vals(vals) if fnames.keys() & vals.keys() else vals
            for vals in vals_list
        ]
        return super().create(vals_list)

    def write(self, vals):
        if self._l10n_ca_id_normalizers().keys() & vals.keys():
            vals = self._l10n_ca_normalize_vals(vals)
        return super().write(vals)
