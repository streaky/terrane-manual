# Terrane reference IR and authoring format

This document defines a structured source format for producing the Terrane reference manual. The canonical authoring unit is a YAML record, normally one file per reference surface or conceptual page. Human prose is written as Markdown inside YAML block scalars. Compiler-known facts remain structured data and can be emitted, compared, and updated without treating Markdown as an API database.

The intended manual combines three forms of reference:

- a browsable language reference, where syntax and semantic rules can be read independently and linked precisely, in the style of the Rust Reference;
- an entity reference, where namespaces, descriptors, classes, interfaces, traits, functions, methods, properties, constants, and diagnostics have predictable generated synopses, in the style of the PHP manual;
- an internals reference, where durable compiler, lowering, runtime, generated-code, projection, tooling, cache, artifact, diagnostic, and host-ABI contracts can be located without treating their implementation as an importable Terrane surface.

This format is a reference representation and publication system. It is not an independent language-design authority. Until the project explicitly changes that relationship:

- `docs/language-spec-and-compiler-architecture-draft.md` remains authoritative for the settled language design;
- executable conformance cases define what the current compiler supports;
- the compiler-emitted reference surface describes facts present in a particular compiler build;
- lifecycle and explanatory text remain explicit authored decisions.

## 1. Central model

The reference system has four inputs and one assembled IR:

```text
compiler semantic model
        |
        v
compiler surface snapshot ---------+
                                    |
authored YAML reference records ----+--> assembled reference IR --> renderers
                                    |
manual navigation -----------------+
                                    |
release/profile configuration ------+
```

The important separation is:

```text
surface facts       compiler-owned
lifecycle decisions human/release-owned
documentation       human-owned
provenance          shared, with field-level ownership
presentation        renderer-owned
```

Markdown is not used to encode signatures, parameters, inheritance, availability, or member ownership. It is used for explanation, examples surrounding a contract, warnings, migration guidance, and conceptual language material.

## 2. Design goals

The format must provide:

1. **A real reference IR.** The processor receives typed entities and relationships rather than recovering them from prose.
2. **Compiler participation.** The compiler can emit the surface it actually understands from its semantic model.
3. **Safe reconciliation.** A tool can add records and update compiler-owned fields without rewriting authored prose or silently removing entities.
4. **Readable authoring.** YAML records and their Markdown scalars remain understandable in a normal editor.
5. **Stable identity.** Entities, pages, rules, examples, terms, and sections retain IDs across renames and file moves.
6. **One system for API and language reference material.** Both participate in navigation, search, cross-references, profiles, and rendering.
7. **Explicit lifecycle.** Presence in or absence from one compiler build is not confused with a human decision to add, deprecate, or remove a public contract.
8. **Generated reference views.** Signatures, parameter tables, inheritance, member indexes, availability, and search records come from structured data.
9. **Checkable examples.** An example states whether it is illustrative, accepted, runnable, or intentionally rejected.
10. **Deterministic output.** Identical inputs and tool versions produce equivalent assembled IR and rendered output.
11. **Strict validation.** Unknown fields, stale references, ambiguous identities, surface drift, and incomplete documentation fail visibly.
12. **Reusable package schema.** Compiler-owned, standard-library, source-declared, and projected dependency surfaces can use the same entity model where their contracts permit it.

The first format deliberately excludes arbitrary YAML tags, anchors and aliases, raw HTML, embedded scripts, remote includes, prose macros, and executable templates.

## 3. Source layout

A reference source root has this shape:

```text
reference/
├── manual.yaml
├── records/
│   ├── manual/
│   │   └── introduction.yaml
│   ├── language/
│   │   ├── lexical-structure.yaml
│   │   └── functions/
│   │       └── arguments.yaml
│   ├── api/
│   │   └── core/
│   │       ├── output/
│   │       │   └── print.yaml
│   │       └── types/
│   │           └── string/
│   │               ├── index.yaml
│   │               └── concat.yaml
│   ├── internals/
│   │   └── execution-runtime.yaml
│   └── diagnostics/
│       └── unknown-name.yaml
├── lifecycle/
│   └── renames.yaml
└── assets/
    └── object-model.svg
```

Rules:

- Every record file uses lowercase kebab-case and the `.yaml` extension.
- A record file defines exactly one page or entity.
- Source paths organize work but do not define identity, ownership, navigation, or output URLs.
- Moving a record does not change its ID.
- `manual.yaml` defines navigation and grouping.
- `lifecycle/renames.yaml` records explicit identity migrations used during reconciliation.
- Assets are local. A build does not fetch remote content.
- Generated compiler snapshots are build inputs, not canonical authored files under `records/`.

## 4. YAML profile

Reference records use the YAML 1.2 core schema with these restrictions:

- UTF-8 only;
- mappings, sequences, strings, integers, booleans, and `null` only;
- no custom tags;
- no anchors, aliases, or merge keys;
- no duplicate mapping keys;
- versions are quoted strings;
- unknown keys are errors;
- list-valued fields always use sequences, including a one-item list;
- source-facing code and Markdown use block scalars rather than escaped single-line strings when multiline.

Use `>-` for a short paragraph whose source may wrap and `|-` for Markdown or source code whose line structure matters:

```yaml
documentation:
  summary: >-
    Writes the canonical display of its arguments followed by one newline.

  sections:
    - id: behaviour
      title: Behaviour
      blocks:
        - type: markdown
          markdown: |-
            Arguments are evaluated from left to right.

            No separator is inserted between their displays.
```

