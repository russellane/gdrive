# gdrive
```
usage: gdrive [--all-fields] [-h] [-H] [-v] [-V] [--config FILE]
              [--print-config] [--print-url] [--completion [SHELL]]
              COMMAND ...

Google `drive` command line interface.

options:
  --all-fields          Use parms['fields'] = '*' (be verbose).

Specify one of:
  COMMAND
    about               Get information about the google user and drive.
    download            Download a file.
    files               List all files.
    folders             List all folders.
    list                List files and folders.
    rename              Rename file.
    renamelist          Rename list of files.
    uploaddir           Upload directories(s).
    uploadfile          Upload file(s).
    uploadlist          Upload list of files.

General options:
  -h, --help            Show this help message and exit.
  -H, --long-help       Show help for all commands and exit.
  -v, --verbose         `-v` for detailed output and `-vv` for more detailed.
  -V, --version         Print version number and exit.
  --config FILE         Use config `FILE` (default: `~/.pygoogle.toml`).
  --print-config        Print effective config and exit.
  --print-url           Print project url and exit.
  --completion [SHELL]  Print completion scripts for `SHELL` and exit
                        (default: `bash`).

See `gdrive COMMAND --help` for help on a specific command.
```

## gdrive about
```
usage: gdrive about [-h] [--no-themes] [--pretty-print]

about.description

options:
  -h, --help      Show this help message and exit.
  --no-themes     Remove theme elements; (implies --all-fields).
  --pretty-print  Pretty-print items.
```

## gdrive download
```
usage: gdrive download [-h] FILE [NEWNAME]

download.description

positional arguments:
  FILE        File to download.
  NEWNAME     Local name to assign.

options:
  -h, --help  Show this help message and exit.
```

## gdrive files
```
usage: gdrive files [-h] [-l | --pretty-print] [--limit LIMIT]

files.description

options:
  -h, --help          Show this help message and exit.
  -l, --long-listing  Use a long listing format.
  --pretty-print      Pretty-print items.
  --limit LIMIT       Limit execution to `LIMIT` number of items.
```

## gdrive folders
```
usage: gdrive folders [-h] [-l | --pretty-print] [--limit LIMIT]

folders.description

options:
  -h, --help          Show this help message and exit.
  -l, --long-listing  Use a long listing format.
  --pretty-print      Pretty-print items.
  --limit LIMIT       Limit execution to `LIMIT` number of items.
```

## gdrive list
```
usage: gdrive list [-h] [-t | -l | --pretty-print] [-f | -d] [-R]
                   [--limit LIMIT]
                   PATH

list.description

positional arguments:
  PATH                File or folder of items to list.

options:
  -h, --help          Show this help message and exit.
  -t, --time          Use a time listing format.
  -l, --long-listing  Use a long listing format.
  --pretty-print      Pretty-print items.
  -f, --files-only    Show files only.
  -d, --folders-only  Show folders only.
  -R, --recursive     Recurse into any sub-folders, recursively.
  --limit LIMIT       Limit execution to `LIMIT` number of items.
```

## gdrive rename
```
usage: gdrive rename [-h] src target

rename.description

positional arguments:
  src         File to rename.
  target      New name.

options:
  -h, --help  Show this help message and exit.
```

## gdrive renamelist
```
usage: gdrive renamelist [-h] listfile

renamelist.description

positional arguments:
  listfile    File with list of renames.

options:
  -h, --help  Show this help message and exit.
```

## gdrive uploaddir
```
usage: gdrive uploaddir [-h] [--add-timestamp] [--convert] [--no-convert]
                        [--target-folder TARGET_FOLDER]
                        [PATH ...]

uploaddir.description

positional arguments:
  PATH                  File to upload.

options:
  -h, --help            Show this help message and exit.
  --add-timestamp       Bake a timestamp into the target name.
  --convert             Convert to google doc.
  --no-convert          Do not convert to google doc.
  --target-folder TARGET_FOLDER
                        Root of destination tree.
```

## gdrive uploadfile
```
usage: gdrive uploadfile [-h] [--add-timestamp] [--convert] [--no-convert]
                         PATH FOLDER [NEWNAME]

uploadfile.description

positional arguments:
  PATH             File to upload.
  FOLDER           Destination folder.
  NEWNAME          New name for target file.

options:
  -h, --help       Show this help message and exit.
  --add-timestamp  Bake a timestamp into the target name.
  --convert        Convert to google doc.
  --no-convert     Do not convert to google doc.
```

## gdrive uploadlist
```
usage: gdrive uploadlist [-h] [--no-themes] [--add-timestamp] [--convert]
                         [--no-convert] [--target-folder TARGET_FOLDER]
                         listfile

uploadlist.description

positional arguments:
  listfile              File with list of uploads.

options:
  -h, --help            Show this help message and exit.
  --no-themes           Remove theme elements; (implies --all-fields).
  --add-timestamp       Bake a timestamp into the target name.
  --convert             Convert to google doc.
  --no-convert          Do not convert to google doc.
  --target-folder TARGET_FOLDER
                        Destination folder.
```

