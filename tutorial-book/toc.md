# Proposed table of contents

## Introduction

- Who this book is for
- What this book will teach
- What this book deliberately leaves to the reference
- How to read the examples
- Terrane's continuum of competence

## 1. A First Taste of Terrane

- What Terrane is for
- Installing the toolchain
- Your first program
- Running a source file
- The edit, check, and run cycle
- Reading a compiler diagnostic
- A slightly more useful program
- Where Terrane fits between scripting and systems programming

## 2. Values, Names, and Everyday Expressions

- Numbers, truth values, and text
- Giving a value a name
- Changing a binding
- Arithmetic and comparisons
- Member access with `.`
- Calling with `;`
- Nested calls and parentheses
- Comments and readable layout
- Everything is an object—semantically
- **Why Terrane:** Why calls use `;`

## 3. Making Decisions and Repeating Work

- Choosing with `if` and `else`
- Combining conditions
- Repeating with `while`
- Iterating with `for`
- Ranges and ordinary iteration
- `break` and `continue`
- Loop-local names
- Choosing the clearest loop
- A small number-classification program

## 4. Functions: Giving Work a Name

- Defining and calling a function
- Parameters and results
- Required, optional, and named arguments
- Returning early
- Local scope
- Passing functions as values
- Small functions that compose
- Turning the number classifier into a program
- **Terrane style:** Express contracts, not ceremony

## 5. Text, Lists, and Maps

- Working with strings
- Multiline text
- Creating and changing lists
- Iterating over collections
- Looking values up in maps
- Building collections from existing values
- Choosing the right collection
- Value behavior during ordinary assignment
- A word-frequency program over a text value
- **Why Terrane:** Values do not alias by accident

## 6. Building a Complete Program

- Starting from a user story
- Dividing the program into functions
- Modeling the program's data
- Validating values
- Reporting useful output
- Keeping decisions separate from presentation
- Checking and testing behavior
- Growing the program without losing its shape
- Project: a small in-memory reporting tool

## 7. Errors Are Part of the Program

- Mistakes, failures, and exceptional conditions
- Throwing an error
- Handling errors with `try` and `catch`
- Cleaning up with `finally`
- Letting an error travel to the right layer
- Replacing and preserving errors
- Designing useful error values
- When not to catch an error
- Improving the reporting tool's failures

## 8. Organizing Code with Namespaces and Imports

- Splitting a program across source files
- Declaring a namespace
- Importing selected names with `from ... import`
- Relative and rooted namespace paths
- Renaming an import
- Declaring a dependency with `use`
- How the package manifest bounds source discovery
- Designing a small public surface
- Turning the reporting tool into a multi-file package
- **Why Terrane:** Imports do not flood your namespace

## 9. Classes, Interfaces, and Traits

- Objects as behavior
- Defining a class
- Constructing an instance
- Typed fields and ordinary methods
- Initialization with `construct`
- Cleanup with `destruct`
- Encapsulation and visibility
- Extending one base class
- Describing shared behavior with an interface
- Reusing fields and methods with traits
- Designing an object that earns its existence
- Project: model a small task list
- **Under the surface:** The object model is a semantic abstraction

## 10. Types When You Want Guarantees

- Starting with inference
- Adding a type where it communicates intent
- Typed parameters and results
- Types as executable contracts
- Numeric types and conversions
- Optional and alternative values
- Narrowing a value safely
- Interfaces for callable and object behavior
- Reading and fixing a type diagnostic
- Strengthening the task-list program gradually
- **Why Terrane:** Types are optional but real
- **Why Terrane:** `int` does not overflow silently

## 11. Values, Shared Identity, and Movement

- Ordinary assignment first
- Independent logical values
- Copy-on-write behavior in practice
- Sharing identity explicitly with `ref`
- Shared references and ownership
- Transferring a value with `move`
- When a value is no longer available
- Lifetimes without annotation clutter
- Choosing between assignment, `ref`, and `move`
- Common designs that do not need references
- **Terrane style:** Make identity part of the model only when it matters

## 12. Asynchronous Work and Structured Concurrency

- When a program should be asynchronous
- Declaring and awaiting asynchronous work
- Task scopes
- Spawning work within a scope
- Joining tasks and observing outcomes
- Cancellation and deadlines
- Why every task must be consumed
- Threaded and cooperative executor profiles
- Project: process several values concurrently
- **Why Terrane:** Async work is structured


## 13. How Terrane Becomes a Native Program

- From Terrane source to an executable
- The semantic model between source and Rust
- Reading generated Rust
- Source locations and diagnostics across lowering
- Debug and release builds
- What optimization may erase
- Why a Terrane object need not become a Rust object
- Behavior is the contract; representation is a compiler decision
- Debugging at the Terrane and Rust levels
- The continuum of competence: from Terrane user to native-code investigator

## 14. Writing Terrane-Shaped Programs

- Prefer the ordinary operation
- Let inference remove noise
- Use types to state real contracts
- Pass values unless identity matters
- Give errors an appropriate owner
- Use iteration rather than managing indexes
- Keep concurrency within a scope
- Favor readable generated behavior over clever source tricks
- Refactoring the book's project as a whole

## 15. A Larger Program, Step by Step

- Choosing a manageable application
- Sketching behavior before structure
- Establishing the package layout
- Modeling the core values
- Writing the first vertical slice
- Adding collections and iteration
- Adding structured error handling
- Adding classes and an interface
- Adding an explicit ownership boundary
- Adding concurrent work where it helps
- Testing observable behavior
- Inspecting the generated Rust
- Building and running the finished application
- What we deliberately did not build

## 16. Where to Go Next

- Navigating the language reference
- Reading compiler diagnostics as guidance
- Exploring generated Rust
- Profiling and debugging native programs
- Standard facilities as they become available
- Going lower: Rust, ABI types, and foreign boundaries
- Specialized and deferred territory
- Contributing packages
- Contributing to Terrane
- Continuing the continuum of competence

## Appendices

### A. Installing Terrane on Supported Platforms

- Toolchain requirements
- Editor integration
- Updating and troubleshooting

### B. The Commands Used in This Book

- `terrane check`
- `terrane rust`
- `terrane build`
- `terrane run`
- Package manifests and `use` declarations

### C. A Reader's Syntax Map

- Bindings and assignment
- Calls and member access
- Function declarations
- Control flow
- Imports and namespaces
- Types, `ref`, and `move`
- Error handling
- Async forms

### D. Answers and Further Experiments

- Chapter exercises
- Alternative solutions
- Ideas for extending the projects

### E. From Tutorial to Reference

- Topic-by-topic pointers into the language and package references
- Features intentionally not taught in the main progression

### F. Beyond the Tutorial

- Standard streams, files, paths, processes, and command-line parsing
- Documents, networking, time, and structured logging
- Native Rust and foreign-runtime boundaries
- Raw addresses and ABI-level facilities
- Deliberately deferred features: generators, labels and `goto`, hot-code replacement, `no_std`, embedded, firmware, and kernel targets
