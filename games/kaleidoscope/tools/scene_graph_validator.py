from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple

SCENE_ID_PATTERN = re.compile(r"\bscene_\d+\b")


@dataclass(frozen=True)
class Link:
    source_scene_id: str
    target_scene_id: str
    file_path: Path
    line_number: int


def find_scene_files(scenes_root: Path) -> List[Path]:
    return sorted(scenes_root.rglob("scene_*.md"))


def extract_choices(scene_file: Path) -> List[Tuple[str, int]]:
    choices: List[Tuple[str, int]] = []
    for line_number, raw_line in enumerate(scene_file.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line.startswith("- "):
            continue
        if "\u2192" not in line:
            continue
        _, target_part = line.split("\u2192", 1)
        target_match = SCENE_ID_PATTERN.search(target_part)
        if target_match is None:
            continue
        choices.append((target_match.group(0), line_number))
    return choices


def build_graph(scene_files: List[Path]) -> Tuple[Dict[str, List[Path]], List[Link]]:
    scene_id_to_paths: Dict[str, List[Path]] = defaultdict(list)
    links: List[Link] = []

    for scene_file in scene_files:
        scene_id = scene_file.stem
        scene_id_to_paths[scene_id].append(scene_file)

    for scene_id, paths in scene_id_to_paths.items():
        # Record links from each file that declares this scene id.
        for path in paths:
            for target_scene_id, line_number in extract_choices(path):
                links.append(
                    Link(
                        source_scene_id=scene_id,
                        target_scene_id=target_scene_id,
                        file_path=path,
                        line_number=line_number,
                    )
                )

    return dict(scene_id_to_paths), links


def compute_reachable(entry_scene_id: str, adjacency: Dict[str, Set[str]]) -> Set[str]:
    if entry_scene_id not in adjacency:
        return set()

    visited: Set[str] = set()
    queue: deque[str] = deque([entry_scene_id])

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in adjacency.get(node, set()):
            if neighbor not in visited:
                queue.append(neighbor)

    return visited


def validate(scenes_root: Path, entry_scene_id: str) -> int:
    scene_files = find_scene_files(scenes_root)
    scene_id_to_paths, links = build_graph(scene_files)

    all_scene_ids = sorted(scene_id_to_paths.keys())
    unique_scene_ids = set(all_scene_ids)

    duplicate_scene_ids = {
        scene_id: sorted(paths)
        for scene_id, paths in scene_id_to_paths.items()
        if len(paths) > 1
    }

    missing_target_links = [link for link in links if link.target_scene_id not in unique_scene_ids]
    self_links = [link for link in links if link.source_scene_id == link.target_scene_id]

    adjacency: Dict[str, Set[str]] = {scene_id: set() for scene_id in unique_scene_ids}
    incoming_counts: Dict[str, int] = {scene_id: 0 for scene_id in unique_scene_ids}

    for link in links:
        if link.target_scene_id in unique_scene_ids:
            adjacency[link.source_scene_id].add(link.target_scene_id)
            incoming_counts[link.target_scene_id] += 1

    reachable = compute_reachable(entry_scene_id, adjacency)
    unreachable = sorted(unique_scene_ids - reachable)

    print("Scene Graph Validator")
    print(f"Scenes root: {scenes_root}")
    print(f"Entry scene: {entry_scene_id}")
    print()

    if duplicate_scene_ids:
        print("Duplicate scene IDs:")
        for scene_id in sorted(duplicate_scene_ids.keys()):
            print(f"- {scene_id}")
            for path in duplicate_scene_ids[scene_id]:
                print(f"  - {path}")
        print()
    else:
        print("Duplicate scene IDs: none")
        print()

    if missing_target_links:
        print("Missing target scenes:")
        for link in sorted(missing_target_links, key=lambda item: (item.file_path.as_posix(), item.line_number)):
            print(
                f"- {link.source_scene_id} -> {link.target_scene_id} "
                f"({link.file_path}:{link.line_number})"
            )
        print()
    else:
        print("Missing target scenes: none")
        print()

    if self_links:
        print("Self-links:")
        for link in sorted(self_links, key=lambda item: (item.file_path.as_posix(), item.line_number)):
            print(f"- {link.source_scene_id} links to itself ({link.file_path}:{link.line_number})")
        print()
    else:
        print("Self-links: none")
        print()

    if entry_scene_id not in unique_scene_ids:
        print(f"Unreachable scenes: entry scene '{entry_scene_id}' was not found; treating all scenes as unreachable")
    if unreachable:
        print("Unreachable scenes:")
        for scene_id in unreachable:
            print(f"- {scene_id}")
        print()
    else:
        print("Unreachable scenes: none")
        print()

    print("Incoming-link counts:")
    for scene_id in sorted(incoming_counts.keys()):
        print(f"- {scene_id}: {incoming_counts[scene_id]}")
    print()

    print("Summary:")
    print(f"- Total scene files found: {len(scene_files)}")
    print(f"- Total unique scene IDs: {len(unique_scene_ids)}")
    print(f"- Broken links found: {len(missing_target_links)}")
    print(f"- Duplicate IDs found: {len(duplicate_scene_ids)}")
    print(f"- Self-links found: {len(self_links)}")
    print(f"- Unreachable scenes found: {len(unreachable)}")

    has_errors = bool(missing_target_links or duplicate_scene_ids or self_links or unreachable)
    return 1 if has_errors else 0


def main() -> int:
    default_scenes_root = Path(__file__).resolve().parents[1] / "story" / "scenes"

    parser = argparse.ArgumentParser(description="Validate Kaleidoscope scene graph integrity.")
    parser.add_argument(
        "--scenes-root",
        type=Path,
        default=default_scenes_root,
        help="Path to the scene root directory (default: games/kaleidoscope/story/scenes).",
    )
    parser.add_argument(
        "--entry-scene",
        default="scene_0001",
        help="Entry scene id used for reachability analysis (default: scene_0001).",
    )

    args = parser.parse_args()
    scenes_root = args.scenes_root.resolve()

    if not scenes_root.exists() or not scenes_root.is_dir():
        print(f"Error: scenes root does not exist or is not a directory: {scenes_root}")
        return 2

    return validate(scenes_root=scenes_root, entry_scene_id=args.entry_scene)


if __name__ == "__main__":
    raise SystemExit(main())
