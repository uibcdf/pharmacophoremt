---
summary: Contributor footer links resolve to a nonexistent path at every documentation depth.
issue: uibcdf/pharmacophoremt#149
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: low
verification: measured
area: [documentation, usability]
guard: devtools/tests/test_docs_navigation.py
normative:
blocked_by: []
supersedes: []
---

# Contributor footer navigation

The actual rendered user-guide footer points to contents/about/who.html.
The real document is content/about/who.html, and nested pages also need the
correct relative prefix. Full strict Sphinx source rendering passes while the
generated template link remains broken. A subsequent actual HTML target audit
exposes the defect; the original output/template remain in the local capsule.

The Jinja template hard-codes an unquoted relative href. Delegate the document
URL to Sphinx's supported pathto context and preserve the attribution wording.
Three actual-template guards reproduce failure for root, user and deep API
contexts. They use the already-declared Jinja2 CI dependency and independent
builder URL declarations, without duplicating Sphinx's routing algorithm.

Acceptance: all three guards pass, full strict rendering succeeds, the real
rendered footer resolves across output depths and the new guide's local links
and fragments verify. Keep original failed/passing-source-render evidence,
update #108/checkpoint and archive this report on resolution. No molecular,
provider, dependency, workflow or version change is needed.

## Resolution — 2026-11-08 UTC

The template now requests Sphinx's pathto('content/about/who') with a quoted href.
Three original guards fail before the fix and pass after it. A fourth case checks
the contributor page's valid self link. All four final guards pass; the actual
strict full HTML render and82rendered contributor targets verify, including51
local links/fragments from the new guide. Six executable recovery-recipe blocks
remain byte-identical. The [receipt](../evidence/library_user_guide_20261108_summary.json)
preserves the original bad link and initial source-reference failure.

The first footer validator incorrectly interpreted the valid self fragment as a
file path; its correction checks the same rendered bytes without another build.
The first index check then exposed the new report's not-yet-regenerated index.
Both control failures remain separate from product rendering/guard evidence.
No public website, representative usability, molecular or installed qualification
is claimed. The fix needs no new dependency: thin CI already declares Jinja2.
