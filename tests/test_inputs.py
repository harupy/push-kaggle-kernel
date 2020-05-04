import pytest
import yaml

from entrypoint import get_input_schema


def read_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


@pytest.fixture
def action_yaml():
    return read_yaml("./action.yml")


@pytest.fixture
def input_schema():
    return get_input_schema()


def test_input_schema(action_yaml, input_schema):
    assert set(input_schema.keys()) == set(action_yaml["inputs"].keys())


def test_input_default_value_does_not_raise_error_when_casting(
    action_yaml, input_schema
):
    for name, inp in action_yaml["inputs"].items():
        if "default" not in inp:
            continue

        cast_func = input_schema[name]
        cast_func(inp["default"])
