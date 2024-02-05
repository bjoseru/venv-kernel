import os

from typer.testing import CliRunner

from venv_kernel import __version__ as venv_kernel_version
from venv_kernel.kernel_tool import app

__version__ = "1.0.11"
runner = CliRunner()


def test_version():
    assert venv_kernel_version == __version__


def test_make_kernel():
    result = runner.invoke(app, ["install"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["install", "--name", "pytest-xyz"])
    assert result.exit_code == 0
    assert "Installed new kernel at" in result.stdout
    assert "pytest-xyz" in result.stdout


def test_list_kernels():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "You have these jupyter kernels installed" in result.stdout


def test_remove_kernels():
    result = runner.invoke(app, ["clean"])
    assert result.exit_code == 0
    assert "Deleting kernels" in result.stdout
    assert "pytest-xyz" in result.stdout
    assert "will delete if --force is used" in result.stdout
    result = runner.invoke(app, ["clean", "--force"])
    assert result.exit_code == 0
    assert "Deleting kernels" in result.stdout
    assert "pytest-xyz" in result.stdout
    assert "DELETED" in result.stdout
    result = runner.invoke(app, ["clean"])
    assert result.exit_code == 0
    assert "There do not seem to be any kernels belonging to this venv" in result.stdout


## From here on we start changing the environment to trigger error handling


def test_make_kernel_fails():
    os.environ["VIRTUAL_ENV"] = ""
    result = runner.invoke(app, ["install", "--name", "pytest-xyz"])
    assert result.exit_code == 1
    assert "You need to be in an active venv to use this tool" in result.stdout
