# Copyright 2026 BADEP Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCompanyIds(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env["res.company"].create(
            {"name": "Test CA", "country_id": cls.env.ref("base.ca").id}
        )

    def test_valid_values(self):
        self.company.write(
            {"l10n_ca_neq": "1182629064", "l10n_ca_corp_number": "1828282-0"}
        )
        self.assertEqual(self.company.l10n_ca_neq, "1182629064")
        self.assertEqual(self.company.l10n_ca_corp_number, "1828282-0")

    def test_writing_one_keeps_the_other(self):
        self.company.write(
            {"l10n_ca_neq": "1182629064", "l10n_ca_corp_number": "1828282-0"}
        )
        self.company.l10n_ca_neq = "2234567890"
        self.assertEqual(self.company.l10n_ca_corp_number, "1828282-0")
        self.company.l10n_ca_corp_number = "1234567-8"
        self.assertEqual(self.company.l10n_ca_neq, "2234567890")

    def test_invalid_values_are_rejected(self):
        for fname, value in (
            ("l10n_ca_neq", "118262906"),
            ("l10n_ca_neq", "11826290AB"),
            ("l10n_ca_corp_number", "182828"),
            ("l10n_ca_corp_number", "18282820"),
        ):
            with self.subTest(fname=fname, value=value), self.assertRaises(
                ValidationError
            ):
                self.company.write({fname: value})

    def test_searchable_and_clearable(self):
        self.company.l10n_ca_neq = "1182629064"
        found = self.env["res.company"].search([("l10n_ca_neq", "=", "1182629064")])
        self.assertEqual(found, self.company)
        self.company.l10n_ca_neq = False
        self.assertFalse(self.company.l10n_ca_neq)
