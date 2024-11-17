import sys

import pytest

from gdrive.cli import GoogleDriveCLI


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
