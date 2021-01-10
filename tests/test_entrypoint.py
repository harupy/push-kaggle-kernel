import os
from unittest import mock

import pytest

from entrypoint import (
    get_action_input,
    is_comment,
    is_empty,
    parse_action_inputs,
    read_json,
    run_shell,
    to_bool,
    to_json,
    to_list,
)


def test_read_json(tmpdir):
    path = tmpdir.join("test.json")
    with open(path, "w") as f:
        f.write('{"a": "b"}')

    assert read_json(path) == {"a": "b"}


def test_to_json(tmpdir):
    path = tmpdir.join("test.json")
    to_json({"a": "b"}, path)
    with open(path) as f:
        assert f.read() == '{\n  "a": "b"\n}'


def test_run_shell(capsys):
    return_code = run_shell("echo foo")
    captured = capsys.readouterr()
    stdout_expected = """
Executing: echo foo
foo
"""
    assert return_code == 0
    assert captured.out.strip() == stdout_expected.strip()

    with pytest.raises(SystemExit):
        run_shell("python -c 'print(a)'")


def test_is_comment():
    assert is_comment("#")
    assert is_comment("  #")
    assert not is_comment("a")


def test_is_empty():
    assert is_empty(" ")
    assert is_empty("\t")
    assert not is_empty("a")


def test_get_action_input():
    with mock.patch.dict(os.environ, {"INPUT_X": "a"}):
        assert get_action_input("x") == "a"
        assert get_action_input("y") is None


def test_to_bool():
    assert to_bool("yes")
    assert to_bool("YES")
    assert to_bool("y")
    assert to_bool("Y")
    assert to_bool("1")
    assert to_bool("true")
    assert to_bool("TRUE")

    assert not to_bool("no")
    assert not to_bool("NO")
    assert not to_bool("n")
    assert not to_bool("N")
    assert not to_bool("0")
    assert not to_bool("false")
    assert not to_bool("FALSE")


def test_to_list():
    assert to_list("foo") == ["foo"]
    assert to_list("foo\nbar") == ["foo", "bar"]
    assert to_list("\nfoo\nbar\n") == ["foo", "bar"]
    assert to_list("foo\n# comment") == ["foo"]
    assert to_list("foo\n  \n") == ["foo"]


def test_parse_action_inputs():
    with mock.patch.dict(
        os.environ, {"INPUT_STR": "a", "INPUT_BOOL": "true", "INPUT_LIST": "foo\nbar"}
    ):
        input_schema = {"str": str, "bool": to_bool, "list": to_list}
        inputs = parse_action_inputs(input_schema)
        assert inputs == {"str": "a", "bool": True, "list": ["foo", "bar"]}
