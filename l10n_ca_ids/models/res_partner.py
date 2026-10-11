# Copyright 2026 BADEP Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models

from ..tools.partner_identifiers import CA_ADDITIONAL_IDENTIFIERS_METADATA


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _get_all_additional_identifiers_metadata(self):
        return {
            **super()._get_all_additional_identifiers_metadata(),
            **CA_ADDITIONAL_IDENTIFIERS_METADATA,
        }