The processor parses Markdown only in fields explicitly declared as Markdown by this format. A string field such as `symbol`, `id`, `type`, or `title` is plain text unless its schema says otherwise.

## 5. Record envelope

Every record has the same top-level envelope and canonical key order:

```yaml
format: 1
id: api.core.output.print
kind: function

surface: {}
lifecycle: {}
documentation: {}
provenance: {}
```

Top-level fields:

| Field | Required | Owner | Meaning |
|---|---:|---|---|
| `format` | yes | format | Integer record-format version. |
| `id` | yes | identity/release | Stable global reference identity. |
| `kind` | yes | identity/release | Record kind from the registry. |
| `surface` | entity kinds | compiler | Compiler-known source-facing contract. |
| `lifecycle` | yes | human/release | Publication status and compatibility history. |
| `documentation` | yes | human | Title, summary, prose, examples, and authored labels. |
| `provenance` | yes | shared | Specification, compiler, and conformance evidence. |

Conceptual records such as language chapters have `surface: null`. Their rules, grammar, and explanations live under `documentation` because they cannot be reconstructed merely by enumerating compiler symbols.

A processor must reject unknown top-level fields. A format revision may add optional fields only under the format-evolution rules in this document.

## 6. Stable IDs

An ID consists of lowercase dot-separated segments. Each segment begins with an ASCII letter and continues with lowercase ASCII letters, digits, or internal hyphens:

```text
[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)*
```

Recommended roots:

| Root | Use |
|---|---|
| `manual` | Introduction, conventions, and manual-level pages. |
| `lang` | Language syntax and semantic topics. |
| `api` | Namespaces and object/API entities. |
| `tool` | Compiler, command-line, manifest, and tooling reference. |
| `diag` | Compiler diagnostics. |
| `term` | Globally defined terms. |
| `rule` | Addressable semantic rules. |

Examples:

```text
manual.introduction
lang.functions.arguments
api.core.output.print
api.core.types.string
api.core.types.string.concat
diag.type.unknown-name
rule.call.arguments.left-to-right
term.callable
```

IDs are identities, not generated slugs. A source rename does not automatically change an ID. If an ID itself must change, the release owner records an explicit rename and redirect.

The default output URL replaces dots with slashes and appends `.html`. A deployment may map one configured landing ID to the site root, but other mappings remain deterministic.

All pages, rules, and terms share one global ID registry. Section and example IDs are local to their page and are addressed as `page-id#local-id`.

## 7. Record kinds

Format version 1 defines:

| Category | Kinds |
|---|---|
| Organizational | `manual`, `topic`, `namespace`, `index`, `glossary` |
| Language | `syntax`, `statement`, `expression`, `operator`, `literal`, `protocol` |
| Object/API | `descriptor`, `class`, `interface`, `trait`, `function`, `method-family`, `method`, `property`, `field`, `constant` |
| Tooling | `command`, `option`, `manifest-key`, `diagnostic` |

A new kind requires a format update. Unknown kinds are errors.

Entity kinds have a non-null `surface`. Organizational and conceptual language pages may use `surface: null`. A protocol that has a compiler-visible descriptor uses a surface; a purely explanatory protocol page does not pretend to have one.

## 8. Field ownership

Ownership is part of the format contract, not an implementation suggestion.

| Subtree or field | Owner | Sync behaviour |
|---|---|---|
| `format` | format | Never rewritten except by explicit migration. |
| `id` | release/identity | Never inferred from a changed symbol after creation. |
| `kind` | release/identity | Changed only through an explicit migration. |
| `surface` | compiler | Replaced from a matched compiler entity. |
| `lifecycle` | human/release | Never changed merely because a compiler entity appears or disappears. |
| `documentation.status` | human | Scaffold may initialize it; sync does not promote it. |
| Other `documentation` | human | Never semantically rewritten by sync. |
| `provenance.compiler` | compiler | Updated from the emitted snapshot. |
| `provenance.conformance` | compiler/tool plus review | Reconciled from verified evidence. |
| `provenance.specification` | human | Preserved and validated. |

A sync tool must preserve human-owned scalar spelling, Markdown block contents, comments, and ordering inside human-owned subtrees. It may canonicalize the compiler-owned `surface` and `provenance.compiler` subtrees.

A plain parse-and-reserialize implementation that reformats the whole file is non-conforming. The implementation must either edit a YAML concrete syntax tree or splice canonically serialized owned subtrees into the existing document without touching authored spans.

## 9. Compiler surface schema

### 9.1 Common entity fields

Every non-null `surface` begins with:

```yaml
surface:
  symbol: /core/output::print
  aliases:
    - print
  namespace: api.core.output
  owner: null
  visibility: public
  availability:
    targets:
      - all
    feature: null
  origin:
    category: compiler
    package: core
```

Fields:

| Field | Required | Meaning |
|---|---:|---|
| `symbol` | yes | Canonical Terrane-facing spelling. Never a Rust lowering name. |
| `aliases` | yes | Source-visible aliases. Empty sequence when none. |
| `namespace` | top-level entities | Namespace record ID. |
| `owner` | members | Owning descriptor, class, interface, trait, method family, or namespace ID. |
| `visibility` | yes | Canonical Terrane visibility. |
| `availability` | yes | Target and feature/profile restrictions known to the compiler. |
| `origin` | yes | Compiler, source package, dependency, adapter, or tool origin. |

Exactly one of `namespace` and `owner` is normally non-null for an API entity. Namespace root records may set both to `null`.

The compiler must derive these values from resolved semantic objects. It must not scrape Terrane source text, generated Rust, documentation comments, or demo files to infer the surface.

### 9.2 Type references

