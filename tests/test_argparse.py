import pytest

from utilities import args_parse, collect_and_check_files


def test_if_threads_set_to_default_1():
    args = args_parse(["-p", "data/"])
    assert args.threads is None


def test_raising_exc_if_folder_has_no_csv_or_no_folder():
    args = args_parse(["-p", "strangefolder/"])
    with pytest.raises(
        FileNotFoundError,
        match="Your path has no csv files. Either wrong path or no files on path."
        "Please set another path",
    ):
        collect_and_check_files(args.path)


@pytest.mark.parametrize(
    ["arg", "value"],
    [
        (["-t", -125]),
        (["-t", None]),
    ],
)
def test_exception_handling_with_wrong_threads_arguments(arg, value):
    arguments = ["-p", "data/", arg, value]
    with pytest.raises(
        ValueError,
        match="Wrong 'threads' argument, it must be integer and it's value must be more then zero",
    ):
        args_parse(arguments)
