"""Drive `files` command module."""

from gdrive.commands import GoogleDriveCmd


class DriveFilesCmd(GoogleDriveCmd):
    """Drive `files` command class."""

    def init_command(self) -> None:
        """Initialize drive `files` command."""

        parser = self.add_subcommand_parser(
            "files",
            help="list all files",
            description="files.description",
        )

        group = parser.add_mutually_exclusive_group()
        self.add_long_listing_option(group)
        self.add_pretty_print_option(group)
        self.add_limit_option(parser)

    def run(self) -> None:
        """Run drive `files` command."""

        for file in self.cli.api.all_files:

            if self.check_limit():
                break

            if self.options.pretty_print:
                self.pprint(file)

            elif self.options.long_listing:
                print(
                    str.format(
                        "{:<40s} {:<13s} {:s} {:s}",
                        file["id"],
                        self.get_item_user_name(file),
                        file["modifiedTime"],
                        file["PATH"],
                    )
                )
            else:
                print(file["PATH"])
