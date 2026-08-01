#!/bin/bash
# PostToolUse hook: runs style_checker.py on any .md file edited by Claude Code.
# Receives tool name, input, and response as JSON on stdin.

input=$(cat)

file_path=$(printf '%s' "$input" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('tool_input', {}).get('file_path', ''))
" 2>/dev/null)

# Exit silently for non-.md files
[[ "$file_path" != *.md ]] && exit 0

# Resolve relative paths against the project root
if [[ "$file_path" != /* ]]; then
    file_path="$CLAUDE_PROJECT_DIR/$file_path"
fi

echo "--- style check: ${file_path#"$CLAUDE_PROJECT_DIR/"} ---"
python3 "$CLAUDE_PROJECT_DIR/style_checker.py" "$file_path"
exit 0
