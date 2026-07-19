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