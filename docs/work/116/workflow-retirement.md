# Guidance rewrite workflow retirement (#84)

This candidate removes only the two hardcoded, write-capable prose-rewrite
definitions, `refine-guidance-docs.yml` and `refine-guidance-docs-v2.yml`.
Their complete history remains in Git. No branch, release, deployment or
provider setting is deleted or changed.

## Verified ownership and completion

- [Guidance issue #13](https://github.com/egohygiene/identity/issues/13) is closed.
- [PR #37](https://github.com/egohygiene/identity/pull/37), authored by `szmyty`
  in `egohygiene/identity`, merged `feat/13-brand-guidance-v1` at
  `f0c714561e85c00db280a154b18d79a9e4fa8243` on 2026-08-26.
- The exact branch-ref lookup for `refs/heads/feat/13-brand-guidance-v1`
  returned GitHub 404 during this sprint, while authenticated reads of the
  repository and PR succeeded. No current ref for that historical branch was
  observed; no branch deletion is performed here.
- Both removed workflows trigger only on pushes changing their own definition
  on that hardcoded branch. They grant `contents: write`, replace historical
  README/ROADMAP prose and push directly back to that branch. They are not
  reusable documentation validators.

## Retained workflow inventory

| Definition | Current purpose / authority |
| --- | --- |
| `validate.yml` | Read-only CLI/source/documentation, formatting, lint and behavior checks on pull requests, main pushes and manual dispatch. The #85 generated-source guard remains read-only. |
| `reference-renderer.yml` | Read-only renderer validation on its existing push/PR/dispatch selections. |
| `identity-experience.yml` | Read-only experience validation under its existing triggers. |
| `decision-validation.yml` | Read-only/advisory decision evidence under existing triggers and pins. |
| `development-image.yml` | Read-only image qualification on PR/manual selections; no local Docker acceptance is inferred. |
| `release.yml` | Existing source validation plus separately gated release publication; its job-specific `contents: write` authority is retained unchanged. |
| `publish-brand-kit.yml` | Existing release-bound Brand Kit publisher with its independently governed Pages permissions; no deployment is requested. |

Read-only source/documentation checks are retained. Removing retired prose
writers does not disable those checks, weaken branch protections or authorize
publication. The source diff is reviewable; no workflow has been dispatched and
the candidate uses `[skip ci]`. Actual workflow execution and broader quality
validation remain deferred, so #84 is not declared accepted or closed here.

ADR not required: retire completed one-time implementation scaffolding without
changing a durable policy, interface or human decision disposition.