A type reference is structured rather than a presentation string:

```yaml
type:
  display: text-display
  entity: api.core.interface.text-display
  arguments: []
  nullable: false
```

Fields:

| Field | Meaning |
|---|---|
| `display` | Deterministic canonical source rendering. |
| `entity` | Principal descriptor/protocol ID when one exists. |
| `arguments` | Nested type references for constructors or composites. |
| `nullable` | Whether `none` is part of the contract, when this representation applies. |

Union, callable, reference, and other composite types should gain explicit tagged shapes rather than encoding their semantics only in `display`. `display` is for rendering and drift review; typed fields drive validation and indexing.

### 9.3 Callable signatures

Functions, methods, method families with a default invocation, class construction, and other callable entities expose signatures:

```yaml
surface:
  symbol: /core/output::print
  aliases:
    - print
  namespace: api.core.output
  owner: null
  visibility: public
  availability:
    targets:
      - all
    feature: null
  origin:
    category: compiler
    package: core

  signatures:
    - id: default
      form: call
      display: print; values...
      receiver: null
      parameters:
        - id: values
          name: values
          type:
            display: text-display
            entity: api.core.interface.text-display
            arguments: []
            nullable: false
          mode: variadic
          default: null
          passing: value
      returns:
        type:
          display: none
          entity: api.core.types.none
          arguments: []
          nullable: false
      throws: []
      contracts:
        asynchronous: false
        receiver-mutation: none
```

Signature rules:

- `id` is stable within the entity and is not derived from list position.
- `form` is `declaration`, `call`, `member`, `construct`, or `expression`.
- `display` is canonical source-facing synopsis text generated from the typed signature.
- Parameter IDs remain stable when a display name is renamed deliberately.
- Parameter `mode` is `required`, `optional`, or `variadic`.
- `default` is canonical source spelling or `null`.
- `passing` uses Terrane ownership vocabulary, not Rust ABI vocabulary.
- `returns` is always present, including `none` and `never`.
- `throws` is always a sequence. An empty sequence means the compiler has established no Terrane throwable outcome for the signature; absence of the field is invalid.
- Callable contracts retain orthogonal facts rather than collapsing them into a generic effect list.

A throwable entry has a stable local ID and a type:

```yaml
throws:
  - id: conversion-failure
    type:
      display: coercion-error
      entity: api.core.errors.coercion-error
      arguments: []
      nullable: false
```

The compiler may know the throwable type without knowing the best human explanation of its condition. That explanation belongs under `documentation.callables` keyed by signature and throwable ID.

### 9.4 Classes, interfaces, traits, and descriptors

Relationship fields are compiler-owned:

```yaml
surface:
  symbol: /example::connection
  aliases: []
  namespace: api.example
  owner: null
  visibility: public
  availability:
    targets:
      - all
    feature: null
  origin:
    category: package
    package: example

  extends: []
  implements:
    - api.core.interface.text-display
  uses: []
  construct-signature: default
  ownership: resource
```

Rules:

- A class has at most one `extends` entry; other kinds follow Terrane's object-model constraints.
- `implements` contains interface/protocol IDs.
- `uses` contains trait IDs.
- Members are discovered by reverse `owner` relationships. A class record does not duplicate a manually maintained member list.
- Construction references a signature on the class record when the class supports default invocation.
- Ownership and lifecycle facts use explicit Terrane categories.
- Inherited members remain owned by their declaring entity; generated views calculate inherited availability separately.

### 9.5 Properties, fields, and constants

A property or field surface includes its type and access contract:

```yaml
surface:
  symbol: connection.closed
  aliases: []
  namespace: null
  owner: api.example.connection
  visibility: public
  availability:
    targets:
      - all
    feature: null
  origin:
    category: package
    package: example

  value-type:
    display: bool
    entity: api.core.types.bool
    arguments: []
    nullable: false
  readable: true
  writable: false
  static: false
```

Constants additionally carry a canonical value representation only when that value is part of the source-visible contract and can be serialized without executing arbitrary code.

### 9.6 Diagnostics and tools

Compiler diagnostics, CLI commands, options, and manifest keys may be emitted through the same snapshot mechanism. Their `surface` uses kind-specific fields, for example:

```yaml
surface:
  symbol: T0001
  aliases: []
  namespace: null
  owner: null
  visibility: public
  availability:
    targets:
      - all
    feature: null
  origin:
    category: compiler
    package: terrane-compiler

  severity: error
  diagnostic-family: name-resolution
```

The explanation, rejected example, and correction remain authored documentation.

## 10. Lifecycle schema

Lifecycle is explicit and human-controlled:

```yaml
lifecycle:
  status: current
  stability: stable
  since: "0.1"
  deprecated-since: null
  removed-in: null
  replacement: null
```

Statuses:

| Status | Meaning |
|---|---|
| `planned` | Settled or exploratory design not present in the selected compiler surface. |
| `current` | Present in the selected published surface. |
| `deprecated` | Present but discouraged, with an explicit migration contract. |
| `removed` | Retained for historical lookup but absent from the selected current surface by decision. |

`status` may be `null` only in a newly generated scaffold whose
`documentation.status` is `missing`. This represents an unresolved release decision, not another
lifecycle state. It is an error in every publication profile.

`stability` is `experimental`, `stable`, or `null` for records where stability is inapplicable.

Rules:

- `current` and `deprecated` require `since`.
- `deprecated` requires `deprecated-since` and normally `replacement` or authored rationale.
- `removed` requires `removed-in` and retains its last known surface for historical rendering.
- `replacement` is a reference ID, never an external URL or prose label.
- An entity disappearing from a compiler snapshot does not change lifecycle status.
- A newly emitted entity does not become a complete public page merely because the compiler can describe it.
- Version strings are opaque quoted release identifiers interpreted by the selected release policy.

