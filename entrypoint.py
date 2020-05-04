import os
import sys
import json
import tempfile
import subprocess
import shutil
from distutils.util import strtobool
import warnings


def read_json(path):
    with open(path) as f:
        return json.load(f)


def to_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def run_shell(command, verbose=True):
    print("Executing:", command)
    p = subprocess.Popen(
        [command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    stdout, stderr = p.communicate()

    stdout = stdout.decode("utf-8")
    stderr = stderr.decode("utf-8")  # stderr contains warnings.

    if p.returncode != os.EX_OK:
        print("Return code:", p.returncode)
        print(stdout)
        print(stderr)
        raise sys.exit(p.returncode)

    if verbose:
        if stdout != "":
            print(stdout)

        if stderr != "":
            print(stderr)

    return p.returncode


def get_action_input(name):
    # NOTE: When `default` is not given in `action.yml`,
    # action input value will be "" (empty string).
    return os.getenv(f"INPUT_{name.upper()}")


def to_list(s):
    return [x for x in s.split("\n") if x.strip() != "" and not x.startswith("#")]


def to_bool(s):
    return strtobool(s) == 1


def get_input_schema():
    return {
        "metadata_file": str,
        "id": str,
        "title": str,
        "code_file": str,
        "language": str,
        "kernel_type": str,
        "is_private": to_bool,
        "enable_gpu": to_bool,
        "enable_internet": to_bool,
        "dataset_sources": to_list,
        "competition_sources": to_list,
        "kernel_sources": to_list,
    }


def parse_action_inputs():
    input_schema = get_input_schema()
    inputs = {}

    for key, cast in input_schema.items():
        val = get_action_input(key)
        inputs[key] = None if (val == "") else cast(val)

    return inputs


def main():
    action_inputs = parse_action_inputs()
    meta_file = action_inputs.pop("metadata_file")
    use_meta = meta_file is not None
    meta = read_json(meta_file) if use_meta else {}

    for key, val in action_inputs.items():
        if val is None:
            continue

        # TODO: Add an option to prevent overwriting metadata keys?
        if key in meta:
            warnings.warn("Overwrite `{}` in metadata by action input".format(key))

        meta.update({key: val})

    code_file = meta["code_file"]
    file_name = os.path.basename(code_file)

    if use_meta:
        # `code_file` is a relative path from the direcotry where `meta_file` exists.
        meta_dir = os.path.dirname(meta_file)
        code_file = os.path.join(meta_dir, file_name)
    else:
        meta["code_file"] = file_name

    # Create a temporary directory to store metadata and kernel.
    with tempfile.TemporaryDirectory() as tmpdir:
        # Save the kernel metadata.
        to_json(meta, os.path.join(tmpdir, "kernel-metadata.json"))

        # Copy the target kernel to `tmpdir`.
        dst = os.path.join(tmpdir, file_name)
        shutil.copyfile(code_file, dst)

        # Push the kernel to Kaggle.
        run_shell(f"kaggle kernels push -p {tmpdir}")
        run_shell(f'kaggle kernels status {meta["id"]}')


if __name__ == "__main__":
    main()
