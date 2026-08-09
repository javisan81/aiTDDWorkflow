---
name: gradle-tests
description: Run all tests in a Gradle project and produce structured failure reports.
---

# /gradle-tests Skill

Use the repository tool `.github/tools/gradle/run-tests.sh` to execute a Gradle test task and
produce machine-readable results grouped by test name.

## Usage

From the repository root:

```bash
.github/tools/gradle/run-tests.sh <project-directory>
```

Optional arguments:

```bash
.github/tools/gradle/run-tests.sh <project-directory> <gradle-task> <output-directory>
```

The default task is `test`. The command is optimized for coding agents:

- Runs the project's `./gradlew` wrapper.
- Prints only a compact result summary and failed-test diagnostics.
- Writes the raw output to `gradle.log`.
- Writes structured results to `test-results.json`.
- Returns Gradle's exit code, so failures can be detected by automation.

Use `--verbose` only when the complete Gradle output is needed:

```bash
.github/tools/gradle/run-tests.sh <project-directory> test build/gradle-test-report --verbose
```

## Structured output

`test-results.json` contains:

- `status`: `passed`, `failed`, or `no-results`.
- `summary`: total, passed, failed, skipped, and errored counts.
- `failed_tests`: failed tests with their class, name, failure details, and
  `system_out`/`system_err` logs. Each failure includes a
  `diagnostic_category` such as `assertion`, `exception`, `timeout`,
  `external_dependency`, or `compilation`.
- `raw_log`: path to the complete Gradle output.

## Understanding failures

When tests fail, do not stop at the test name or the Gradle exit code. For each
entry in `failed_tests`:

1. Read `message` first. For assertions, identify the expected value and the
   actual value.
2. Read `details` as the primary stack trace and exception context. Find the
   first application or test source location, not only framework internals.
3. Inspect `logs.system_out` and `logs.system_err` for request payloads, setup
   data, external-service responses, and additional test context.
4. Use `diagnostic_category` as a starting point, not as proof. Explain the
   likely cause using the concrete evidence from the failure and distinguish
   confirmed facts from hypotheses.
5. Group repeated failures by common exception, source location, or dependency
   so the agent reports root causes instead of repeating symptoms.

The result should explain, for every failed test: what was expected, what
actually happened, where it failed, and the most likely reason it failed.

For a passing run, the agent should normally use only the single-line summary
from stdout. The full log and JSON report should be opened only when the
summary indicates failures or when more context is required.

The parser can also be run independently:

```bash
.github/tools/gradle/parse-test-results.py \
  --results-dir <project-directory>/build/test-results \
  --task test
```

## Subagent execution

This skill must run in a dedicated subagent, including when Gradle verification
appears small or straightforward. Return the one-line result for a passing
run. For failures, return only the failed test lines and report paths; inspect
the full log or JSON report only when diagnosing a failure.