## 11. Documentation schema

### 11.1 Common fields

```yaml
documentation:
  status: complete
  title: print
  title-style: code
  summary: >-
    Writes the canonical text display of zero or more values followed by one
    newline.
  tags:
    - output
    - text-display
  callables: {}
  sections: []
  see-also: []
```

Fields:

| Field | Required | Meaning |
|---|---:|---|
| `status` | yes | `missing`, `draft`, or `complete`. |
| `title` | yes except a new scaffold | Plain display title. |
| `title-style` | yes | `text`, `code`, or another format-defined presentation enum. |
| `summary` | complete records | Short Markdown standfirst, normally one sentence. |
| `tags` | yes | Authored search terms; empty sequence when none. |
| `callables` | callable entities | Descriptions keyed to compiler-owned signature components. |
| `sections` | yes | Ordered authored content sections. |
| `see-also` | yes | Structured related-reference links. |

`documentation.status` is independent of lifecycle. A compiler-present entity may have missing documentation; a removed entity may retain complete historical documentation.

A public build includes only records whose lifecycle and documentation statuses satisfy its profile.

### 11.2 Callable documentation

Descriptions attach to stable signature, parameter, return, and throwable IDs without being stored inside the compiler-owned surface:

```yaml
documentation:
  callables:
    default:
      parameters:
        values: |-
          Values are evaluated from left to right and converted through their
          canonical text-display contracts.
      returns: |-
        Returns `none` after writing the line.
      throws: {}
```

Rules:

- The outer key is a signature ID.
- Parameter keys are parameter IDs, not display names.
- `returns` is Markdown.
- Throwable description keys are throwable IDs.
- Empty `throws` documentation is valid only when the compiler-owned throwable sequence is empty.
- Stale keys after a surface update are errors requiring review; the sync tool does not delete their prose.
- Missing descriptions may be warnings or errors according to the publication profile.

### 11.3 Sections and blocks

Sections are ordered and have stable local IDs:

```yaml
sections:
  - id: behaviour
    title: Behaviour
    blocks:
      - type: markdown
        markdown: |-
          The converted values are concatenated without an inserted separator.

      - type: rule
        id: rule.output.print.trailing-newline
        level: must
        markdown: |-
          Exactly one newline follows the concatenated display.

  - id: examples
    title: Examples
    blocks:
      - type: example
        id: multiple-values
        title: Print several values
        language: terrane
        mode: run
        source: |-
          namespace reference-examples/print-values

          function main;
            print; 'answer: ', 42
        response:
          kind: stdout
          language: text
          display: on-run
          content: |-
            answer: 42
```

Format version 1 block types are:

| Type | Purpose |
|---|---|
| `markdown` | Ordinary explanatory Markdown. |
| `table` | Authored tabular data with typed columns and validated rows. |
| `rule` | Addressable normative rule. |
| `grammar` | Formal Terrane grammar productions. |
| `example` | Structured source example and expected result. |
| `admonition` | Note, warning, implementation detail, experimental notice, or deprecation guidance. |
| `term` | Addressable term definition. |
| `entity-index` | Generated query over assembled entities. |
| `diagnostic` | Structured diagnostic condition where not represented by a dedicated record. |

Blocks are tagged unions. Fields not allowed for the selected `type` are errors.

### 11.4 Markdown blocks

A Markdown block is:

```yaml
- type: markdown
  markdown: |-
    Ordinary **Markdown** is allowed here, including lists, inline code, and
    fenced code blocks.
```

Markdown uses CommonMark 0.31.2 plus strikethrough. Raw HTML and Markdown table syntax are errors; authored tabular data uses a `table` block. Internal references use the syntax in §12. External links and local asset links use ordinary Markdown links.

### 11.5 Tables

Authored tabular data uses a dedicated block:

```yaml
- type: table
  id: structural-words
  title: Structural words
  show-header: true
  columns:
    - id: area
      title: Area
      cell: text
    - id: words
      title: Structural words
      cell: code-list
  rows:
    - area: Namespaces and imports
      words:
        - namespace
        - from
        - import
        - as
```

`id` and `title` may be `null`. Column IDs are unique within the table and determine the keys allowed in every row. Column order determines rendered order; row order is authored and preserved. Every row must provide exactly one value for every column, and an authored table must contain at least one column and one row.

Column `title` is required even when `show-header` is `false`. A hidden header remains available to accessibility tools, non-visual renderers, exports, and processors; the flag controls its visual presentation rather than discarding its meaning.

Format version 1 cell representations are:

| Cell | YAML value | Rendering |
|---|---|---|
| `text` | string | Plain text with no Markdown interpretation. |
| `markdown` | string | Markdown inline content; block constructs are forbidden. |
| `code` | string | One code-styled value. |
| `code-list` | sequence of strings | A renderer-joined list of separately code-styled values. |

Tables do not contain nested blocks, column spans, row spans, sorting expressions, or executable values. Add those only if a concrete reference page cannot be represented clearly without them.

### 11.6 Rules

```yaml
- type: rule
  id: rule.call.arguments.left-to-right
  level: must
  since: null
  evidence:
    - calls/evaluation-order
  markdown: |-
    The receiver is evaluated before member selection, and supplied arguments
    are then evaluated exactly once from left to right.
```

Rule IDs are globally unique. `level` is `must`, `should`, or `may`. Rule prose is normative. Evidence values are configured conformance case IDs.

