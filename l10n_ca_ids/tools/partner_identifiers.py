# Copyright 2026 BADEP Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import re

from stdnum.ca import bn as ca_bn

from odoo.tools.translate import LazyTranslate

_lt = LazyTranslate(__name__)

_NEQ_RE = re.compile(r"^\d{10}$")
_CORP_RE = re.compile(r"^(\d{7})(\d)$")
_RQ_RE = re.compile(r"^\d{10}$")


def _digits(value):
    return re.sub(r"[\s.-]", "", value or "")


def neq_validate(value):
    number = _digits(value)
    if not _NEQ_RE.match(number):
        raise ValueError("A NEQ has 10 digits.")
    return number


def bn_validate(value):
    """9-digit CRA Business Number (without the program account suffix)."""
    number = _digits(value)
    if len(number) != 9:
        raise ValueError("A Business Number has 9 digits.")
    return ca_bn.validate(number)


def corp_validate(value):
    """Corporations Canada number, stored as ``1234567-8``."""
    match = _CORP_RE.match(_digits(value))
    if not match:
        raise ValueError("A federal corporation number looks like 1234567-8.")
    return f"{match.group(1)}-{match.group(2)}"


def rq_validate(value):
    number = _digits(value)
    if not _RQ_RE.match(number):
        raise ValueError("A Revenu Québec identification number has 10 digits.")
    return number


CA_ADDITIONAL_IDENTIFIERS_METADATA = {
    "CA_NEQ": {
        "sequence": 10,
        "label": _lt("NEQ"),
        "help": _lt(
            "Québec enterprise number (Numéro d'entreprise du Québec) issued "
            "by the Registraire des entreprises."
        ),
        "placeholder": "1182629064",
        "category": "EN",
        "validation_function": neq_validate,
        "countries": ["CA"],
    },
    "CA_CORP": {
        "sequence": 20,
        "label": _lt("Federal Corporation No."),
        "help": _lt("Corporation number issued by Corporations Canada (CBCA)."),
        "placeholder": "1234567-8",
        "category": "EN",
        "validation_function": corp_validate,
        "countries": ["CA"],
    },
    "CA_BN": {
        "sequence": 30,
        "label": _lt("BN"),
        "help": _lt(
            "9-digit Business Number issued by the Canada Revenue Agency. "
            "The GST/HST account (BN + RT 0001) goes in the Tax ID field."
        ),
        "placeholder": "123026635",
        "category": "EN",
        "validation_function": bn_validate,
        "countries": ["CA"],
    },
    "CA_RQ": {
        "sequence": 40,
        "label": _lt("Revenu Québec ID"),
        "help": _lt(
            "10-digit Revenu Québec identification number (NI), shared by the "
            "IC, RS and TQ files. The QST account (NI + TQ 0001) goes in the "
            "PST number field."
        ),
        "placeholder": "1234567890",
        "category": "EN",
        "validation_function": rq_validate,
        "countries": ["CA"],
    },
}
