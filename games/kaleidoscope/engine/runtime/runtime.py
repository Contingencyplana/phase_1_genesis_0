from __future__ import annotations

import sys
from pathlib import Path

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from choice_handler.choice_handler import get_target_scene_id
from scene_loader.scene_loader import load_scene


def run_game(start_scene_id: str = "scene_0001") -> None:
    current_scene_id = start_scene_id

    while True:
        scene = load_scene(current_scene_id)

        print(f"\n=== {scene['title']} ===")
        if scene.get("location"):
            print(f"Location: {scene['location']}")
        print()
        print(scene["scene_text"])
        print()

        raw_choices = scene.get("choices", [])
        if not isinstance(raw_choices, list):
            raise ValueError("Scene choices are invalid.")

        choices = raw_choices
        if not choices:
            print("[End of story path]")
            break

        for index, (choice_text, _) in enumerate(choices, start=1):
            print(f"{index}. {choice_text}")

        while True:
            raw = input("\nChoose an option: ").strip()
            try:
                selection = int(raw)
                current_scene_id = get_target_scene_id(scene, selection)
                break
            except ValueError:
                print("Please enter a valid numbered choice.")


if __name__ == "__main__":
    run_game()
