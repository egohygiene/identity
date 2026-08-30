# Repository-presentation fixtures

These fixtures exercise Identity's visual boundary without making Identity an
evidence authority:

- `source.organization-default.json` inherits the approved organization banner
  and pairs with explicit passing evidence;
- `source.product-override.json` applies one approved alt-text override and
  pairs with explicit advisory evidence;
- `source.private.json` records private visibility and pairs with an explicit
  exemption state; and
- `evidence.missing.json` supplies the fail-closed `unknown` state when no
  trustworthy evidence is available.

`hygiene-profile.v1.json` is byte-identical to
`egohygiene/hygiene@cb2ed63425d29abada2d2bbb43a3b3e59d11aeb8` at
`catalog/repository-presentation-profile.json`. Its normalized SHA-256 is
`44e0881519350e6747723995939c79c6fb4659e38a74b2c32e409866e7a186ba`.
The profile is `1.0.0-alpha.1` and `proposed`; these fixtures do not activate it.
