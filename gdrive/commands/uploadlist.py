"""Drive `uploadlist` command module."""

import json
import os

from libfile import File

from gdrive.commands import GoogleDriveCmd


class DriveUploadlistCmd(GoogleDriveCmd):
    """Drive `uploadlist` command class."""

    def init_command(self) -> None:
        """Initialize drive `uploadlist` command."""

        parser = self.add_subcommand_parser(
            "uploadlist",
            help="upload list of files",
            description="uploadlist.description",
        )

        parser.add_argument(
            "--no-themes",
            action="store_true",
            help="remove theme elements; (implies --all-fields)",
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
            help="destination folder",
        )

        parser.add_argument(
            "listfile",
            help="file with list of uploads",
        )

    def run(self) -> None:
        """Run drive `uploadlist` command."""

        oldroot = "/home/rlane/ext/Ginger/"
        newroot = "/My Drive/Ginger-PC/"

        with open(self.options.listfile, encoding="utf-8") as file:

            for line in file:
                line = line.strip()
                if not line:
                    break

                j = json.loads(line)

                src = j["src"]
                assert src.startswith(oldroot)
                # src = newroot + src[oldrootlen:]

                target = j["target"]
                assert target.startswith(newroot)
                # target = newroot + target[oldrootlen:]

                self.options.target_folder = os.path.dirname(target)

                file = File(src)

                # logger.error('src {!r} target_folder {!r}', file, self.options.target_folder)

                self.cli.api.upload(self.options, file)
