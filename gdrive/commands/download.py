"""Drive `download` command module."""

import os

from gdrive.commands import GoogleDriveCmd


class DriveDownloadCmd(GoogleDriveCmd):
    """Drive `download` command class."""

    def init_command(self) -> None:
        """Initialize drive `download` command."""

        parser = self.add_subcommand_parser(
            "download",
            help="download a file",
            description="download.description",
        )

        parser.add_argument(
            "file",
            metavar="FILE",
            help="file to download",
        )
        parser.add_argument(
            "rename",
            metavar="NEWNAME",
            nargs="?",
            help="local name to assign",
        )

    def run(self) -> None:
        """Run drive `download` command."""

        for target_filename in self.cli.api.download(
            self.options, self.options.file, self.options.rename
        ):
            self._ls_minus_el(target_filename)

    @staticmethod
    def _ls_minus_el(path) -> None:
        """Run `ls -l` on given `path`."""

        os.system("/bin/ls -l " + path)
