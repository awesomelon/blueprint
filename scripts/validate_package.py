#!/usr/bin/env python3
"""Validate distribution metadata and maintained inline document links."""

import importlib.util
import json
from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("harness", ROOT / "skills/blueprint/scripts/harness.py")
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


def validate():
    errors = []
    # Parse every committed-format JSON/YAML, excluding local execution evidence.
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts or relative.parts[:2] == (".blueprint", "runs"):
            continue
        try:
            if path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            elif path.suffix in (".yaml", ".yml"):
                yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, yaml.YAMLError) as exc:
            errors.append(f"{relative}: {exc}")

    manifests = [
        json.loads((ROOT / path).read_text())
        for path in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json")
    ]
    for field in ("name", "version", "description", "author", "homepage", "repository", "license", "keywords"):
        if any(manifest[field] != manifests[0][field] for manifest in manifests[1:]):
            errors.append(f"Plugin manifests disagree on {field}. Keep all distributions aligned.")
    if manifests[0]["extensions"]["com.openai"]["interface"] != manifests[1]["interface"]:
        errors.append("Portable and Codex presentation metadata differ.")
    for manifest in manifests[1:]:
        if manifest["skills"] != "./skills/":
            errors.append("Host manifests must package the shared skills/ directory.")
    for path in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
        marketplace = json.loads((ROOT / path).read_text())
        plugin = marketplace["plugins"][0]
        source = plugin["source"]
        if plugin["name"] != manifests[0]["name"] or source not in (
            "./", {"source": "local", "path": "./"}
        ):
            errors.append(f"{path}: marketplace must point to this package.")
    skill = (ROOT / "skills/blueprint/SKILL.md").read_text()
    frontmatter = yaml.safe_load(skill.split("---", 2)[1])
    if frontmatter["name"] != manifests[0]["name"] or not frontmatter["description"]:
        errors.append("Skill frontmatter must match the package.")
    agent = yaml.safe_load((ROOT / "skills/blueprint/agents/openai.yaml").read_text())
    if agent["interface"]["display_name"] != manifests[1]["interface"]["displayName"]:
        errors.append("Skill and plugin display names differ.")
    documents = [
        str(path.relative_to(ROOT)) for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and not path.is_relative_to(ROOT / ".blueprint/runs")
    ]
    errors.extend(harness.document_errors(ROOT, documents))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Package metadata and inline file links validated ({len(documents)} Markdown files).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(validate())
    except (KeyError, IndexError, TypeError, OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Invalid package structure: {exc}", file=sys.stderr)
        sys.exit(1)
