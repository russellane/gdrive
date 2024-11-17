"""Google API base class."""

import xdg
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore[import-untyped]
from googleapiclient.discovery import Resource, build  # type: ignore[import-untyped]
from loguru import logger

# import logging
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# import httplib2
# httplib2.debuglevel = 4

__all__ = ["connect_to_google"]


def connect_to_google(scope: str, version: str) -> Resource:
    """Connect to Google service identified by `scope`.

    Args:
        scope:          (valid examples):
                        "https://www.googleapis.com/auth/gmail"
                        "https://www.googleapis.com/auth/gmail.readonly"
                        "gmail"
                        "gmail.readonly"
                        "drive.metadata.readonly"
                        "photoslibrary.readonly"

        version:        "v1", "v3", etc.

    Files:
        credentials:    XDG_CONFIG_HOME / pygoogle / credentials.json

        token:          XDG_CACHE_HOME / pygoogle / {scope}-token.json
    """

    #
    _scope_prefix = "https://www.googleapis.com/auth/"
    if scope.startswith(_scope_prefix):
        scope = scope[len(_scope_prefix) :]  # strip prefix
    scopes = [_scope_prefix + scope]  # fully qualified

    #
    _credentials_dir = xdg.xdg_config_home() / "pygoogle"
    _credentials_dir.mkdir(parents=True, exist_ok=True)
    credentials_file = _credentials_dir / "credentials.json"

    #
    _token_dir = xdg.xdg_cache_home() / "pygoogle"
    _token_dir.mkdir(parents=True, exist_ok=True)
    token_file = _token_dir / f"{scope}-token.json"

    #
    credentials = None
    if token_file.exists():
        credentials = Credentials.from_authorized_user_file(token_file, scopes)  # type: ignore[no-untyped-call]

    #
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())  # type: ignore[no-untyped-call]
        else:
            logger.debug("Sign in")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            credentials = flow.run_local_server(port=0)
        #
        with open(token_file, "w", encoding="utf-8") as token:
            token.write(credentials.to_json())

    #
    service_name = scope.split(".")[0]
    service_version = version
    logger.debug(f"Connecting to {service_name!r} {service_version!r}")

    service = build(
        service_name,
        service_version,
        credentials=credentials,
        cache_discovery=False,
    )

    return service
