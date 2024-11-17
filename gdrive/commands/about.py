"""Drive `about` command module."""

from libcli import BaseCmd


class DriveAboutCmd(BaseCmd):
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

    def run(self) -> None:
        """Perform the command."""

        if not self.options.no_themes:
            self.options.all_fields = True
            self.cli.api.all_fields = True

        about = self.cli.api.about()

        if self.options.no_themes:
            about.pop("driveThemes", None)
            about.pop("teamDriveThemes", None)

        print(about)