Not every contractual sentence needs a rule block. Use one when a fact benefits from a stable link, independent evidence, or distinct lifecycle.

### 11.7 Grammar

```yaml
- type: grammar
  id: function-declaration
  notation: terrane-ebnf
  grammar: |-
    FunctionDeclaration = [ "async" ], "function", Identifier,
                          ReturnType, ";", [ ParameterList ], Block ;
```

The local block ID produces `page-id#function-declaration`. Format version 1 uses:

```text
Production = Expression ;          definition
A, B                               sequence
A | B                              choice
[ A ]                              zero or one
{ A }                              zero or more
A, { A }                           one or more
"text"                             literal source text
TOKEN                              separately defined lexical token
(* text *)                         grammar comment
```

Precedence is grouping, repetition/option, sequence, then choice. Empty alternatives are forbidden.

### 11.8 Examples

```yaml
- type: example
  id: multiple-values
  title: Print several values
  language: terrane
  mode: run
  target: null
  timeout-ms: null
  source: |-
    namespace reference-examples/print-values

    function main;
      print; 'answer: ', 42
  response:
    kind: stdout
    language: text
    display: on-run
    content: |-
      answer: 42
  diagnostic: null
  markdown: null
```

`language` is required and identifies the source language for rendering and verification. It is a lowercase identifier rather than a closed format-version enum; publication profiles register the languages and runners they support. Use `text` when no programming or data language applies. An unknown language is an error for executable modes and may fall back to plain rendering only for `illustrative`.

Modes:

| Mode | Contract |
|---|---|
| `illustrative` | Rendered but not claimed as accepted by a configured runner. |
| `check` | Must pass the selected language's configured checking pipeline. |
| `build` | Must produce its configured build artifact without warnings. |
| `run` | Must build and run successfully. |
| `reject` | Must fail with the stable code in `diagnostic`. |

An example may carry a structured response:

```yaml
response:
  kind: stdout
  language: text
  display: on-run
  content: |-
    answer: 42
```

Response `kind` is `stdout`, `diagnostic`, `source`, or `text`. Response `language` is required under the same rules as example source language, including explicit `text`. Display is `shown`, `on-run`, or `hidden`:

- `shown` renders the response immediately;
- `on-run` keeps it out of the initial presentation and displays it when the reader runs the example; a non-interactive renderer may provide an equivalent collapsed reveal;
- `hidden` retains the response for verification but does not publish it.

For a `run` example, a `stdout` response must match normalized standard output exactly. A `reject` example still requires the stable code in `diagnostic`; a rendered diagnostic response supplements rather than replaces that stable contract. Other response kinds are validated by the runner selected for the source language and publication profile.

Rules:

- `reject` requires `diagnostic`; other modes forbid it.
- A response is optional. When present, all four response fields are required.
- `markdown` provides optional explanation associated with the example.
- Examples are independent programs in format version 1.
- The processor never executes `illustrative` examples.
- Executable modes require a configured runner for `language`.
- Verification uses the real language pipeline, not a documentation-specific parser.

### 11.9 Admonitions

```yaml
- type: admonition
  kind: warning
  title: null
  markdown: |-
    This operation may discard information under the selected policy.
```

Kinds are `note`, `important`, `warning`, `implementation`, `experimental`, and `deprecated`. Status and lifecycle remain structured fields; an admonition cannot change them.

### 11.10 Terms

```yaml
- type: term
  id: term.callable
  name: callable
  markdown: |-
    A **callable** is an object that supports default invocation through the
    call marker.
```

Term IDs are globally unique and share the reference registry.

### 11.11 Entity indexes

```yaml
- type: entity-index
  query:
    owner: api.core.types.string
    kinds:
      - method
      - property
    statuses:
      - current
      - deprecated
  sort: symbol
  layout: table
```

At least one query constraint is required. Supported sort modes are `symbol`, `title`, and `manual`; layouts are `table`, `list`, and `compact`. Results come from the assembled IR. Authors do not maintain a second member list in Markdown.

### 11.12 Related references

```yaml
see-also:
  - id: lang.text-display
    label: Text display
  - id: api.core.types.string.concat
    label: null
```

`label: null` uses the target's title. The processor validates every target after profile selection.

## 12. Markdown cross-references

Markdown fields use one minimal custom inline syntax:

```markdown
See [[api.core.output.print]].
See [[api.core.output.print|`print`]].
See [[lang.functions.arguments#evaluation-order|evaluation order]].
See [[rule.call.arguments.left-to-right]].
```

The target before `|` is a global ID with an optional local `#section-or-block`. The optional label is Markdown inline content. Reference links cannot nest. Literal `[[` is escaped as `\[[`.

The default label is:

- the page title for a page;
- the canonical code-styled ID or configured short label for a rule;
- the defined term name for a term;
- the block title for a local example or section.

Unresolved targets, ambiguous redirects, filtered required targets, and references to non-public local IDs are errors. Normal Markdown links must not point to another reference YAML source file.

## 13. Provenance

```yaml
provenance:
  specification:
    - document: language-spec
      section: "9.6"
  conformance:
    - output/print
  compiler:
    semantic-id: core.output.print
    surface-digest: sha256:...
```

Ownership:

- `specification` is authored and validated against a configured source revision;
- `conformance` is reconciled from explicit case associations and reviewed evidence;
- `compiler` is emitted and updated by the compiler/sync tool;

A compiler digest detects drift; it is not an entity identity. A digest change triggers semantic comparison of the structured surface.

