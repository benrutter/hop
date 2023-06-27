from typing import List
from pathlib import Path
import shutil

from send2trash import send2trash

from hop import icons


def copy_files(files: List[Path]) -> str:
    """
    Copies files into current location, returns message
    """
    not_copied: List[str] = []
    for i in files:
        try:
            shutil.copy(i, f"{i.stem}{i.suffix}")
        except:
            not_copied.append(str(i))
    if not_copied:
        return "[red bold]Could not copy:\n" + "\n".join(not_copied) + "[/red bold]"
    else:
        return "[green]Files in inventory copied[/green]"


def delete_files(files: List[Path]) -> str:
    """
    Deletes files into recycling bin, returns message
    """
    not_deleted: List[str] = []
    for i in files:
        try:
            send2trash(i)
        except:
            not_deleted.append(str(i))
    if not_deleted:
        return "[red bold]Could not delete:\n" + "\n".join(not_deleted) + "[/red bold]"
    else:
        return "[green]Files in inventory deleted[/green]"


def move_files(files: List[Path]) -> str:
    """
    Move files into current location, returns message
    """
    not_moved: List[str] = []
    for i in files:
        try:
            shutil.move(i, f"{i.stem}{i.suffix}")
        except:
            not_moved.append(str(i))
    if not_moved:
        return "[red bold]Could not move:\n" + "\n".join(not_moved) + "[/red bold]"
    else:
        return "[green]Files in inventory moved[/green]"


def levenshtein_distance(a: str, b: str) -> int:
    """
    Calculate levenshtein distance between two strings
    """
    char_diff = len(set(a) - set(b))
    len_diff = abs(len(b) - len(a))
    return len_diff + char_diff


def get_icon(path: Path) -> str:
    """
    Return icon for filepath
    """
    if path.is_dir():
        return ":file_folder:"
    return icons.icons[path.suffix.lower()]
