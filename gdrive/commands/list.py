"""Drive `list` command module."""

import os

from gdrive.commands import GoogleDriveCmd


class DriveListCmd(GoogleDriveCmd):
    """Drive `list` command class."""

    def init_command(self) -> None:
        """Initialize drive `list` command."""

        parser = self.add_subcommand_parser(
            "list",
            help="list files and folders",
            description="list.description",
        )

        group = parser.add_mutually_exclusive_group()
        group.add_argument("-t", "--time", action="store_true", help="use a time listing format")
        self.add_long_listing_option(group)
        self.add_pretty_print_option(group)

        group = parser.add_mutually_exclusive_group()
        group.add_argument("-f", "--files-only", action="store_true", help="show files only")
        group.add_argument("-d", "--folders-only", action="store_true", help="show folders only")

        parser.add_argument(
            "-R",
            "--recursive",
            action="store_true",
            help="recurse into any sub-folders, recursively",
        )

        self.add_limit_option(parser)

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

            if self.check_limit():
                break

            if self.options.pretty_print:
                self.pprint(item)
                continue

            filename = item["PATH"]
            if self.cli.api.is_folder(item):
                filename += os.path.sep

            if self.options.time:
                print(str.format("{:s} {:s}", item["modifiedTime"], filename))

            elif self.options.long_listing:
                print(
                    str.format(
                        "{:<66s} {:<13s} {:s} {:s}",
                        item["mimeType"],
                        self.get_item_user_name(item),
                        item["modifiedTime"],
                        filename,
                    )
                )
            else:
                print(filename)
