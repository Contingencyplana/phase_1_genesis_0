from __future__ import annotations

from typing import Dict


def get_target_scene_id(scene: Dict[str, object], choice_index: int) -> str:
    choices = scene.get("choices", [])
    if not isinstance(choices, list):
        raise ValueError("Scene choices are invalid.")

    if choice_index < 1 or choice_index > len(choices):
        raise ValueError("Choice index out of range.")

    return choices[choice_index - 1][1]
