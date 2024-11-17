"""Drive `list` command module."""

import os

from libcli import BaseCmd


class DriveListCmd(BaseCmd):
    """Drive `list` command class."""

    def init_command(self) -> None:
        """Initialize drive `list` command."""

        parser = self.add_subcommand_parser(
            "list",
            help="list files and folders",
            description="list.description",
        )

        parser.add_argument(
            "-t",
            "--time",
            action="store_true",
            help="use a time listing format",
        )

        parser.add_argument(
            "-l",
            "--long-listing",
            action="store_true",
            help="use a long listing format",
        )

        parser.add_argument(
            "-f",
            "--files-only",
            action="store_true",
            help="show files only",
        )

        parser.add_argument(
            "-d",
            "--folders-only",
            action="store_true",
            help="show folders only",
        )

        parser.add_argument(
            "-R",
            "--recursive",
            action="store_true",
            help="recurse into any sub-folders, recursively",
        )

        parser.add_argument(
            "path",
            metavar="PATH",
            help="file or folder of items to list",
        )

    def run(self) -> None:
        """Run drive `list` command.

        List items at `PATH`.

        If path refers to a file, the file is listed;
        (note: there may be multiple files in a folder with the same name).
        If path refers to a folder, the folder's contents are listed.
        """

        for item in self.cli.api.list(
            self.options.path,
            self.options.files_only,
            self.options.folders_only,
            self.options.recursive,
        ):

            if self.cli.check_limit():
                break

            mimetype = item["mimeType"]
            filename = item["PATH"]
            if self.cli.api.is_folder(item):
                filename += os.path.sep

            if self.options.time:
                print(str.format("{:s} {:s}", item["modifiedTime"], filename))

            elif self.options.long_listing:
                if user := item.get("lastModifyingUser"):
                    user = user.get("displayName")
                print(
                    str.format(
                        "{:<66s} {:<13s} {:s} {:s}",
                        mimetype,
                        user or "?",
                        item["modifiedTime"],
                        filename,
                    )
                )
            else:
                # print(str.format("{:<66s} {:s}", mimetype, filename))
                print(filename)
