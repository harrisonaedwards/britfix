"""Shared pytest fixtures for the britfix suite."""

import pytest


@pytest.fixture(scope='session')
def _empty_user_config_dir(tmp_path_factory):
    """A guaranteed-empty stand-in for the user's config home."""
    return tmp_path_factory.mktemp('isolated_user_config')


@pytest.fixture(autouse=True)
def isolate_user_config(monkeypatch, _empty_user_config_dir):
    """Point user-level ignore discovery at an empty directory for every test.

    ``discover_ignore_words`` merges the user's own ignore file
    (``~/.config/britfix/ignore``, or ``%APPDATA%/britfix/ignore``) regardless
    of the project's .git boundary, so without this the developer's personal
    ignores leak into the suite. That makes results depend on whose machine the
    tests run on: green in CI, red locally for anyone who ignores a word a test
    asserts on.

    Tests that need a user config still set the env var themselves — theirs is
    applied inside the test body, after this fixture, and wins.
    """
    monkeypatch.setenv('XDG_CONFIG_HOME', str(_empty_user_config_dir))
    monkeypatch.setenv('APPDATA', str(_empty_user_config_dir))
