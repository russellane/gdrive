"""Drive `about` command module."""

from gdrive.commands import GoogleDriveCmd


class DriveAboutCmd(GoogleDriveCmd):
    """Drive `about` command class."""

    def init_command(self) -> None:
        """Initialize drive `about` command."""

        parser = self.add_subcommand_parser(
            "about",
            help="get information about the google user and drive",
            description="about.description",
        )

        parser.add_argument(
            "--no-themes",
            action="store_true",
            help="remove theme elements; (implies --all-fields)",
        )

        self.add_pretty_print_option(parser)

    def run(self) -> None:
        """Perform the command."""

        if self.options.no_themes:
            self.options.all_fields = True
            self.cli.api.all_fields = True

        about = self.cli.api.about()

        if self.options.no_themes:
            about.pop("driveThemes", None)
            about.pop("teamDriveThemes", None)

        if self.options.pretty_print:
            self.pprint(about)
        else:
            print(about)
