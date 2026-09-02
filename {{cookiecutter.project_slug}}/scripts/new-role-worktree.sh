#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: $0 <task-id> <specifier|coder|cleaner|architect|hardener|qa> [base-ref]" >&2
  exit 2
fi
task_id="$1"
role="$2"
base_ref="${3:-HEAD}"
if [[ ! "$task_id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$ ]]; then
  echo "invalid task id: use 1-64 letters, digits, dot, underscore, or hyphen" >&2
  exit 2
fi
case "$role" in
  specifier|coder|cleaner|architect|hardener|qa) ;;
  *) echo "unknown role: $role" >&2; exit 2 ;;
esac
if ! root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  echo "not a Git repository; run git init, add files, and create an initial commit first" >&2
  exit 2
fi
if ! git -C "$root" rev-parse --verify --quiet "${base_ref}^{commit}" >/dev/null; then
  echo "base ref is not a commit: $base_ref" >&2
  exit 2
fi
if [[ -n "$(git -C "$root" status --porcelain=v1 --untracked-files=all)" ]]; then
  echo "working tree is not clean; commit or preserve tracked and untracked changes first" >&2
  exit 2
fi
target="$(dirname "$root")/worktrees/${task_id}-${role}"
branch="agent/${task_id}-${role}"
if [[ -e "$target" ]] || git -C "$root" show-ref --verify --quiet "refs/heads/$branch"; then
  echo "target or branch already exists: $target / $branch" >&2
  exit 2
fi
mkdir -p "$(dirname "$target")"
git -C "$root" worktree add --quiet -b "$branch" "$target" "$base_ref"
cp "$root/prompts/$role.md" "$target/ROLE_PROMPT.md"
echo "$target"
