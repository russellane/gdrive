import argparse
import os
import sys

import pytest

from gdrive.api import GoogleDriveAPI
from gdrive.cli import GoogleDriveCLI

disabled = pytest.mark.skipif(True, reason="disabled")
slow = pytest.mark.skipif(not os.environ.get("SLOW"), reason="slow")


@pytest.fixture(name="drive")
def drive_() -> GoogleDriveAPI:
    return GoogleDriveAPI()


def run_cli(options: list[str]) -> None:
    """Test calling the cli directly."""

    sys.argv = ["gdrive"]
    if options:
        sys.argv += options
    print(f"\nRunning {sys.argv!r}", flush=True)
    GoogleDriveCLI().main()


def test_gdrive_no_args() -> None:
    with pytest.raises(SystemExit) as err:
        run_cli([])
    assert err.value.code == 2


@pytest.fixture(name="args")
def fixture_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-action", action="store_true")
    parser.add_argument("target_folder", nargs="?")
    parser.add_argument("target_basename", nargs="?")
    return parser.parse_args([])


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
def test_list_1(drive, path):
    print()
    for _ in drive.list(path):
        print(_["PATH"])


def test_list_2(drive):
    print()
    path = "/test-data"
    for _ in drive.list(path, recursive=True):
        print(_["PATH"])


@pytest.mark.parametrize("path", ["/tmp/a/a/", "/tmp/a/b/", "/tmp/b/a/", "/tmp/b/b/"])
def test_makedirs_1(drive, path, args):
    print()
    _ = drive.makedirs(args, path)
    print(f"makedirs({path!r}) returned {_!r}")

    # print('all_folders after creating new folders')
    # for _ in drive.all_folders:
    #    print(_['PATH'])


@disabled
def test_round_trip_1(drive, args):
    print()

    name = "/test-data/test-doc"
    local_filename = drive.download(args, name)[0]
    print(str.format("name {} local {}", name, local_filename))

    args.target_folder = "/tmp"
    remote_filename = drive.upload(args, local_filename)[0]
    print(str.format("name {} local {} remote {}", name, local_filename, remote_filename))

    name = "/tmp/test-doc.docx"
    local_filename = drive.download(args, name)[0]
    print(str.format("name {} local {}", name, local_filename))

    args.target_folder_path = "/tmp"
    args.target_filename = "bobo"
    remote_filename = drive.upload(args, local_filename)[0]
    print(str.format("name {} local {} remote {}", name, local_filename, remote_filename))


# @disabled
# def test_round_trip_2(drive, args):
#     print()
#     for file in drive.list("/test-data/test-doc"):
#         horzrule()
#         if drive.is_folder(file):
#             continue
#         if not file["capabilities"]["canDownload"]:
#             print("SKIPPING NO CAN DOWNLOADABLE")
#             continue

#         print(str.format("name {}", file["PATH"]))
#         local_filename = drive.download(args, file["PATH"])
#         print(str.format("name {} local {}", file["PATH"], local_filename))
#         remote_filename = drive.upload(args, local_filename, target_folder_path="/tmp")
#         print(
#             str.format(
#                 "name {} local {} remote {}", file["PATH"], local_filename, remote_filename
#             )
#         )
#         print("NEVER")
#     print("HAPPENED")

# @disabled
# def test_round_trip_3(drive):
#     print()
#     for file in drive.list("/test-data"):
#         horzrule()
#         if drive.is_folder(file):
#             continue
#         if not file["capabilities"]["canDownload"]:
#             print("SKIPPING NO CAN DOWNLOADABLE")
#             continue
#         local_filename = drive.download(args, file["PATH"])
#         remote_filename = drive.upload(args, local_filename, target_folder_path="/tmp")
#         print(
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
# def test_upload_0(drive, args):
#     print()
#     path = Path("setup.py")
#     args.target_folder = Path("/tmp")
#     _ = drive.upload(args, path)
#     print(
#         str.format("upload({}, {}) returned {}", pformat(path), pformat(destdir), pformat(_))
#     )

# @disabled
# def test_upload_1(drive):
#     print()
#     path = "setup.py"
#     destdir = "/tmp/a/b/"
#     _ = drive.upload(args, path, destdir)
#     print(
#         str.format("upload({}, {}) returned {}", pformat(path), pformat(destdir), pformat(_))
#     )

# @disabled
# def test_upload_2(drive):
#     print()
#     path = "Makefile"
#     destdir = "/tmp/b/a/"
#     _ = drive.upload(args, path, destdir)
#     print(
#         str.format("upload({}, {}) returned {}", pformat(path), pformat(destdir), pformat(_))
#     )

# @disabled
# def test_upload_3(drive):
#     print()
#     _ = drive.upload(args, "Makefile", "/tmp", "Makefile.mk")
#     path = "Makefile"
#     destdir = "/tmp"
#     destfile = "Makefile.mk"
#     _ = drive.upload(args, path, destdir, destfile)
#     print(
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
def test_download_1(drive, path, args):
    print()
    _ = drive.download(args, path)
    print(f"download({path!r}) returned {_!r}")


# @pytest.mark.build
def test_about(drive):
    print()
    print(drive.about())
