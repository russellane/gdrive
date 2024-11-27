"""Drive `uploaddir` command module."""

from libfile import File

from gdrive.commands import GoogleDriveCmd


class DriveUploaddirCmd(GoogleDriveCmd):
    """Drive `uploaddir` command class."""

    def init_command(self) -> None:
        """Initialize drive `uploaddir` command."""

        parser = self.add_subcommand_parser(
            "uploaddir",
            help="upload directories(s)",
            description="uploaddir.description",
        )

        parser.add_argument(
            "--add-timestamp",
            action="store_true",
            help="bake a timestamp into the target name",
        )

        parser.add_argument(
            "--convert",
            dest="convert",
            action="store_true",
            help="convert to google doc",
        )

        parser.add_argument(
            "--no-convert",
            dest="convert",
            action="store_false",
            help="do not convert to google doc",
        )

        parser.set_defaults(convert=True)

        parser.add_argument(
            "--target-folder",
            help="root of destination tree",
        )

        parser.add_argument(
            "path",
            metavar="PATH",
            nargs="*",
            help="file to upload",
        )

    def run(self) -> None:
        """Run drive `uploaddir` command."""

        for file in File.walk(self.options.path):
            self.cli.api.upload(self.options, file)
