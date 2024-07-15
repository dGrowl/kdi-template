from argparse import ArgumentParser
from os import makedirs, rename
from pathlib import Path
from subprocess import run
from sys import executable


ROOT_PATH = Path(__file__).parent.parent.absolute()

DEFAULT_MODULE_NAME = "kdi_template"
PIP_PATH = ROOT_PATH / "venv" / "Scripts" / "pip"
PYPROJECT_PATH = ROOT_PATH / "pyproject.toml"

verbose = False

parser = ArgumentParser(
	prog="python init_dev.py",
	description="Sets up the development environment for a new KDI module.",
)
parser.add_argument("name", help="specifies a name for the module")
parser.add_argument(
	"-v",
	"--verbose",
	action="store_true",
	default=verbose,
	help="prints the output of each command",
)


def run_wrapper(cmd: list[Path | str]):
	result = run(cmd, capture_output=True)
	if verbose:
		print(" ".join(map(str, cmd)))
		if result.stdout:
			print(result.stdout.decode())
	if result.stderr:
		print("** ERROR: **")
		print(result.stderr.decode())


def rename_pyproject(new_name: str):
	print('Renaming project in "pyproject.toml"...')
	with open(PYPROJECT_PATH, "r") as f:
		lines = f.readlines()
	lines[1] = f'name = "{new_name}"\n'
	with open(PYPROJECT_PATH, "w", newline="\n") as f:
		f.writelines(lines)


def rename_project_dir(new_name: str):
	print(f'Renaming "/src/{DEFAULT_MODULE_NAME}" -> "/src/{new_name}"...')
	rename(ROOT_PATH / "src" / DEFAULT_MODULE_NAME, ROOT_PATH / "src" / new_name)


def make_build_dir():
	print('Creating "/build" dir...')
	makedirs(ROOT_PATH / "build", exist_ok=True)


def create_venv():
	print('Creating virtual environment in "/venv"...')
	run_wrapper([executable, "-m", "venv", ROOT_PATH / "venv"])


def setup_git_hooks():
	print("Setting up git hooks...")
	run_wrapper(["git", "config", "--local", "core.hooksPath", "dev/hooks/"])


def install_self():
	print("Installing self as an editable package...")
	run_wrapper([PIP_PATH, "install", "-e", ROOT_PATH])


def install_dev_dependencies():
	print("Installing dev dependencies...")
	run_wrapper([PIP_PATH, "install", "-r", ROOT_PATH / "requirements" / "dev.txt"])


if __name__ == "__main__":
	args = parser.parse_args()
	verbose = args.verbose

	rename_pyproject(args.name)
	rename_project_dir(args.name)
	create_venv()
	setup_git_hooks()
	make_build_dir()
	install_self()
	install_dev_dependencies()
