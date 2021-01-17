from pathlib import Path
from typing import Set


def collect_and_check_files(list_of_paths) -> Set[Path]:
    """
    Checking if the files are present on the path from your input and giving collection of files
    """
    files_to_read = set()
    for path in list_of_paths:
        files_to_read.update(set(Path(path).glob("**/*.csv")))
    if not files_to_read:
        raise FileNotFoundError("Your path has no csv files. Please set another path")
    return files_to_read
