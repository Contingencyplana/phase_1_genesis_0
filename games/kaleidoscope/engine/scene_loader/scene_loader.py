from __future__ import annotations

from pathlib import Path
from typing import Dict

from scene_loader.scene_parser import parse_scene_file


SCENES_ROOT = Path(__file__).resolve().parents[2] / "story" / "scenes"


def _find_scene_file(scene_id: str, scenes_root: Path) -> Path:
    expected_name = f"{scene_id}.md"
    for path in scenes_root.rglob(expected_name):
        if path.is_file():
            return path
    raise FileNotFoundError(f"Scene not found: {scene_id}")


def load_scene(scene_id: str, scenes_root: Path = SCENES_ROOT) -> Dict[str, object]:
    scene_path = _find_scene_file(scene_id, scenes_root)
    return parse_scene_file(scene_path)
