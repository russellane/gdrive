"""Command Line Interface to Google Drive."""

from pathlib import Path
from typing import Any

from libcli import BaseCLI
from loguru import logger

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

    api: Any = None  # connection to google service

    def init_parser(self) -> None:
        """Initialize argument parser."""

        self.ArgumentParser(
            prog="gdrive",
            description="Google `drive` command line interface.",
            epilog="See `%(prog)s COMMAND --help` for help on a specific command.",
        )

    def add_arguments(self) -> None:
        """Add arguments to parser."""

        arg = self.parser.add_argument(
            "--limit",
            type=int,
            help="limit execution to `LIMIT` number of items",
        )
        self.add_default_to_help(arg)

        self.parser.add_argument(
            "--all-fields",
            action="store_true",
            help="use parms['fields'] = '*' (be verbose)",
        )

        self.add_subcommand_modules("gdrive.commands", prefix="Drive", suffix="Cmd")

    def main(self) -> None:
        """Command line interface entry point (method)."""

        if not self.options.cmd:
            self.parser.print_help()
            self.parser.exit(2, "error: Missing COMMAND\n")

        self.api = GoogleDriveAPI(self.options.all_fields)
        self.options.cmd()

    def check_limit(self):
        """Call at top of loop before performing work."""

        if self.options.limit is None:
            logger.trace("No limit")
            return False

        self.options.limit -= 1
        logger.trace("limit {!r}", self.options.limit)
        return self.options.limit < 0


def main(args: list[str] | None = None) -> None:
    """Command line interface entry point (function)."""
    GoogleDriveCLI(args).main()
