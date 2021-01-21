import pytest

from utilities import args_parse, collect_and_check_files


def test_if_threads_set_to_default_1():
    args = args_parse(["-p", "data/"])
    assert args.threads == 1


def test_raising_exc_if_folder_has_no_csv_or_no_folder():
    args = args_parse(["-p", "strangefolder/"])
    with pytest.raises(
        FileNotFoundError, match="Your path has no csv files. Please set another path"
    ):
        collect_and_check_files(args.path)
