"""
Installtion script for easy install.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from shlex import split


class Installer:
    def __init__(
        self, verbose: bool = False, use_env: bool = True, dir: str = "."
    ) -> None:
        self.verbose = verbose
        self.use_env = use_env
        self.dir = Path(dir).absolute()
        self.remote_url = "https://github.com/Aradhya-Tripathi/MSc-Group-Project.git"

    def set_dependency_installation_guideline(self) -> dict[str, str]: ...

    @property
    def in_env(self) -> bool:
        return sys.base_prefix != sys.prefix

    def cmd(self, command: str, cwd: str = ".") -> int:
        if self.verbose:
            print(f"$ {command}")
        try:
            subprocess.run(
                split(command),
                stdout=subprocess.DEVNULL,
                cwd=cwd,
            )
        except Exception as e:
            print(f"Error occured during installation: {e}")

    def create_env(self) -> None:
        import venv

        builder = venv.EnvBuilder(with_pip=True)
        builder.create(env_dir=self.dir / "env")

    def get_remote(self) -> None:
        self.cmd(f"git clone {self.remote_url} {self.dir / 'localfold'}")

    def install(self) -> None:
        print(f"Starting install in: {self.dir.absolute()}")
        if not self.in_env and self.use_env:
            print(f"Creating env {self.dir / 'env'} ...")
            self.create_env()

        self.get_remote()
        if not self.in_env and self.use_env:
            # At this point we have a environment created by us.
            self.cmd(
                f"{self.dir / 'env/bin/pip'} install .", cwd=self.dir / "localfold"
            )
        else:
            self.cmd("pip install .", cwd=self.dir / "localfold")

        self.cmd("npm install", cwd=self.dir / "localfold/ui")

        print(f"\ncd {self.dir / 'localfold/localfold'} && localfold --help")

        print("\n\nInstallation Complete!\n\n")


def main():
    parser = argparse.ArgumentParser(
        description="Installation script for easy install."
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--make-env",
        dest="use_env",
        action="store_true",
        help="Do not use virtual environment",
    )
    parser.add_argument(
        "--dir",
        default="./localfold-installation",
        help="Directory to install (default: current directory)",
    )
    args = parser.parse_args()
    installer = Installer(verbose=args.verbose, use_env=args.use_env, dir=args.dir)
    installer.install()


if __name__ == "__main__":
    main()
