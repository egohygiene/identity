# Approval timestamp parser finding

Inspected implementation: `75ca39f3fc7e5e9e0b5578af58c966cd2590a652`.
This is a bounded synthetic-fixture probe for the existing #70 quality work.
It does not change the parser or admit actual Identity source.

`scripts/identity_validation/governance.py` calls `datetime.fromisoformat`
for `reviewedAt`. Python accepts a date-only string there, although the native
diagnostic and authoring contract require an RFC 3339 timestamp with an explicit
UTC offset. The source schema's `format: date-time` expresses the same boundary.

The actual probe copied `tests/fixtures/v1/valid/minimal/.identity/` into a new
temporary directory and changed only the 14 fictional approval records'
`reviewedAt` values to `2026-11-22`. It then ran:

```sh
python3 scripts/validate_identity.py --repository-root TEMP_CONSUMER --format json
```

Observed: **exit 0, valid true, no diagnostics**. Pipe/disk/runtime failures or
the actual Identity candidate were not substituted for this result. The copied
fixture used its existing fictional subjects/reviewer; no real owner approval
was created and the temporary tree was removed.

The installed `jsonschema.FormatChecker` has no `date-time` checker registered
because that optional format support is unavailable. Its zero diagnostics on
this probe therefore does not supply RFC 3339 conformance. Null fields still
fail ordinary schema types, which is distinct from checking a non-null time.

Do not use date-only parser acceptance to populate actual owner metadata. The
proposed Identity candidate retains null review times and remains invalid.
Root owns the separate bounded parser repair and meaningful date-only,
timezone-free, explicit-offset and native-bundle controls; this checkpoint adds
no new issue, runtime/schema change or approval exception.
