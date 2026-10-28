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
- Catching up after an upgrade: read the
  [changelog version index](reference/records/manual/changelog.yaml). Each version has its own page of dated changes, with Unreleased first.
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

PDF publishing consumes that structured HTML directly through Chromium's print
engine, not through a Markdown round-trip. The converter needs an installed
Chromium/Chrome executable for PDF output; set `CHROME` to its full path if it is
not found automatically. In a Terrane checkout, see
`projects/docs-converter/README.md` for runtime prerequisites and the real-PDF
regression command.

The manual repository is intentionally separate from the Terrane compiler repository.
Authored documentation remains reviewable and versionable here. Build inputs such as
compiler snapshots are supplied by the documentation pipeline, while generated lookup
artifacts record the exact source digest used for a refresh.

## Format, validate, and refresh manual YAML

Install the pinned formatter release once:

```sh
npm install --global --prefix ~/.local prettier@3.9.8
```

From this repository inside a Terrane checkout:

```sh
# Format manifest-derived YAML, validate records, and refresh generated files.
python tools/generate_manual_catalog.py

# Format manifest-derived YAML, then fail if generated files need refreshing.
python tools/generate_manual_catalog.py --check
```

Both commands reject duplicate YAML mapping keys before running the formatter, including
duplicates nested inside examples. Errors identify the input file and the first and
repeated key locations; invalid input is left unchanged. Standard YAML merge keys and
explicit overrides of merged defaults remain supported.

Run the validator regression tests with:

```sh
python -m unittest discover -s tools -p 'test_*.py'
```

Prettier formats the YAML envelope at an 80-character print width, then reflows
prose-only `markdown` literal scalars at the same width. Typed preformatted material
is preserved; code and other preformatted content belong in `example` or `grammar`
fields. Both commands snapshot every manifest-derived YAML input, format it, and
restore it if formatting exposes a record-validation or generation failure. `--check`
retains successful formatting changes and then reports stale generated artifacts.

The generator validates stable record and section IDs, verifies marked compiler-backed
synopses against compiler-owned declarations, and refreshes all files under
`generated/`. The format-2 catalog is the compact discovery view: it carries each
page's authored summary and recursive ID-and-title section outline without duplicating
that metadata in `manual.yaml`. Pass `--compiler-root PATH` when the compiler checkout
is not the parent directory.

The Terrane documentation pipeline validates and renders the complete manual IR.