A complete current public entity should have authoritative specification or package-contract provenance and executable evidence where the contract is implemented and testable. The publication profile decides which omissions are fatal.

## 14. Conceptual language pages

A conceptual page uses the same envelope without inventing a compiler surface:

```yaml
format: 1
id: lang.functions.arguments
kind: topic

surface: null

lifecycle:
  status: current
  stability: stable
  since: "0.1"
  deprecated-since: null
  removed-in: null
  replacement: null

documentation:
  status: complete
  title: Function arguments
  title-style: text
  summary: >-
    Function calls bind positional, named, defaulted, and variadic arguments
    according to one deterministic order.
  tags:
    - calls
    - parameters
  sections:
    - id: evaluation-order
      title: Evaluation order
      blocks:
        - type: rule
          id: rule.call.arguments.left-to-right
          level: must
          since: null
          evidence:
            - calls/evaluation-order
          markdown: |-
            The receiver is evaluated before member selection, and supplied
            arguments are evaluated exactly once from left to right.
    - id: examples
      title: Examples
      blocks: []
  see-also:
    - id: api.core.types.function
      label: Function objects

provenance:
  specification:
    - document: language-spec
      section: "13"
  conformance:
    - calls/evaluation-order
  compiler: null
```

Language pages can still be updated with compiler assistance: the processor can validate grammar, examples, diagnostics, and conformance links. The compiler does not own their explanatory rule text merely because it implements those rules.

## 15. Complete entity example

A complete `print` record illustrates how structured surface and Markdown documentation join:

```yaml
format: 1
id: api.core.output.print
kind: function

surface:
  symbol: /core/output::print
  aliases:
    - print
  namespace: api.core.output
  owner: null
  visibility: public
  availability:
    targets:
      - all
    feature: null
  origin:
    category: compiler
    package: core
  signatures:
    - id: default
      form: call
      display: print; values...
      receiver: null
      parameters:
        - id: values
          name: values
          type:
            display: text-display
            entity: api.core.interface.text-display
            arguments: []
            nullable: false
          mode: variadic
          default: null
          passing: value
      returns:
        type:
          display: none
          entity: api.core.types.none
          arguments: []
          nullable: false
      throws: []
      contracts:
        asynchronous: false
        receiver-mutation: none

lifecycle:
  status: current
  stability: stable
  since: "0.1"
  deprecated-since: null
  removed-in: null
  replacement: null

documentation:
  status: complete
  title: print
  title-style: code
  summary: >-
    Writes the canonical text display of zero or more values followed by one
    newline.
  tags:
    - output
    - text-display
  callables:
    default:
      parameters:
        values: |-
          Values are evaluated from left to right and converted through their
          canonical text-display contracts.
      returns: |-
        Returns `none` after writing the line.
      throws: {}
  sections:
    - id: behaviour
      title: Behaviour
      blocks:
        - type: rule
          id: rule.output.print.concatenation
          level: must
          since: null
          evidence:
            - output/print
          markdown: |-
            Converted values are concatenated without an inserted separator,
            and exactly one newline follows the result.
    - id: examples
      title: Examples
      blocks:
        - type: example
          id: multiple-values
          title: Print several values
          language: terrane
          mode: run
          target: null
          timeout-ms: null
          source: |-
            namespace reference-examples/print-values

            function main;
              print; 'answer: ', 42
          response:
            kind: stdout
            language: text
            display: on-run
            content: |-
              answer: 42
          diagnostic: null
          markdown: null
  see-also:
    - id: lang.text-display
      label: Text display

provenance:
  specification:
    - document: language-spec
      section: "9.6"
  conformance:
    - output/print
  compiler:
    semantic-id: core.output.print
    surface-digest: sha256:example
```

IDs and case names in this example illustrate the format and become binding only when those registries exist.

## 16. Manual navigation

`manual.yaml` defines authored navigation separately from entity relationships:

```yaml
format: 1
title: Terrane Reference
landing: manual.introduction
navigation:
  - page: manual.introduction
  - group: Language
    children:
      - page: lang.lexical-structure
      - page: lang.functions.arguments
  - group: Core API
    children:
      - page: api.core.output
      - page: api.core.types.string
  - generated:
      title: Diagnostics
      query:
        kinds:
          - diagnostic
        statuses:
          - current
      sort: symbol
```

Rules:

- A `page` item references exactly one record.
- A `group` is a label and does not create a page.
- A `generated` item declares a deterministic query.
- Every published non-member page must be reachable once from navigation unless marked as intentionally index-only by the format.
- Member pages may be reached through generated owner indexes without all appearing in the global sidebar.
- Navigation order does not imply namespace, ownership, inheritance, or lifecycle.
- Previous/next links follow the expanded navigation order.

## 17. Compiler snapshot

The compiler emits a deterministic snapshot from the resolved semantic model:

```yaml
format: 1
compiler-version: "..."
profile:
  target: native
  features: []
entities:
  - semantic-id: core.output.print
    reference-id: api.core.output.print
    kind: function
    surface: {}
    provenance: {}
```

Requirements:

- Emission reuses the same semantic model as `check`, `rust`, `build`, and `run`.
- It does not create a command-specific parser or resolver.
- Every emitted entity has a stable compiler semantic ID.
- Compiler-owned reference IDs are assigned deliberately in compiler metadata; they are not regenerated from display symbols on each run.
- Entities are sorted by reference ID.
- Maps with semantically unordered content use canonical key order.
- No wall-clock time, host path, random ID, or directory traversal order enters the snapshot.
- Target/profile selection is explicit and recorded.
- Projected dependency entities retain their Terrane projection spelling and package provenance.
- Unsupported or unrepresentable dependency surfaces are omitted with structured reasons rather than emitted as plausible incomplete entities.

