import webbrowser

import pyperclip

from . import setup_console


def guide(
    colab_links: list[str] = [
        "https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb"
        # Additional colab links to be passed on from main handler later on.
    ],
) -> str:

    password = setup_console.input(
        "[bold grey93 on black]$Select a ssh password: ", password=True
    )
    pyperclip.copy(
        f"""
# Install colab_ssh on google colab
!pip install colab_ssh --upgrade

from colab_ssh import launch_ssh_cloudflared
launch_ssh_cloudflared(password="{password}")
"""
    )

    for link in colab_links:
        setup_console.print(
            (
                "\n[bold grey93 on black]$Opening colab...[bold grey93 on black]\n\nCreate a new cell and press ctrl/cmd + p"
                " and run the cell, after cell execution copy the cloudflared server name"
            )
        )

        webbrowser.open_new_tab(link)

    hostname = setup_console.input("\n\n[bold grey93 on black]$ssh-hostname: ")

    pyperclip.copy("")
    return hostname, password
