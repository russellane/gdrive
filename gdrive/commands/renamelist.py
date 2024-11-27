"""Drive `renamelist` command module."""

import json

from gdrive.commands import GoogleDriveCmd


class DriveRenamelistCmd(GoogleDriveCmd):
    """Drive `renamelist` command class."""

    def init_command(self) -> None:
        """Initialize drive `renamelist` command."""

        parser = self.add_subcommand_parser(
            "renamelist",
            help="rename list of files",
            description="renamelist.description",
        )

        parser.add_argument(
            "listfile",
            help="file with list of renames",
        )

    def run(self) -> None:
        """Run drive `renamelist` command."""

        oldroot = "/home/rlane/ext/Ginger/"
        oldrootlen = len(oldroot)
        newroot = "/Ginger-PC/"

        with open(self.options.listfile, encoding="utf-8") as file:

            for line in file:
                line = line.strip()
                if not line:
                    break

                j = json.loads(line)

                src = j["src"]
                assert src.startswith(oldroot)
                src = newroot + src[oldrootlen:]

                target = j["target"]
                assert target.startswith(oldroot)
                target = newroot + target[oldrootlen:]

                self.cli.api.rename(self.options, src, target)
