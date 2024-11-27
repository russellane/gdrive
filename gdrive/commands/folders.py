"""Drive `folders` command module."""

from gdrive.commands import GoogleDriveCmd


class DriveFoldersCmd(GoogleDriveCmd):
    """Drive `folders` command class."""

    def init_command(self) -> None:
        """Initialize drive `folders` command."""

        parser = self.add_subcommand_parser(
            "folders",
            help="list all folders",
            description="folders.description",
        )

        group = parser.add_mutually_exclusive_group()
        self.add_long_listing_option(group)
        self.add_pretty_print_option(group)
        self.add_limit_option(parser)

    def run(self) -> None:
        """Run drive `folders` command."""

        for folder in self.cli.api.all_folders:

            if self.check_limit():
                break

            if self.options.pretty_print:
                self.pprint(folder)

            elif self.options.long_listing:
                print(
                    str.format(
                        "{:<40s} {:<13s} {:s} {:s}",
                        folder["id"],
                        self.get_item_user_name(folder),
                        folder["modifiedTime"],
                        folder["PATH"],
                    )
                )
            else:
                print(folder["PATH"])
