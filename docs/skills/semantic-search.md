---
name: semantic-search
description: Use Qdrant for conceptual code search and incremental project indexing.
---

# Semantic search

Use Qdrant when it is available and a conceptual or cross-cutting code search
would be more effective than a literal search.

1. Identify the active sub-project before indexing.
2. Run `reindex_changes` for an already indexed sub-project at the sub-project
   path, never at the monorepo root.
3. Use `index_codebase` with `forceReindex: true` only when the collection has
   never been indexed or was deleted.
4. When creating a collection, pass ignore patterns matching the repository's
   `.ragignore`.
5. Do not use Qdrant as a reason to duplicate a direct `rg`, `glob`, or file
   read that already answers the question.

