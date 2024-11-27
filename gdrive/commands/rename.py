"""Drive `rename` command module."""

from gdrive.commands import GoogleDriveCmd


class DriveRenameCmd(GoogleDriveCmd):
    """Drive `rename` command class."""

    def init_command(self) -> None:
        """Initialize drive `rename` command."""

        parser = self.add_subcommand_parser(
            "rename",
            help="rename file",
            description="rename.description",
        )

        parser.add_argument(
            "src",
            help="file to rename",
        )

        parser.add_argument(
            "target",
            help="new name",
        )

    def run(self) -> None:
        """Run drive `rename` command."""

        self.cli.api.rename(self.options, self.options.src, self.options.target)
