# Authorized Identity source merges — 2026-11-02

| PR | Merged commit | Source scope |
| --- | --- | --- |
| [#129](https://github.com/egohygiene/identity/pull/129) | `ec865c336a892943e55e8e1d3be0ae5c3c299c61` | Complete public kit; merge tree exactly matches head d247487379569c3701a8cefe6d6136502657fa64. |
| [#130](https://github.com/egohygiene/identity/pull/130) | `f9b20b707d72472134ae209ec496cb8e6e4df053` | Product handoffs, announcement draft, workflow retirement and validator/projection refactors; merge tree matches head 8cc57e2da51c44a132b7380e85ef4b1276184366. |
| [#123](https://github.com/egohygiene/identity/pull/123) | `037fcc042f8e94743d3756a121f0df1d0a5f74d7` | Reconciled browser preparation; merge tree matches head d0d9535546a45c7fce3ed2f2cba1731ca3a71c03 and resolved source tree f027f90514772055273ff7c16ad15d53c34a2153. |

The maintainer authorized these source merges with tests/CI deferred. All merge
messages contain CI skip markers; zero workflow runs were observed for the three
merge commits. No tests, current browser replay, actual local Docker run,
release, deployment, posting or new creative approval was performed.

## Preserved integration boundaries

PR123 was reconciled with the newer product and validator/projection source.
The current producer/verifier both require **nine** positive E2E cases, plus
one intentional screenshot-comparison failure and one restored pass. Zero
retries/skips, the approved screenshot hash and image/font pins are retained.
Historical six-case receipts and screenshots remain byte-identical; they apply
only to their dated source and do not qualify this combined code. Python/JS
syntax, conflict/whitespace and exact-source preservation were inspected.

## Remaining work

- #105 is closed through PR129. IDN-Q35 records its actual prior exact-head
  qualification and authorized merge; this is not a blanket current-CI pass.
- GitHub automatically closed #80 when #123 merged. It is reopened: fresh
  nine-case replay and actual local Docker acceptance are still missing.
- #70 retains the full lint/test/native/browser/CI sweep. #82/#88 retain the
  #80 dependency; #84/#85/#86 source landed but their deferred validation remains.
- #109 and ADR-0031 require explicit scope disposition. #106/ADR-0032 need an
  agreed consumer/template and runtime proof; #107 needs actual selection or
  disposition. #108 records the DCO action reference as unresolved, not a new
  enforcement implementation. No proposed ADR is accepted by these merges.
- #87, final #83 and #98 self-source/rights, release, dogfood and contrasting
  consumer acceptance remain in #116. The [sprint handoff](HANDOFF.md) retains
  exact deferred commands and per-issue scope.

ADR not required: this closeout updates operational facts and evidence after
explicitly authorized source merges, without changing runtime behavior,
contract ownership, creative rights or human decision disposition.
