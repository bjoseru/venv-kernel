import os
import re
import shutil
import sys
from pathlib import Path
from typing import Optional

import jupyter_client
import pkg_resources
from rich import print
from typer import Option, Typer, Exit

__version__ = "1.0.2"

app = Typer(
    help=f"""
Create a custom jupyter kernel for your venv.

Version {__version__}. Copyright 2021 Björn Rüffer. MIT License.
""", add_completion=False
)



@app.command(name="install")
def make_kernel(
    name: str = Option(
        None,
        help="Name of the kernal to install, as shown in `jupyter kernelspec list`.",
    ),
    display_name: str = Option(
        None, help="Long version of name as shown in jupyter notebook."
    ),
    set_path: bool = Option(
        True, help="Include current PATH in the kernel environment."
    ),
) -> None:
    "Create and install a jupyter kernel for the current venv."
    if not os.getenv("VIRTUAL_ENV"):
        print('[red]You need to be in an active venv to use this tool.')
        raise Exit(code=1)
    if display_name is None:
        display_name = (
            f'\U0001F40D venv {re.sub(os.getenv("HOME"), "~", os.getcwd())} | '
            + f"Python {sys.version_info.major}.{sys.version_info.minor}."
            + f"{sys.version_info.micro}"
        )
    extra_dict = dict()
    if set_path:
        extra_dict["PATH"] = f'{os.getenv("VIRTUAL_ENV")}/bin:{os.getenv("PATH")}'
    spec = jupyter_client.kernelspec.KernelSpec(
        argv=[sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
        env={
            "VIRTUAL_ENV": os.getenv("VIRTUAL_ENV"),
            **extra_dict,
        },
        language="python",
        display_name=display_name,
    )

    if name is None:
        name = re.sub("/", " ", os.getenv("VIRTUAL_ENV")).strip()
        name = re.sub(" ", "-", name)
        name = re.sub("[^a-zA-Z0-9-]", "", name)

    kernel_path = Path(os.getenv("VIRTUAL_ENV")) / "kernels" / name
    kernel_path.mkdir(exist_ok=True, parents=True)

    with open(kernel_path / "kernel.json", "w") as f:
        f.write(spec.to_json())

    jupyter_client.kernelspec.install_kernel_spec(
        str(kernel_path), kernel_name=name, user=True,
        replace=True
    )

    print(f"Installed new kernel at\n[blue not bold]{kernel_path}.")


def is_current_kernel(spec: jupyter_client.kernelspec.KernelSpec) -> bool:
    "Does the given kernel include the current venv?"
    return (
        ("VIRTUAL_ENV" in spec.env.keys())
        and (os.getenv("VIRTUAL_ENV") != "")
        and (spec.env["VIRTUAL_ENV"] == os.getenv("VIRTUAL_ENV"))
    )


@app.command(name="list")
def list_kernels():
    "List all installed kernels."
    print("[bold yellow]You have these jupyter kernels installed:")
    for name, path in jupyter_client.kernelspec.find_kernel_specs().items():
        print(name, path, end="")
        spec = jupyter_client.kernelspec.get_kernel_spec(name)
        if is_current_kernel(spec):
            print("[bold red] <- [not bold red] current venv")
        else:
            print()


@app.command(name="clean")
def remove_kernels(
    force: bool = Option(False, "--force", "-f", help="Actually remove kernels.")
):
    "Delete all kernels that correspond to the current venv."
    kernel_list = {
        name: path
        for name, path in jupyter_client.kernelspec.find_kernel_specs().items()
        if is_current_kernel(jupyter_client.kernelspec.get_kernel_spec(name))
    }
    if kernel_list:
        print("[bold cyan]Deleting kernels:")
        for name, path in kernel_list.items():
            print(name, path, end="")
            if force:
                # do actual deletion here
                #
                # It seems one should be able to somehow do this using
                #     jupyter_client.kernelspecapp.RemoveKernelSpec(name)
                # but that doesn't work. Fixes welcome!
                #
                p = Path(path)
                shutil.rmtree(p, ignore_errors=True)
                print("[bold red] DELETED")
            else:
                print("[green not bold] will delete if --force is used")
    else:
        print(
            "[red not bold]There do not seem to be any kernels belonging to this venv."
        )


if __name__ == "__main__":
    app()
