#!/usr/bin/env python

# Library
from apps.sit_api.api import get_uwb_device_settings
from apps.sit_api.auth import Authenticator


def main():
    auth = Authenticator()
    auth.login()
    get_uwb_device_settings(auth=auth)


if __name__ == "__main__":
    main()