A snapshot describes one selected compiler/profile surface. It is not itself the historical manual and cannot make lifecycle decisions.

## 18. Reconciliation

A conceptual command such as:

```text
terrane reference sync <snapshot> <reference-root>
```

compares the compiler snapshot with canonical records.

Default invocation is read-only and emits a semantic change report. A separate `--write` action applies reviewable changes.

### 18.1 Matching

Matching order is:

1. exact stable reference ID;
2. explicit rename mapping in `lifecycle/renames.yaml`;
3. otherwise unmatched.

Symbol similarity is diagnostic evidence only. The tool must not infer a rename solely because an old and new symbol look alike.

### 18.2 Newly emitted entity

For an unmatched compiler entity, sync may create a scaffold:

```yaml
format: 1
id: api.core.types.string.partition
kind: method
surface: {}
lifecycle:
  status: null
  stability: null
  since: null
  deprecated-since: null
  removed-in: null
  replacement: null
documentation:
  status: missing
  title: null
  title-style: null
  summary: null
  tags: []
  callables: {}
  sections: []
  see-also: []
provenance: {}
```

The compiler-owned fields are filled from the snapshot. Human-owned unknowns remain `null` or
`missing`; the report may recommend `current` and a title style without writing either. Such a
scaffold cannot enter a public build until reviewed.

### 18.3 Changed entity

For a matched entity, sync computes a typed diff:

```text
api.core.types.string.concat
  signature default
    parameter values
      type: string -> text-display
```

With `--write`, it replaces the compiler-owned surface and compiler provenance. It then validates authored attachments:

- descriptions keyed by retained signature and parameter IDs remain attached;
- descriptions keyed by disappeared IDs are retained but reported as stale;
- new signature components without documentation are reported as missing;
- lifecycle and prose are unchanged;
- a changed canonical symbol is reported prominently even when the stable identity matches.

### 18.4 Missing entity

When a canonical `current` or `deprecated` record has no snapshot match, sync stops with an unresolved lifecycle event. It does not delete the record, empty its surface, or mark it removed.

The reviewer must choose one of:

- record an explicit rename;
- confirm a target/profile distinction;
- correct a compiler regression or snapshot configuration;
- mark the entity `removed` with `removed-in` and optional replacement;
- mark a planned record appropriately if it was never part of the selected compiler surface.

A removed record retains its last known surface and documentation for historical rendering.

### 18.5 Explicit rename

`lifecycle/renames.yaml` uses stable IDs:

```yaml
format: 1
renames:
  - from: api.core.output.write-line
    to: api.core.output.print
    in: "0.3"
    preserve-redirect: true
```

A rename cannot target an existing unrelated identity. Redirects are generated from the mapping. The destination record owns the current surface; historical rendering may retain the source record according to policy.

### 18.6 Report

A sync report groups:

```text
added
changed
renamed
missing-from-compiler
stale-documentation
missing-documentation
lifecycle-conflicts
profile-only-differences
unchanged
```

Every item carries stable IDs and field paths. A machine-readable report uses the same typed paths as the record schema.

## 19. Assembly and rendering

The manual processor:

1. parses all YAML while retaining source spans and comments;
2. validates local record schemas;
3. builds the global ID and redirect registry;
4. resolves owners, namespaces, inheritance, interfaces, traits, and type references;
5. joins lifecycle, documentation, provenance, and selected compiler/profile facts;
6. validates Markdown references and local IDs;
7. verifies examples when explicitly requested by the build workflow;
8. expands navigation and entity-index queries;
9. creates the assembled reference IR;
10. renders HTML, search data, indexes, print views, and optional machine-readable output.

### 19.1 Generated entity page shape

For a function or method, the default renderer produces:

```text
title and summary
availability and lifecycle
canonical symbol and aliases
signature synopsis
parameters with authored descriptions
return contract and description
throwable outcomes and descriptions
authored sections in order
related references
provenance/source links
```

For a class, interface, trait, or descriptor:

```text
title and summary
availability and lifecycle
canonical symbol and aliases
inheritance, interfaces, traits, and ownership
construction synopsis
properties and fields from reverse owner lookup
methods and method families from reverse owner lookup
authored sections in order
related references
provenance/source links
```

For a conceptual page, the renderer uses the authored sections directly and adds navigation, lifecycle, provenance, and indexes.

### 19.2 Generated outputs

A default build provides:

- browsable manual navigation and breadcrumbs;
- stable canonical URLs and redirects;
- previous/next navigation;
- local section contents;
- source-facing synopses;
- parameter, return, and throwable presentations;
- owner/member and inheritance indexes;
- namespace indexes;
- glossary and rule indexes;
- diagnostic index;
- search by ID, title, symbol, alias, term, heading, summary, tag, and diagnostic code;
- a printable no-JavaScript reading surface;
- machine-readable assembled IR for editors and other tools;
- a reconciliation and example-evidence report.

Search ranks exact canonical symbols and aliases above prose matches. Excluded profiles do not leak planned or removed material into results.

## 20. Publication profiles

A publication profile selects:

- Terrane release;
- compiler surface snapshot;
- target and feature profile;
- lifecycle statuses;
- accepted stability levels;
- required documentation completeness;
- whether historical removed pages are emitted;
- example-verification evidence policy.

Typical behaviour:

| Lifecycle | Public current manual | Design preview | Historical manual |
|---|---:|---:|---:|
| `planned` | excluded | included | optional |
| `current` | included | included | version-dependent |
| `deprecated` | included | included | included |
| `removed` | redirect or excluded | optional | included |

