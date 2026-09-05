---
name: semantic-search
description: Use Qdrant and graphify for conceptual code search and incremental project indexing.
---

# Semantic search

Use Qdrant when it is available and a conceptual or cross-cutting code search
would be more effective than a literal search.
Use Graphify when it is available to read the correct information.

## 2. Graphify
Take into account graphify has graphs in each subproject, execute it at that subproject level. 
For example searchBrowseBff is indexed and there is a graphify-out directory inside it. The rest of projects follow the same pattern.

- BEFORE running file search commands (`find`, `grep`, `glob`) or reading codebase files, ALWAYS query Graphify first.
- Check the local AST graph in each subproject (`graphify` / `graph.json`) to trace dependencies, type hierarchies, and caller relationships.
- DO NOT read full source files to inspect class definitions or method signatures. Extract them directly from the Graphify schema.
- ONLY read complete files on disk if you need to inspect the internal implementation logic of a specific method identified via Graphify.

## Qdrant
1. Identify the active sub-project before indexing.
2. Run `reindex_changes` for an already indexed sub-project at the sub-project
   path, never at the monorepo root.
3. Use `index_codebase` with `forceReindex: true` only when the collection has
   never been indexed or was deleted.
4. When creating a collection, pass ignore patterns matching the repository's
   `.ragignore`.
5. Do not use Qdrant as a reason to duplicate a direct `rg`, `glob`, or file
   read that already answers the question.

