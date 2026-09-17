# Terrane manual

This repository is the canonical authored source for Terrane's user documentation.
It contains two publications:

- **[The Terrane Book](tutorial-book/manual.yaml)** — a guided learning path from a
  first program through application architecture, testing, concurrency, and
  performance.
- **[Terrane Reference](reference/manual.yaml)** — precise language, standard-library,
  package, tooling, and compiler-interface contracts.

## Where to start

- New to Terrane: begin with the [tutorial preface](tutorial-book/records/preface.yaml).
- Building a real application: use the
  [application development map](reference/records/manual/application-development-map.yaml).
- Looking up package configuration: use the
  [complete package manifest reference](reference/records/packages/package-manifest.yaml).
- Looking up a function, operation, manifest key, diagnostic, or namespace: search
  [the generated symbol index](generated/symbol-index.yaml).
- Checking whether surprising behavior is intended: compare the normative reference
  with [current implementation limitations](reference/records/tooling/current-limitations.yaml).

The [unified catalog](generated/catalog.yaml) lists every published record with its
publication, navigation group, source path, lifecycle, documentation status, surface,
provenance, and stable section IDs. Compiler-backed lookup data lives in
[the compiler surface](generated/compiler-surface.yaml) and
[the diagnostic inventory](generated/diagnostics.yaml).

## Documentation model

`spec.md` defines the shared YAML manual IR. Publication manifests (`manual.yaml`) own
navigation and select canonical records. Records own stable semantic IDs,
documentation blocks, lifecycle data, and provenance. The Markdown renderer is one
output consumer; records are not converted through Markdown before HTML generation.

The manual repository is intentionally separate from the Terrane compiler repository.
Authored documentation remains reviewable and versionable here. Build inputs such as
compiler snapshots are supplied by the documentation pipeline, while generated lookup
artifacts record the exact source digest used for a refresh.

## Validate and refresh generated indexes

From this repository inside a Terrane checkout:

```sh
python tools/generate_manual_catalog.py
python tools/generate_manual_catalog.py --check
```

The generator validates stable record and section IDs, verifies marked compiler-backed
synopses against compiler-owned declarations, and refreshes all files under
`generated/`. Pass `--compiler-root PATH` when the compiler checkout is not the parent
directory.

The Terrane documentation pipeline validates and renders the complete manual IR.
