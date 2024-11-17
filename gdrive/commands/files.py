"""Drive `files` command module."""

from libcli import BaseCmd


class DriveFilesCmd(BaseCmd):
    """Drive `files` command class."""

    def init_command(self) -> None:
        """Initialize drive `files` command."""

        parser = self.add_subcommand_parser(
            "files",
            help="list all files",
            description="files.description",
        )

        parser.add_argument(
            "-l",
            "--long-listing",
            action="store_true",
            help="use a long listing format",
        )

    def run(self) -> None:
        """Run drive `files` command."""

        for file in self.cli.api.all_files:
            if self.options.long_listing:
                print(
                    str.format(
                        "{:<40s} {:<13s} {:s} {:s}",
                        file["id"],
                        file["lastModifyingUser"]["displayName"],
                        file["modifiedTime"],
                        file["PATH"],
                    )
                )
            else:
                print(file["PATH"])
