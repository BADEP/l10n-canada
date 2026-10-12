Adds the Canadian business identifiers of *your own company* that `l10n_ca`
and Odoo do not cover. They are real stored (searchable) fields on the company,
shown on the company form for Canadian companies (the NEQ and Revenu Québec
ID only when the province is Québec), validated and normalized on
save:

| Field | Issuer | Format |
|---|---|---|
| NEQ | Registraire des entreprises du Québec | 10 digits |
| Federal Corporation No. | Corporations Canada (CBCA) | `1234567-8` |
| BN | Canada Revenue Agency | 9 digits (Luhn checked) |
| Revenu Québec ID (NI) | Revenu Québec | 10 digits |

Partners are intentionally left alone: what is usually asked from customers
and suppliers is already covered, so it is not duplicated:

- **GST/HST account** (`123456789 RT 0001`): the standard *Tax ID* field.
- **PST / QST account** (`1234567890 TQ 0001`): the *PST number* field of `l10n_ca`.
