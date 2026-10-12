Adds the Canadian business identifiers of *your own company* that `l10n_ca`
and Odoo do not cover. They are real stored (searchable) fields on the company,
validated on save:

| Field | Issuer | Format | Shown |
|---|---|---|---|
| NEQ | Registraire des entreprises du Québec | 10 digits | Canadian companies in Québec |
| Federal Corporation No. | Corporations Canada (CBCA) | `1234567-8` | Canadian companies |

Other Canadian identifiers are already covered, so they are not duplicated:

- **GST/HST account** (`123456789 RT 0001`, which contains the CRA Business
  Number): the standard *Tax ID* field.
- **PST / QST account** (`1234567890 TQ 0001`, which contains the Revenu Québec
  ID): the *PST number* field of `l10n_ca`.
