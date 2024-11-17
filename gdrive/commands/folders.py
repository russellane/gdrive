"""Drive `folders` command module."""

from libcli import BaseCmd


class DriveFoldersCmd(BaseCmd):
    """Drive `folders` command class."""

    def init_command(self) -> None:
        """Initialize drive `folders` command."""

        parser = self.add_subcommand_parser(
            "folders",
            help="list all folders",
            description="folders.description",
        )

        parser.add_argument(
            "-l",
            "--long-listing",
            action="store_true",
            help="use a long listing format",
        )

    def run(self) -> None:
        """Run drive `folders` command."""

        for folder in self.cli.api.all_folders:
            if self.options.long_listing:
                print(
                    str.format(
                        "{:<40s} {:<13s} {:s} {:s}",
                        folder["id"],
                        folder["lastModifyingUser"]["displayName"],
                        folder["modifiedTime"],
                        folder["PATH"],
                    )
                )
            else:
                print(folder["PATH"])
