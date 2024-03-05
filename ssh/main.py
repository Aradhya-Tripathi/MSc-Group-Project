from paramiko import AutoAddPolicy, ProxyCommand, SSHClient, SSHException
from paramiko.auth_strategy import Password

from setup import setup_console
from setup.installations import Setup
from setup.user_interaction import guide


class Connection:
    """Initialise pre-connection setup, include warnings and host keys setup"""

    def __init__(
        self,
        hostname: str = None,
        password: str = None,
        timeout: None | int = None,
    ) -> None:
        """Run setup and trigger remote colab connection also supports existing hostname and password
        to cater for existing ssh connections.
        """
        self.timeout = timeout
        self.setup = self.run_setup()

        if not hostname and not password:
            self.hostname, self.password = guide()
        else:
            self.hostname, self.password = hostname, password

        self.colab_client: SSHClient = self.connect()

    def connect(self) -> SSHClient:
        """
        Initiate ssh connection with selected colab
        supports only one colab for now.
        """
        colab_client = SSHClient()
        colab_client.load_system_host_keys()
        colab_client.set_missing_host_key_policy(AutoAddPolicy())

        setup_console.print(
            "[bold grey93 on black]Attempting connection to remote machine...[bold grey93 on black]"
        )

        try:
            colab_client.connect(
                hostname=self.hostname,
                auth_strategy=Password(self.setup.user, lambda: self.password),
                sock=ProxyCommand(
                    self.setup.proxy_command.replace(
                        "%h", self.hostname
                    )  # This replace is required by pramiko
                ),
                timeout=self.timeout,
            )
        except SSHException:
            setup_console.print_exception()
            exit()

        setup_console.print(f"\n[green]Connected to {self.hostname} successfully!")

        return colab_client

    def run_setup(self) -> Setup:
        """Trigger setup and fail fast if things are not in order."""
        return Setup()


if __name__ == "__main__":
    Connection(
        hostname="practitioner-books-render-villages.trycloudflare.com",
        password="123",
        timeout=1,
    )