Filtering operates on complete records and generated query results. The processor does not conditionally delete arbitrary paragraphs from Markdown. Target- or release-specific prose requires separate structured variation support in a later format version rather than ad hoc template conditions.

A current page must not rely on a filtered planned page for required semantics. Such cross-profile dependencies are validation errors.

## 21. Validation

Diagnostics use stable `R` codes and include record path, YAML path, line, and column where available.

| Range | Category |
|---|---|
| `R0001`–`R0099` | YAML and record syntax |
| `R0100`–`R0199` | IDs, symbols, and redirects |
| `R0200`–`R0299` | record-kind and field shape |
| `R0300`–`R0399` | ownership, types, and entity relationships |
| `R0400`–`R0499` | Markdown links, sections, and navigation |
| `R0500`–`R0599` | lifecycle and publication profiles |
| `R0600`–`R0699` | compiler reconciliation and surface drift |
| `R0700`–`R0799` | examples and conformance evidence |
| `R0800`–`R0899` | assets, security, and rendering safety |

A public build fails on:

- invalid YAML or unknown fields;
- duplicate IDs, symbols, semantic identities, or local IDs;
- unresolved owners, namespaces, type references, links, or redirects;
- relationship targets of the wrong kind;
- object-model cycles forbidden by Terrane;
- current/deprecated lifecycle inconsistent with the selected snapshot;
- incomplete required lifecycle metadata;
- `documentation.status` other than `complete` for included public pages;
- stale callable documentation keys;
- missing required callable descriptions under a strict profile;
- invalid or failed required example evidence;
- navigation duplication or unreachable required pages;
- raw HTML, unsafe URLs, missing assets, or source-root escapes.

A strict quality profile additionally requires:

- specification or package-contract provenance;
- conformance evidence for implemented observable contracts where applicable;
- checked accepted and plausible rejected examples for materially documented language boundaries;
- a summary within the configured search length;
- explicit local IDs for linkable sections;
- deprecation migration guidance;
- no hand-maintained member list duplicating assembled IR queries.

## 22. Determinism

An assembled reference build records:

- record-format version;
- compiler snapshot format and compiler version;
- processor version;
- selected release and publication profile;
- sorted input paths and content hashes;
- lifecycle rename map hash;
- example target/profile selections;
- assembled IR hash.

Semantic output must not depend on wall-clock timestamps, host paths, random values, directory iteration, YAML map insertion accidents, or process locale. Human deployment timestamps may be added outside the semantic build.

Generated lists sort by explicit navigation order or Unicode code-point order over canonical source spellings, as selected by the query. Sorting policy is recorded rather than inherited from the host locale.

## 23. Security and accessibility

The processor:

- never executes YAML tags, Markdown, or attribute values;
- rejects raw HTML and unsafe URL schemes;
- never fetches remote content during assembly;
- sanitizes active assets according to explicit policy;
- escapes all authored content at the renderer boundary;
- runs verified examples only in an isolated temporary package without network access and under resource limits;
- never follows a source or asset path outside the configured root.

Renderers preserve semantic heading order, visible keyboard focus, table headers, code-language labels, and textual admonition labels. Images require alt text unless marked decorative. Colour is never the only status or warning signal. Generated relationship diagrams have equivalent text lists.

## 24. Authoring guidance

Reference authors should:

1. Put compiler-known facts in `surface`, never in duplicated Markdown tables.
2. Put explanations and consequences in Markdown documentation fields.
3. Attach parameter and throwable prose through stable local IDs, not source list positions.
4. In public language and entity records, state observable Terrane behaviour rather than Rust implementation details.
5. In internals records, document durable current responsibilities, boundaries, invariants, formats, and implementation evidence without presenting them as public language APIs.
6. Use an `implementation` admonition in a public record when lowering details are genuinely useful but do not warrant their own internals topic.
7. Give each semantic or internal contract one authoritative home and link to it elsewhere.
8. Keep examples focused on one contract.
9. Distinguish accepted, runnable, rejected, and illustrative examples honestly.
10. Describe plausible negative boundaries, not only successful forms.
11. Distinguish `none`, empty data, iteration end, cancellation, throwable failure, and panic according to Terrane semantics.
12. Never describe planned behaviour as current merely because it exists in the design specification.
13. Never mark a missing compiler entity removed without an explicit lifecycle decision.
14. Avoid time-relative prose such as “currently” and “soon”; use lifecycle and release fields.
15. Use generated indexes rather than copied member inventories.
16. Keep entity pages useful when opened from search without duplicating their owner's general contract.

## 25. Format evolution

`format` versions the YAML reference-record syntax, not the Terrane language. A processor supports only declared versions and fails clearly on newer ones.

A backwards-compatible addition may introduce an optional field only if older processors already reject it rather than silently misrender it. Removing a field or changing its meaning requires a new integer version and a mechanical migration path.

The compiler snapshot format is versioned separately from canonical records. The sync tool owns explicit migrations between supported snapshot versions and the current record format.

Deferred until concrete need justifies them:

- localization and translated-record identity;
- reusable prose includes;
- prose-level target and version conditions;
- shared multi-file example fixtures;
- user-contributed notes;
- interactive playground execution;
- arbitrary renderer components;
- automatic ingestion of undocumented third-party prose;
- lifecycle decisions inferred from compiler absence.

The durable rule is: **the compiler owns what the surface is, humans own what it means and how its lifecycle changes, YAML carries the joined reference model, and Markdown carries prose inside that model.**