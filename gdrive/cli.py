"""Command Line Interface to Google Drive."""

from pathlib import Path

from libcli import BaseCLI

from gdrive.api import GoogleDriveAPI

__all__ = ["GoogleDriveCLI"]


class GoogleDriveCLI(BaseCLI):
    """Command Line Interface to Google Drive."""

    config = {
        # name of config file.
        "config-file": Path("~/.pygoogle.toml"),
        # toml [section-name].
        "config-name": "gdrive",
        # distribution name, not importable package name
        "dist-name": "rlane-gdrive",
    }

    api: GoogleDriveAPI  # connection to google service

    def init_parser(self) -> None:
        """Initialize argument parser."""

        self.ArgumentParser(
            prog=__package__,
            description="Google `drive` command line interface.",
            epilog="See `%(prog)s COMMAND --help` for help on a specific command.",
        )

    def add_arguments(self) -> None:
        """Add arguments to parser."""

        self.add_subcommand_modules("gdrive.commands", prefix="Drive", suffix="Cmd")

        self.parser.add_argument(
            "--all-fields",
            action="store_true",
            help="use parms['fields'] = '*' (be verbose)",
        )

    def main(self) -> None:
        """Command line interface entry point (method)."""

        if not self.options.cmd:
            self.parser.print_help()
            self.parser.exit(2, "error: Missing COMMAND\n")

        self.api = GoogleDriveAPI(self.options)
        self.options.cmd()


def main(args: list[str] | None = None) -> None:
    """Command line interface entry point (function)."""
    GoogleDriveCLI(args).main()
