"""Read-only structural checks for the AGU design bundle. Standard library only."""

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote


def check_design(root):
    root = Path(root).resolve()
    decisions = root / "docs/00-baseline-decisions.md"
    if not decisions.is_file():
        raise ValueError("--root must contain docs/00-baseline-decisions.md")
    issues = []

    def issue(code, path, detail, line=None):
        issues.append({"code": code, "file": path.relative_to(root).as_posix(), "line": line, "detail": detail})

    active = sorted((root / "docs").glob("[0-9][0-9]-*.md"))
    active += sorted((root / "docs/decisions").glob("ADR-*.md"))
    ignored = {".git", "node_modules", ".venv", "venv", ".local", ".next", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache"}
    markdown = []
    for directory, children, names in os.walk(root):
        children[:] = [name for name in children if name not in ignored]
        markdown.extend(Path(directory) / name for name in names if name.endswith(".md"))
    markdown.sort()
    visible = {}
    json_blocks = 0
    local_links = 0
    for path in markdown:
        text = path.read_text(encoding="utf-8-sig")
        if "\ufffd" in text:
            issue("invalid_unicode", path, "Unicode replacement character present")
        plain, fenced, fence, block, start = [], [], None, [], None
        for number, line in enumerate(text.splitlines(), 1):
            match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
            if fence is None and match:
                fence = (match[1][0], len(match[1]), match[2].strip().lower())
                block, start = [], number
                plain.append("")
            elif fence is not None:
                if match and match[1][0] == fence[0] and len(match[1]) >= fence[1] and not match[2].strip():
                    fenced.append((fence[2], "\n".join(block), start))
                    fence = None
                else:
                    block.append(line)
                plain.append("")
            else:
                plain.append(line)
        if fence is not None:
            issue("unclosed_fence", path, "Fenced block is not closed", start)
        visible[path] = "\n".join(plain)
        for language, block, number in fenced:
            if language == "json":
                json_blocks += 1
                try:
                    json.loads(block)
                except ValueError as error:
                    issue("invalid_json", path, str(error), number)
        for number, line in enumerate(plain, 1):
            # Code samples are not actual document dependencies.
            line = re.sub(r"`[^`]*`", "", line)
            for link in re.finditer(r'\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+"[^"]*")?\s*\)', line):
                target = link[1] or link[2]
                if re.match(r"^(?:https?://|mailto:|#)", target, re.I):
                    continue
                local_links += 1
                target = unquote(target.split("#", 1)[0])
                if not (path.parent / target).resolve().exists():
                    issue("missing_local_link", path, target, number)

    version_pattern = re.compile(r"^\|\s*(?:Phiên bản|Version|ADR\s*/\s*revision)\s*\|\s*([^|]+)\|", re.M | re.I)

    def version(path):
        match = version_pattern.search(visible.get(path, ""))
        number = re.search(r"\d+\.\d+(?:\.\d+)?", match[1]) if match else None
        return number[0] if number else None

    expected_version = version(decisions)
    if expected_version is None:
        issue("missing_version", decisions, "No numeric baseline version in metadata")
    for path in active:
        found = version(path)
        if found != expected_version or found is None:
            issue("version_mismatch", path, f"Expected {expected_version}, found {found}")

    prd = root / "docs/02-prd.md"
    definitions = re.findall(r"^\|\s*((?:FR|AC|BR|NFR)-\d+)\s*\|", visible.get(prd, ""), re.M)
    counts = Counter(definitions)
    if not prd.is_file():
        issue("missing_prd", prd, "PRD source of requirement IDs is missing")
    for item, count in counts.items():
        if count > 1:
            issue("duplicate_requirement", prd, f"{item} is defined {count} times")
    for path in active:
        references = re.sub(r"\b((?:FR|AC|BR|NFR)-)(\d+)((?:/\d+)+)", lambda m: " ".join(m[1] + n for n in [m[2], *m[3].strip("/").split("/")]), visible[path])
        for item in set(re.findall(r"\b(?:FR|AC|BR|NFR)-\d+\b", references)):
            if item not in counts:
                issue("unknown_requirement", path, item)

    roadmap = root / "docs/08-implementation-roadmap.md"
    graph, dependency_column = {}, None
    for number, line in enumerate(visible.get(roadmap, "").splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if any(x.lower() in {"dependency", "dependencies"} for x in cells):
            dependency_column = next(i for i, x in enumerate(cells) if x.lower() in {"dependency", "dependencies"})
        if not re.fullmatch(r"WP-\d+", cells[0]):
            continue
        name = cells[0]
        if name in graph:
            issue("duplicate_work_package", roadmap, name, number)
        if dependency_column is None or len(cells) <= dependency_column:
            issue("missing_dependency_column", roadmap, name, number)
            continue
        dependency = re.sub(r"WP-(\d+)((?:/\d+)+)", lambda m: " ".join("WP-" + n for n in [m[1], *m[2].strip("/").split("/")]), cells[dependency_column])
        graph[name] = re.findall(r"WP-\d+", dependency)
    if not roadmap.is_file():
        issue("missing_roadmap", roadmap, "Roadmap is missing")
    for name, dependencies in graph.items():
        for dependency in dependencies:
            if dependency not in graph:
                issue("unknown_work_package", roadmap, f"{name} -> {dependency}")
    visited, visiting = set(), []

    def visit(name):
        if name in visiting:
            issue("dependency_cycle", roadmap, " -> ".join(visiting[visiting.index(name):] + [name]))
            return
        if name in visited:
            return
        visiting.append(name)
        for dependency in graph.get(name, []):
            visit(dependency)
        visiting.pop()
        visited.add(name)

    for name in graph:
        visit(name)
    return {
        "structural_checks_passed": not issues,
        "semantic_review_required": True,
        "approval_recorded_by_checker": False,
        "baseline_version": expected_version,
        "markdown_files": len(markdown),
        "active_design_documents": len(active),
        "local_links_checked": local_links,
        "json_blocks_checked": json_blocks,
        "requirement_counts": {prefix: sum(key.startswith(prefix + "-") for key in counts) for prefix in ("FR", "AC", "BR", "NFR")},
        "work_packages": len(graph),
        "issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        report = check_design(args.root)
    except (ValueError, OSError) as error:
        print(json.dumps({"input_error": str(error)}, ensure_ascii=True))
        return 2
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0 if report["structural_checks_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
