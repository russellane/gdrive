"""Google Drive Commands."""

from argparse import ArgumentParser, _ArgumentGroup
from typing import Any, TypeVar

from libcli import BaseCmd
from loguru import logger
from rich.pretty import pprint as rich_pretty_print

from gdrive.cli import GoogleDriveCLI

Parser = TypeVar("Parser", ArgumentParser, _ArgumentGroup)

__all__ = ["GoogleDriveCmd"]


class GoogleDriveCmd(BaseCmd):
    """Base class of google drive commands."""

    cli: GoogleDriveCLI

    def add_limit_option(self, parser: Parser) -> None:
        """Add `--limit` to the given `parser`."""

        parser.add_argument(
            "--limit",
            type=int,
            help="limit execution to `LIMIT` number of items",
        )

    def check_limit(self) -> bool:
        """Call at top of loop before performing work."""

        if self.options.limit is None:
            logger.trace("No limit")
            return False

        self.options.limit -= 1
        logger.trace("limit {!r}", self.options.limit)
        assert isinstance(self.options.limit, int)
        return self.options.limit < 0

    def add_pretty_print_option(self, parser: Parser) -> None:
        """Add `--pretty-print` to the given `parser`."""

        parser.add_argument(
            "--pretty-print",
            action="store_true",
            help="pretty-print items",
        )

    @staticmethod
    def pprint(obj: Any, **kwargs: Any) -> None:
        """Make `pprint` convenient."""

        rich_pretty_print(obj, **kwargs)

    def add_long_listing_option(self, parser: Parser) -> None:
        """Add `--long-listing` to the given `parser`."""

        parser.add_argument(
            "-l",
            "--long-listing",
            action="store_true",
            help="use a long listing format",
        )

    @staticmethod
    def get_item_user_name(item: dict[str, Any]) -> str:
        """Return name of last user to modify this item."""

        try:
            return item["lastModifyingUser"]["displayName"]
        except KeyError:
            return "?"
