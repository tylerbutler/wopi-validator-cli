# coding=utf-8
import os

try:
    from _version import version
except ImportError:
    from propane_distribution import update_version_py

    update_version_py(version_path=os.path.dirname(__file__))
    try:
        # noinspection PyUnresolvedReferences
        # noinspection PyProtectedMember
        from wopi_validator._version import version
    except ImportError:
        raise

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'
