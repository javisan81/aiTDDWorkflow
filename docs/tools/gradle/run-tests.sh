#!/usr/bin/env bash
set -o pipefail

usage() {
  echo "Usage: $0 <project-dir> [gradle-task] [output-dir] [--verbose]" >&2
}

PROJECT_DIR="${1:-}"
TASK="${2:-test}"
OUTPUT_DIR="${3:-}"
VERBOSE="${4:-}"

if [[ -z "$PROJECT_DIR" ]]; then
  usage
  exit 2
fi

PROJECT_DIR="$(cd "$PROJECT_DIR" 2>/dev/null && pwd)" || {
  echo "Project directory does not exist: $1" >&2
  exit 2
}

if [[ ! -x "$PROJECT_DIR/gradlew" ]]; then
  echo "Executable Gradle wrapper not found: $PROJECT_DIR/gradlew" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${OUTPUT_DIR:-$PROJECT_DIR/build/gradle-test-report}"
mkdir -p "$OUTPUT_DIR"

RAW_LOG="$OUTPUT_DIR/gradle.log"
JSON_REPORT="$OUTPUT_DIR/test-results.json"

if [[ "$VERBOSE" == "--verbose" ]]; then
  (
    cd "$PROJECT_DIR" || exit 2
    ./gradlew "$TASK" --console=plain 2>&1
  ) | tee "$RAW_LOG"
  GRADLE_EXIT_CODE=${PIPESTATUS[0]}
else
  (
    cd "$PROJECT_DIR" || exit 2
    ./gradlew "$TASK" --console=plain >"$RAW_LOG" 2>&1
  )
  GRADLE_EXIT_CODE=$?
fi

set +e
python3 "$SCRIPT_DIR/parse-test-results.py" \
  --results-dir "$PROJECT_DIR/build/test-results" \
  --task "$TASK" \
  --raw-log "$RAW_LOG" \
  --output "$JSON_REPORT" \
  --agent-summary
PARSER_EXIT_CODE=$?
set -e

if [[ "$PARSER_EXIT_CODE" -ne 0 && "$GRADLE_EXIT_CODE" -eq 0 ]]; then
  exit "$PARSER_EXIT_CODE"
fi
exit "$GRADLE_EXIT_CODE"
