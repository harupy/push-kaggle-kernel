import os
import sys
import json
import tempfile
import subprocess
import shutil


def to_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def run_command(command, verbose=True):
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


def create_kernel_meta(
    username,
    slug,
    title,
    code_file,
    language,
    kernel_type,
    is_private,
    enable_gpu,
    enable_internet,
    dataset_sources,
    competition_sources,
    kernel_sources,
):
    return {
        "id": f"{username}/{slug}",
        "title": title,
        "code_file": code_file,
        "language": language,
        "kernel_type": kernel_type,
        "is_private": is_private,
        "enable_gpu": enable_gpu,
        "enable_internet": enable_internet,
        "dataset_sources": dataset_sources,
        "competition_sources": competition_sources,
        "kernel_sources": kernel_sources,
    }


def get_action_input(name, as_list=False):
    action_input = os.getenv(f"INPUT_{name.upper()}")
    if as_list:
        # Ignore empty and comment lines.
        return [
            x
            for x in action_input.split("\n")
            if x.strip() != "" and not x.startswith("#")
        ]

    return action_input


def main():
    username = os.getenv("KAGGLE_USERNAME")
    slug = get_action_input("slug")
    title = get_action_input("title")
    code_file = get_action_input("code_file")
    language = get_action_input("language")
    kernel_type = get_action_input("kernel_type")
    is_private = get_action_input("is_private")
    enable_gpu = get_action_input("enable_gpu")
    enable_internet = get_action_input("enable_internet")
    dataset_sources = get_action_input("dataset_sources", as_list=True)
    competition_sources = get_action_input("competition_sources", as_list=True)
    kernel_sources = get_action_input("kernel_sources", as_list=True)

    script_name = os.path.basename(code_file)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Save kernel metadata to tmpdir.
        kernel_meta = create_kernel_meta(
            username,
            slug,
            title,
            script_name,
            language,
            kernel_type,
            is_private,
            enable_gpu,
            enable_internet,
            dataset_sources,
            competition_sources,
            kernel_sources,
        )
        to_json(kernel_meta, os.path.join(tmpdir, "kernel-metadata.json"))

        # Copy script to tmpdir.
        dst = os.path.join(tmpdir, script_name)
        shutil.copyfile(code_file, dst)

        run_command(f"kaggle kernels push -p {tmpdir}")
        run_command(f"kaggle kernels status {username}/{slug}")


if __name__ == "__main__":
    main()
