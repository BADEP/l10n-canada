Adds the Canadian business identifiers that `l10n_ca` and Odoo do not cover,
using Odoo's additional identifiers (shown on the partner and company forms
for Canadian contacts, validated and normalized on save):

| Identifier | Issuer | Format |
|---|---|---|
| NEQ | Registraire des entreprises du Québec | 10 digits |
| Federal Corporation No. | Corporations Canada (CBCA) | `1234567-8` |
| BN | Canada Revenue Agency | 9 digits (Luhn checked) |
| Revenu Québec ID (NI) | Revenu Québec | 10 digits |

Already covered elsewhere, so intentionally not duplicated:

- **GST/HST account** (`123456789 RT 0001`): the standard *Tax ID* field.
- **PST / QST account** (`1234567890 TQ 0001`): the *PST number* field of `l10n_ca`.
