import os
from pathlib import Path

from . import setup_console


class Setup:
    """Class to check all prerequisite eg, ssh client, cloudflared etc."""

    def __init__(self) -> None:

        self.ssh_config_path: Path = Path(os.path.expanduser("~/.ssh/config"))

        # No support for windows currently!
        self.probable_cloudlfared_paths: list[str] = [
            "/usr/local/bin/cloudflared",
            "/opt/homebrew/bin/cloudflared",
        ]

        self.proxy_command: str = (
            f"{self.get_cloudflared_binary()} access ssh --hostname %h"
        )

        self.user: str = "root"
        self.config_for_remote_connection: str = f"""
Host *.trycloudflare.com
    HostName %h
    User {self.user}
    Port 22
    ProxyCommand {self.proxy_command}
        """

        self.check_ssh_config()

    def get_cloudflared_binary(self) -> Path:
        for probable_path in self.probable_cloudlfared_paths:
            if os.path.exists(probable_path):
                return Path(probable_path)

        raise FileNotFoundError("Please install cloudlfared before starting!")

    def check_ssh_config(self):
        """Checks for generic config file in ~/.ssh/ create one if not present"""

        # What if the ssh dir is not present?
        if not os.path.exists(self.ssh_config_path.parent):
            raise FileNotFoundError(
                f"SSH directory does not exist at {self.ssh_config_path.parent} how are you alive...?"
            )

        # what if the config file is not present?
        if not os.path.exists(self.ssh_config_path):
            setup_console.print(
                f"[yellow]> SSH config file not found at {self.ssh_config_path} create a new one...[yellow]"
            )
            with open(self.ssh_config_path, "w") as config_file:
                config_file.write(self.config_for_remote_connection)

            setup_console.print(
                f"[green]> Created new ssh config for remote colab connection[green]"
            )

        # what if file is present but cloudflared is not present...most likely case.
        with open(self.ssh_config_path, "a+") as config_file:
            config_file.seek(0)

            if "*.trycloudflare.com" not in config_file.read():
                config_file.write(self.config_for_remote_connection)
                setup_console.print(
                    "[yellow] > Cloudflared configurations not found writing cloudflared configs...[yellow]"
                )

        setup_console.print("\n[green]> Setup Completed!\n")


if __name__ == "__main__":
    Setup()
