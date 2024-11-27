"""Interface to Google Drive."""

import os
import time
from argparse import Namespace

import xdg
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from loguru import logger

from gdrive.google import connect_to_google

__all__ = ["GoogleDriveAPI"]


class GoogleDriveAPI:
    """Interface to Google Drive.

    See https://developers.google.com/gdrive/api/v1/reference
    """

    _GOOGLE_MIMETYPE_FOLDER = "application/vnd.google-apps.folder"

    @classmethod
    def is_folder(cls, file):
        """Return True if mimetype is a Google Drive Folder."""
        return file["mimeType"] == cls._GOOGLE_MIMETYPE_FOLDER

    _GOOGLE_MIMETYPES = {}
    for file in (
        {
            "extension": ".docx",
            "google": "application/vnd.google-apps.document",
            "openxml": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        },
        {
            "extension": ".xlsx",
            "google": "application/vnd.google-apps.spreadsheet",
            "openxml": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        },
        {
            "extension": ".pptx",
            "google": "application/vnd.google-apps.presentation",
            "openxml": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        },
    ):
        _GOOGLE_MIMETYPES[file["extension"]] = file
        _GOOGLE_MIMETYPES[file["google"]] = file
        _GOOGLE_MIMETYPES[file["openxml"]] = file

    _FILE_ATTRS = ", ".join(
        [
            "parents",
            "id",
            "name",
            "mimeType",
            "modifiedTime",
            "lastModifyingUser/displayName",
            "capabilities/canDownload",
        ]
    )

    def __init__(self, options: Namespace) -> None:
        """Connect to Google Drive."""

        self.options = options
        self.service = connect_to_google("drive", "v3")
        self.download_dir = xdg.xdg_data_home() / "pygoogle-gdrive"

        # Properties
        self._root_folder = None
        self._shared_with_me_folder = None
        self._all_folders = None
        self._all_files = None
        self._items_by_id = None

    @property
    def root_folder(self):
        """Return the top-level folder, a.k.a. ``My Drive``."""

        if not self._root_folder:
            self._root_folder = self._get_item_by_id("root")
            self._root_folder["PATH"] = os.path.sep + self._root_folder["name"]
            self._root_folder["PARENT"] = None

        return self._root_folder

    def _get_item_by_id(self, id):
        """Return item with matching ``id``."""

        # https://developers.google.com/drive/api/v3/reference/files/get
        parms = {}
        parms["fileId"] = id
        parms["fields"] = "*" if self.options.all_fields else self._FILE_ATTRS

        logger.debug("service.files().get({!r})", parms)
        response = self.service.files().get(**parms).execute()  # noqa: PLE101
        logger.trace("response {!r}", response)

        return response

    @property
    def shared_with_me_folder(self):
        """Return pseudo-folder for items ``Shared with me``."""

        if not self._shared_with_me_folder:

            name = "Shared with me"

            self._shared_with_me_folder = {
                "id": "shared-with-me",
                "name": name,
                "PATH": os.path.sep + name,
                "PARENT": None,
                "mimeType": self._GOOGLE_MIMETYPE_FOLDER,
                "lastModifyingUser": {"displayName": "-"},
                "capabilities": {"canDownload": False},
                "modifiedTime": "-",
            }

        return self._shared_with_me_folder

    @property
    def all_folders(self):
        """Return list of all folders sorted by ``PATH``."""

        if self._all_folders:
            return self._all_folders

        # https://developers.google.com/drive/api/v3/reference/files/list
        parms = {}
        parms["fields"] = (
            "*"
            if self.options.all_fields
            else "nextPageToken, files({})".format(self._FILE_ATTRS)
        )
        parms["q"] = "not trashed"
        parms["q"] += ' and mimeType="{:s}"'.format(self._GOOGLE_MIMETYPE_FOLDER)

        folders = []
        while True:
            logger.debug("service.files().list({!r})", parms)
            response = self.service.files().list(**parms).execute()  # noqa: PLE101
            logger.trace("response {!r}", response)

            files = response.get("files", [])
            folders.extend(files)

            parms["pageToken"] = response.get("nextPageToken")
            if not parms["pageToken"]:
                break

        # build lookup map
        self._items_by_id = {}

        # these items are not in response; their PATH and PARENT attributes are already set.
        for folder in (self.root_folder, self.shared_with_me_folder):
            self._items_by_id[folder["id"]] = folder

        # add items from the response
        for folder in folders:
            self._items_by_id[folder["id"]] = folder

        # lookup map built; now we can link each item to its (first) parent.
        for folder in folders:
            ids = folder.get("parents")
            folder["PARENT"] = self._items_by_id[ids[0]] if ids else self.shared_with_me_folder

        # and now we can utilize the links to
        # set each folder's absolute, fully-qualified PATH.
        for folder in folders:
            names = []
            node = folder
            while node:
                names.append(node["name"])
                node = node.get("PARENT")
            names.reverse()
            folder["PATH"] = os.path.join(os.path.sep, *names)

        # create and return a sorted list
        self._all_folders = sorted(self._items_by_id.values(), key=lambda _: _["PATH"].lower())
        return self._all_folders

    def _add_folder(self, folder):
        """Add folder to list of all folders, maintaining sort order."""

        for index, value in enumerate(self._all_folders):
            if value["PATH"] > folder["PATH"]:
                self._all_folders.insert(index, folder)
                self._items_by_id[folder["id"]] = folder
                return

        self._all_folders.append(folder)
        self._items_by_id[folder["id"]] = folder

    def _lookup_folder_by_path(self, path):
        """Return the folder with the matching ``PATH``."""

        folders = [x for x in self.all_folders if x["PATH"] == path]
        return folders[0] if folders else None

    @property
    def all_files(self):
        """Return list of all files sorted by ``PATH``."""

        if self._all_files:
            return self._all_files

        _ = self.all_folders

        # https://developers.google.com/drive/api/v3/reference/files/list
        parms = {}
        parms["fields"] = (
            "*"
            if self.options.all_fields
            else "nextPageToken, files({})".format(self._FILE_ATTRS)
        )
        parms["q"] = "not trashed"
        parms["q"] += ' and mimeType!="{:s}"'.format(self._GOOGLE_MIMETYPE_FOLDER)

        items = []
        while True:
            logger.debug("service.files().list({!r})", parms)
            response = self.service.files().list(**parms).execute()  # noqa: PLE101
            logger.trace("response {!r}", response)

            files = response.get("files", [])
            items.extend(files)

            parms["pageToken"] = response.get("nextPageToken")
            if not parms["pageToken"]:
                break

        # point each item to its parent
        for item in items:
            ids = item.get("parents")
            item["PARENT"] = self._items_by_id[ids[0]] if ids else self.shared_with_me_folder
            item["PATH"] = os.path.join(item["PARENT"]["PATH"], item["name"])

        # create and return a sorted list
        self._all_files = sorted(items, key=lambda _: _["PATH"].lower())

        return self._all_files

    def list(self, path, files_only=False, folders_only=False, recursive=False):
        """Generate list of items at ``PATH``."""

        path = self._normalize_drive_path(path)

        nitems = 0  # noqa
        for item in self._get_items_at_path(path):
            nitems += 1  # noqa:

            if self.is_folder(item):

                if not files_only:
                    # yield the folder
                    yield item

                # yield the folder's contents
                yield from self._list(item, path, files_only, folders_only, recursive)

            else:
                if not folders_only:
                    # yield the file
                    yield item

        if not nitems:
            logger.error("FileNotFoundError {!r}", path)

    def _normalize_drive_path(self, path):
        """Normalize path to be absolute, fully-qualified from the root."""

        # remove leading and trailing slashes.
        # reduce doubled slashes to a single slash.

        if path:
            path = os.path.normpath(path)
            if path[0] == os.path.sep:
                path = path[1:]

        if not path:
            path = self.root_folder["name"]
        elif not path.startswith(self.root_folder["name"]) and not path.startswith(
            self.shared_with_me_folder["name"]
        ):
            path = os.path.join(self.root_folder["name"], path)

        if not path.startswith(os.path.sep):
            path = os.path.sep + path

        return path

    def _get_items_at_path(self, path):
        """Return items at ``path``."""

        # does path refer to a folder?
        folder = self._lookup_folder_by_path(path)
        if folder:
            yield folder
            return  # yes

        # does path refer to a file within a folder?
        dirname, filename = os.path.split(path)
        folder = self._lookup_folder_by_path(dirname)
        if not folder:
            return  # no

        # there may be multiple items in the same folder with the same filename.
        for item in self._search(folder, filename):
            item["PATH"] = os.path.join(folder["PATH"], filename)
            item["PARENT"] = folder
            yield item

    def _search(
        self,
        parent,
        name=None,
        files_only=False,
        folders_only=False,
        recursive=False,
    ):
        """Generate list of matching items."""

        # pylint: disable=too-many-positional-arguments

        # https://developers.google.com/drive/api/v3/reference/files/list

        parms = {}
        parms["fields"] = (
            "*"
            if self.options.all_fields
            else "nextPageToken, files({})".format(self._FILE_ATTRS)
        )
        parms["q"] = "not trashed"

        if name:
            parms["q"] += " and name='{:s}'".format(name.replace("'", "\\'"))

        if parent == self.shared_with_me_folder:
            parms["q"] += " and sharedWithMe=true"
        elif parent:
            parms["q"] += ' and "{:s}" in parents'.format(parent["id"])

        if files_only and not recursive:
            parms["q"] += ' and mimeType!="{:s}"'.format(self._GOOGLE_MIMETYPE_FOLDER)

        if folders_only:
            parms["q"] += ' and mimeType="{:s}"'.format(self._GOOGLE_MIMETYPE_FOLDER)

        while True:
            logger.debug("service.files().list({!r})", parms)
            response = self.service.files().list(**parms).execute()  # noqa: PLE101
            logger.trace("response {!r}", response)

            yield from response.get("files", [])

            parms["pageToken"] = response.get("nextPageToken")
            if parms["pageToken"] is None:
                return

    def _list(self, parent, path, files_only, folders_only, recursive):
        """Generate list of items at ``path``, which must be an existing drive folder."""

        # pylint: disable=too-many-positional-arguments

        # Get the contents of the folder as a list of folders, and a list of files.

        folders = []
        files = []

        for item in self._search(
            parent, files_only=files_only, folders_only=folders_only, recursive=recursive
        ):
            item["PATH"] = os.path.join(path, item["name"])
            if self.is_folder(item):
                folders.append(item)
            else:
                files.append(item)

        # the files...

        yield from sorted(files, key=lambda _: _["name"].lower())

        # the folders...

        folders = sorted(folders, key=lambda _: _["name"].lower())

        if not recursive:
            yield from folders
            return

        for folder in folders:
            subfolder = os.path.join(path, folder["name"])
            yield from self.list(subfolder, files_only, folders_only, recursive)

    def makedirs(self, args, path):
        """Create folder.

        No error if existing, make parent directories as needed; (like ``mkdir -p path``)
        """

        path = self._normalize_drive_path(path)
        folders = [x for x in path.split(os.path.sep) if x]

        parent = self.root_folder
        folder = None

        for name in folders[1:]:
            path = os.path.join(parent["PATH"], name)
            folder = self._lookup_folder_by_path(path)
            if not folder:
                folder = self._create_folder(args, name, parent)
            parent = folder

        return folder

    def _create_folder(self, args, name, parent):
        """Create folder ``name`` in folder ``parent``."""

        # https://developers.google.com/drive/api/v3/reference/files/create

        parms = {
            "body": {
                "name": name,
                "mimeType": self._GOOGLE_MIMETYPE_FOLDER,
                "fields": "id",
                "parents": [parent["id"]],
            },
        }

        if args.no_action:
            logger.warning("Not running service.files().create({!r})", parms)
            response = {"FAKE-FOLDER": "--no-action"}
            response["PATH"] = os.path.join(parent["PATH"], name)
            response["PARENT"] = parent
            args.no_action += 1
            response["id"] = "fake-id-{}".format(args.no_action)
            return response

        logger.info("service.files().create({!r})", parms)
        response = self.service.files().create(**parms).execute()  # noqa: PLE101
        logger.debug("response {!r}", response)

        # Update cache
        id = response.get("id")
        folder = self._get_item_by_id(id)
        folder["PATH"] = os.path.join(parent["PATH"], folder["name"])
        folder["PARENT"] = parent
        self._add_folder(folder)

        return folder

    def download(self, args, path, rename=None):
        """Copy file at ``path`` from google drive to current working directory.

        Returns name of new file.
        """

        path = self._normalize_drive_path(path)

        #
        target_filenames = []
        for item in self._get_items_at_path(path):
            target_filenames.append(
                self._download(args, item, path, rename, len(target_filenames))
            )

        if not target_filenames:
            logger.error("FileNotFoundError {!r}", path)

        return target_filenames

    def _download(self, args, file, path, rename, itemno):
        """docstring."""

        # pylint: disable=too-many-positional-arguments

        if self.is_folder(file):
            logger.error("IsADirectoryError {!r}", path)
            return None

        target_filename = rename or file["name"]  # in current working directory

        # use export_media for known types, else get_media for binary.

        gmt = self._GOOGLE_MIMETYPES.get(file["mimeType"])
        if gmt:

            ext = gmt["extension"]
            if not path.endswith(ext):
                logger.warning("{!r} expecting {!r} for {!r}", path, ext, file["mimeType"])
                target_filename += ext

            if itemno:
                root, ext = os.path.splitext(target_filename)
                target_filename = root + "(" + str(itemno + 1) + ")" + ext

            # https://developers.google.com/drive/api/v3/reference/files/export
            parms = {}
            parms["fileId"] = file["id"]
            parms["mimeType"] = gmt["openxml"]
            logger.debug("Converting {!r} -> {!r}", file["mimeType"], parms["mimeType"])

            if args.no_action:
                logger.warning("Not running service.files().export_media({!r})", parms)
                return None

            logger.debug("service.files().export_media({!r})", parms)
            request = self.service.files().export_media(**parms)  # noqa: PLE101

        else:
            # https://developers.google.com/drive/api/v3/reference/files/get
            parms = {}
            parms["fileId"] = file["id"]

            if args.no_action:
                logger.warning("service.files().get_media({!r})", parms)
                return None

            logger.debug("service.files().get_media({!r})", parms)
            request = self.service.files().get_media(**parms)  # noqa: PLE101

        #
        logger.debug("request {!r}", request)
        logger.info("Downloading {!r} -> {!r}", path, target_filename)

        with open(target_filename, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                logger.debug("Download progress {}%", int(status.progress() * 100))

        return target_filename

    def upload(self, args, file):
        """Upload single regular file.

             Any looping or walking of the filesystem is for the caller to do.


             Given `find ./testpictree -type f -ls`:
        249370     40 -rwxrwxrwx   1 rlane    rlane       37407 Jun 20 18:14 ./testpictree/2007-10/file1.jpg
        249372   5172 -rwxrwxrwx   1 rlane    rlane     5295103 Jun 20 18:14 ./testpictree/2013-05/file2.jpg
        249373   6732 -rwxrwxrwx   1 rlane    rlane     6891634 Jun 20 18:14 ./testpictree/2013-05/file3.jpg

             run-test-1:
                 uploaddir --target-folder /folder/subdir ./testpictree

             expect-test-1:
                 gdrive://folder/subdir/2007-10/file1.jpg
                 gdrive://folder/subdir/2013-05/file2.jpg
                 gdrive://folder/subdir/2013-05/file3.jpg
        """

        # assert file.isfile

        #
        target_folder_pathname = (
            args.target_folder if args.target_folder else self.root_folder["PATH"]
        )

        dirname, target_basename = os.path.split(file.pathname)

        if args.command != "uploadlist" and dirname:
            target_folder_pathname = os.path.join(target_folder_pathname, dirname)

        if args.add_timestamp:
            target_basename = str(int(time.time())) + "-" + target_basename
        target_pathname = os.path.join(target_folder_pathname, target_basename)

        target_folder = self._lookup_folder_by_path(target_folder_pathname)
        if not target_folder:
            target_folder = self.makedirs(args, target_folder_pathname)

        # https://developers.google.com/drive/api/v3/reference/files/create\#request-body
        parms = {}
        parms["media_body"] = MediaFileUpload(file.pathname)
        parms["fields"] = "*" if self.options.all_fields else self._FILE_ATTRS
        parms["body"] = {}
        parms["body"]["name"] = target_basename
        if target_folder:
            parms["body"]["parents"] = [target_folder["id"]]

        if args.convert:
            _, extension = os.path.splitext(target_basename)
            gmt = self._GOOGLE_MIMETYPES.get(extension)
            if gmt:
                parms["body"]["mimeType"] = gmt["google"]
                logger.debug(
                    "converting to google mimetype {!r} for ext {!r}",
                    parms["body"]["mimeType"],
                    extension,
                )
            else:
                try:
                    # `/usr/bin/file file | grep -q ASCII`
                    magic_string = magic.from_buffer(open(file).read(1024))  # noqa:
                    if magic_string.find("ASCII") >= 0:
                        if target_basename.endswith(".csv"):
                            parms["body"]["mimeType"] = "text/csv"
                        else:
                            parms["body"]["mimeType"] = "text/plain"
                except Exception:  # pylint: disable=broad-exception-caught
                    pass

        if args.no_action:
            logger.warning("Not running service.files().create({!r})", parms)
            response = {"FAKE-FILE": "--no-action"}
        else:
            logger.info("Uploading {!r}", target_pathname)
            logger.debug("service.files().create({!r})", parms)

            try:
                response = self.service.files().create(**parms).execute()  # noqa: PLE101
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error("{!r} {}", target_pathname, e)
                response = {"ERROR": str(e)}

        logger.trace("response {!r}", response)
        response["PATH"] = target_pathname
        response["PARENT"] = target_folder
        return response  # https://developers.google.com/drive/api/v3/reference/files\#resource

    def rename(self, args, oldpath, newpath):
        """Docstring."""

        oldpath = self._normalize_drive_path(oldpath)
        newpath = self._normalize_drive_path(newpath)

        newhead, newtail = os.path.split(newpath)

        # make sure old file exists
        old = None
        for old in self._get_items_at_path(oldpath):  # noqa:
            break
        if not old:
            logger.error("Can't find {!r}", oldpath)
            return
        # logger.debug('old {!r}', old)

        # make sure the target directory exists
        target_folder = self._lookup_folder_by_path(newhead)
        if not target_folder:
            target_folder = self.makedirs(args, newhead)
        else:
            # logger.debug('target_folder exists {!r}', target_folder)
            # make sure new file does not exist
            for new in self._get_items_at_path(newpath):
                logger.error("file already exists at {!r}", new)
                return

        # https://developers.google.com/drive/api/v3/reference/files/update

        parms = {}
        parms["fileId"] = old["id"]
        parms["addParents"] = target_folder["id"]
        parms["removeParents"] = old["PARENT"]["id"]

        if newtail != os.path.basename(oldpath):
            parms["body"] = {}
            parms["body"]["name"] = newtail

        if args.no_action:
            logger.warning("Not running service.files().update({})", str(parms))
        else:
            logger.info("Renaming {!r} -> {!r}", oldpath, newpath)
            logger.debug("service.files().update({!r})", parms)
            response = self.service.files().update(**parms).execute()  # noqa: PLE101
            logger.trace("response {!r}", response)

    def about(self):
        """Get and return information about the google user and drive."""

        # https://developers.google.com/drive/api/v3/reference/about/get
        parms = {}
        parms["fields"] = "*" if self.options.all_fields else "storageQuota, user"

        logger.debug("service.about().get({!r})", parms)
        response = self.service.about().get(**parms).execute()  # noqa: PLE101
        logger.trace("response {!r}", response)

        return response
