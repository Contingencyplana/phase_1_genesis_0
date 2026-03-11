from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple


def _get_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start == -1:
        return ""

    section = text[start + len(marker) :]

    # Trim divider if present.
    section = section.split("\n---", 1)[0]

    # Stop at next heading of the same level.
    next_heading = section.find("\n## ")
    if next_heading != -1:
        section = section[:next_heading]

    return section.strip()


def _parse_choices(choices_block: str) -> List[Tuple[str, str]]:
    choices: List[Tuple[str, str]] = []
    for raw_line in choices_block.splitlines():
        line = raw_line.strip()
        if not line.startswith("- "):
            continue
        body = line[2:].strip()
        if "\u2192" not in body:
            continue
        choice_text, target_scene_id = body.split("\u2192", 1)
        choices.append((choice_text.strip(), target_scene_id.strip()))
    return choices


def parse_scene_markdown(markdown_text: str) -> Dict[str, object]:
    first_line = markdown_text.splitlines()[0].strip() if markdown_text.strip() else ""
    scene_id = ""
    if first_line.startswith("# Scene:"):
        scene_id = first_line.split(":", 1)[1].strip()

    title = _get_section(markdown_text, "Title")
    location = _get_section(markdown_text, "Location")
    scene_text = _get_section(markdown_text, "Scene Text")
    choices_block = _get_section(markdown_text, "Choices")
    choices = _parse_choices(choices_block)

    return {
        "scene_id": scene_id,
        "title": title,
        "location": location,
        "scene_text": scene_text,
        "choices": choices,
    }


def parse_scene_file(scene_file_path: Path) -> Dict[str, object]:
    return parse_scene_markdown(scene_file_path.read_text(encoding="utf-8"))
