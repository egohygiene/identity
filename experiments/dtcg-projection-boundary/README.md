# DTCG projection boundary proof

This disposable proof exercises one high-risk decision from
[issue #7](https://github.com/egohygiene/identity/issues/7): canonical DTCG
tokens can remain immutable while a replaceable projection adapter emits
deterministic consumer output.

The adapter is intentionally tiny. It is a contract double, not a general DTCG
implementation and not production compiler code. It covers only the fixture's
color, dimension, inherited type, alias, stable-name, and stable-order behavior.
The complete parser, resolver, diagnostics, and Style Dictionary integration
belong to #9 and #10.

## Run

Requires Node.js 20 or newer and no installed packages:

```bash
node --test adapter.test.mjs
node adapter.mjs tokens.dtcg.json actual.css
```

The test verifies that:

- the canonical input bytes do not change;
- two independent projections are byte-identical;
- ordering does not depend on object insertion order;
- the projection matches the reviewed golden CSS fixture;
- unsupported types fail instead of being guessed or silently dropped.

## Production handoff

When the compiler workspace exists, preserve these fixtures and replace this
contract double with adapter contract tests. A Style Dictionary adapter must
consume Identity's validated/resolved representation and match the projection
contract; it must never mutate `.identity/` or define merge semantics.

