## 🚀 Main Features

* **Assisted Test Generation:** From a natural language description, the AI generates the initial test cases.
* **Automated Red-Green-Refactor Cycle:**
* 🔴 **Red:** Creation of robust tests that initially fail.
* 🟢 **Green:** Suggestion of the minimum viable code to pass the tests.
* 🔵 **Refactor:** Intelligent analysis to improve code readability, maintainability, and performance.


* **Language Agnostic:** Patterns and workflows adaptable to multiple programming languages (Python, JavaScript/TypeScript, Java, Go, etc.).
* **Easy Integration:** Designed to be incorporated into your current repositories and pipelines.

## 📋 Prerequisites

To get the most out of this workflow, it is recommended to have:

* Basic knowledge of agile methodologies and TDD.
* An execution environment compatible with your usual testing tools (e.g., Jest, PyTest, JUnit).
* (Optional) Access to Large Language Model (LLM) APIs such as OpenAI, Claude, or a local model (e.g., Llama 3) for automation.

## 🛠️ Installation and Setup

1. **Clone the repository to your local machine:**
```bash
git clone https://github.com/javisan81/aiTDDWorkflow.git
cd aiTDDWorkflow

```


2. **Review the internal documentation:**
Explore the `/docs` folder (if available) or the base scripts to adapt the workflow to your environment.
3. **Environment Setup:**
If you use automated scripts from this repository, make sure to install the necessary dependencies and initialize your environment variables (e.g., `.env` with your API keys).

## 🔍 Optional: Semantic Code Search (qdrant-rag)

This workspace supports **semantic code search** via a local Qdrant vector database, integrated with GitHub Copilot CLI through the `qdrant-rag` MCP server. This is **entirely optional** but significantly improves code navigation in large codebases.

### Stack

| Component | Purpose |
|---|---|
| [Docker](https://www.docker.com/) | Runs the Qdrant container |
| [Qdrant](https://qdrant.tech/) | Local vector database that stores code embeddings |
| [qdrant-rag MCP server](https://github.com/feuerdev/qdrant-rag-mcp) | MCP server that indexes code and exposes semantic search to Copilot |

### Installation

**1. Start Qdrant locally with Docker:**
```bash
docker run -d --name qdrant \
  -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

**2. Install the qdrant-rag MCP server:**
```bash
npm install -g qdrant-rag-mcp
```

**3. Register it in your Copilot CLI MCP config** (`~/.copilot/mcp.json` or equivalent):
```json
{
  "mcpServers": {
    "qdrant-rag": {
      "command": "npx",
      "args": ["qdrant-rag-mcp"],
      "env": {
        "QDRANT_URL": "http://localhost:6333"
      }
    }
  }
}
```

**4. Index the sub-projects** (first time only — see `AGENTS.md` for the full collection map):
```bash
# Example for one sub-project:
# Use the qdrant-rag index_codebase tool via Copilot CLI, pointing at the sub-project path.
# Never index from the repo root — the root .gitignore blocks everything.
```

### Usage

Once installed, Copilot agents will automatically use `reindex_changes` at the start of each session (as instructed in `AGENTS.md`) and will prefer semantic search over `grep` for conceptual queries.

---

## 💻 Basic Usage

The core of `aiTDDWorkflow` relies on discipline. When facing a new requirement:

1. **Define the expected behavior:** Use your AI assistant (or a script from this repository) by providing a clear prompt about what the system should do.
2. **Run the Test:** Verify that the test fails (Red).
3. **Implement with AI:** Ask the AI to solve the failure and provide the implementation (Green).
4. **Refactor:** Request code optimization and clean-up (Refactor).

*Example AI prompt:*

> "Write a PyTest test case for a function `calculate_discount(price, percentage)` that validates that the final price is not negative."

---

*Developed and maintained by [javisan81](https://github.com/javisan81).*