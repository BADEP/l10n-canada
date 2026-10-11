# Copyright 2026 BADEP Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestCaIdentifiers(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test CA",
                "country_id": cls.env.ref("base.ca").id,
                "is_company": True,
            }
        )

    def _set(self, key, value):
        self.partner._set_additional_identifier(key, value)
        return self.partner._get_additional_identifier(key)

    def test_valid_values_are_normalized(self):
        self.assertEqual(self._set("CA_NEQ", "1182 629 064"), "1182629064")
        self.assertEqual(self._set("CA_BN", "782 787 246"), "782787246")
        self.assertEqual(self._set("CA_CORP", "18282820"), "1828282-0")
        self.assertEqual(self._set("CA_CORP", "1828282-0"), "1828282-0")
        self.assertEqual(self._set("CA_RQ", "1234240621"), "1234240621")

    def test_invalid_values_are_rejected(self):
        for key, value in (
            ("CA_NEQ", "118262906"),
            ("CA_BN", "123456783"),
            ("CA_BN", "782787246RT0001"),
            ("CA_CORP", "182828"),
            ("CA_RQ", "12342406AB"),
        ):
            with self.subTest(key=key, value=value), self.assertRaises(
                ValidationError
            ):
                self.partner._set_additional_identifier(key, value)

    def test_available_for_canadian_partner(self):
        available = self.partner.available_additional_identifiers_metadata
        self.assertTrue({"CA_NEQ", "CA_CORP", "CA_BN", "CA_RQ"} <= set(available))

    def test_not_available_for_foreign_partner(self):
        partner = self.env["res.partner"].create(
            {"name": "Test FR", "country_id": self.env.ref("base.fr").id}
        )
        self.assertFalse({"CA_NEQ", "CA_BN"} & set(partner.available_additional_identifiers_metadata))
