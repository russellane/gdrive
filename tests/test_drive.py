import argparse

# from pathlib import Path
from pprint import pformat

import pytest

from gdrive.api import GoogleDriveAPI
from tests.testlib import disabled, horzrule, tprint

drive = None


@pytest.fixture
def _connect():
    global drive  # noqa: PLW603
    if not drive:
        drive = GoogleDriveAPI()


@pytest.fixture(name="args")
def fixture_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-action", action="store_true")
    parser.add_argument("target_folder", nargs="?")
    parser.add_argument("target_basename", nargs="?")
    return parser.parse_args([])


@pytest.mark.usefixtures("_connect")
class TestGoogleDrive:
    # @pytest.mark.build
    @pytest.mark.parametrize(
        "path",
        [
            "/",
            # "/test-data",
            # "/test-data/test-doc",
            # "/My Drive/",
            # "/My Drive/test-data",
            # "/My Drive/test-data/test-doc",
        ],
    )
    def test_list_1(self, path):
        tprint()
        horzrule()
        for _ in drive.list(path):
            tprint(_["PATH"])

    def test_list_2(self):
        tprint()
        path = "/test-data"
        for _ in drive.list(path, recursive=True):
            tprint(_["PATH"])

    @pytest.mark.parametrize("path", ["/tmp/a/a/", "/tmp/a/b/", "/tmp/b/a/", "/tmp/b/b/"])
    def test_makedirs_1(self, path, args):
        tprint()
        _ = drive.makedirs(args, path)
        tprint(str.format("makedirs({}) returned {}", pformat(path), pformat(_)))

        # tprint('all_folders after creating new folders')
        # for _ in drive.all_folders:
        #    tprint(_['PATH'])

    @disabled
    def test_round_trip_1(self, args):
        tprint()

        name = "/test-data/test-doc"
        local_filename = drive.download(args, name)[0]
        tprint(str.format("name {} local {}", name, local_filename))

        args.target_folder = "/tmp"
        remote_filename = drive.upload(args, local_filename)[0]
        tprint(str.format("name {} local {} remote {}", name, local_filename, remote_filename))

        name = "/tmp/test-doc.docx"
        local_filename = drive.download(args, name)[0]
        tprint(str.format("name {} local {}", name, local_filename))

        args.target_folder_path = "/tmp"
        args.target_filename = "bobo"
        remote_filename = drive.upload(args, local_filename)[0]
        tprint(str.format("name {} local {} remote {}", name, local_filename, remote_filename))

    # @disabled
    # def test_round_trip_2(self, args):
    #     tprint()
    #     for file in drive.list("/test-data/test-doc"):
    #         horzrule()
    #         if drive.is_folder(file):
    #             continue
    #         if not file["capabilities"]["canDownload"]:
    #             tprint("SKIPPING NO CAN DOWNLOADABLE")
    #             continue

    #         tprint(str.format("name {}", file["PATH"]))
    #         local_filename = drive.download(args, file["PATH"])
    #         tprint(str.format("name {} local {}", file["PATH"], local_filename))
    #         remote_filename = drive.upload(args, local_filename, target_folder_path="/tmp")
    #         tprint(
    #             str.format(
    #                 "name {} local {} remote {}", file["PATH"], local_filename, remote_filename
    #             )
    #         )
    #         tprint("NEVER")
    #     tprint("HAPPENED")

    # @disabled
    # def test_round_trip_3(self):
    #     tprint()
    #     for file in drive.list("/test-data"):
    #         horzrule()
    #         if drive.is_folder(file):
    #             continue
    #         if not file["capabilities"]["canDownload"]:
    #             tprint("SKIPPING NO CAN DOWNLOADABLE")
    #             continue
    #         local_filename = drive.download(args, file["PATH"])
    #         remote_filename = drive.upload(args, local_filename, target_folder_path="/tmp")
    #         tprint(
    #             str.format(
    #                 "name {} local {} remote {}", file["PATH"], local_filename, remote_filename
    #             )
    #         )

    # Spreadsheet
    # Document
    # Text
    # Image
    # Send different types of files, let google assign mimetype.
    # Send different types of files, we specify mimetype.

    # @disabled
    # def test_upload_0(self, args):
    #     tprint()
    #     path = Path("setup.py")
    #     args.target_folder = Path("/tmp")
    #     _ = drive.upload(args, path)
    #     tprint(
    #         str.format("upload({}, {}) returned {}", pformat(path), pformat(destdir), pformat(_))
    #     )

    # @disabled
    # def test_upload_1(self):
    #     tprint()
    #     path = "setup.py"
    #     destdir = "/tmp/a/b/"
    #     _ = drive.upload(args, path, destdir)
    #     tprint(
    #         str.format("upload({}, {}) returned {}", pformat(path), pformat(destdir), pformat(_))
    #     )

    # @disabled
    # def test_upload_2(self):
    #     tprint()
    #     path = "Makefile"
    #     destdir = "/tmp/b/a/"
    #     _ = drive.upload(args, path, destdir)
    #     tprint(
    #         str.format("upload({}, {}) returned {}", pformat(path), pformat(destdir), pformat(_))
    #     )

    # @disabled
    # def test_upload_3(self):
    #     tprint()
    #     _ = drive.upload(args, "Makefile", "/tmp", "Makefile.mk")
    #     path = "Makefile"
    #     destdir = "/tmp"
    #     destfile = "Makefile.mk"
    #     _ = drive.upload(args, path, destdir, destfile)
    #     tprint(
    #         str.format(
    #             "upload({}, {}, {}) returned {}",
    #             pformat(path),
    #             pformat(destdir),
    #             pformat(destfile),
    #             pformat(_),
    #         )
    #     )

    @disabled
    @pytest.mark.parametrize(
        "path",
        ["/tmp/bobo", "20190823_170238.jpg", "/tmp/20190823_170238.jpg"],
    )
    def test_download_1(self, path, args):
        tprint()
        _ = drive.download(args, path)
        tprint(str.format("download({}) returned {}", pformat(path), pformat(_)))

    # @pytest.mark.build
    def test_about(self):
        tprint()
        tprint(drive.about())
