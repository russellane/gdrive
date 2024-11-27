"""Drive `uploadfile` command module."""

from libfile import File

from gdrive.commands import GoogleDriveCmd


class DriveUploadfileCmd(GoogleDriveCmd):
    """Drive `uploadfile` command class."""

    def init_command(self) -> None:
        """Initialize drive `uploadfile` command."""

        parser = self.add_subcommand_parser(
            "uploadfile",
            help="upload file(s)",
            description="uploadfile.description",
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
            "path",
            metavar="PATH",
            help="file to upload",
        )

        parser.add_argument(
            "target_folder",
            metavar="FOLDER",
            help="destination folder",
        )

        parser.add_argument(
            "target_basename",
            metavar="NEWNAME",
            nargs="?",
            help="new name for target file",
        )

    def run(self) -> None:
        """Run drive `uploadfile` command."""

        for file in File.walk(self.options.path):
            self.cli.api.upload(self.options, file)
