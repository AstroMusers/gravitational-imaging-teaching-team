import os
from pathlib import Path
from unittest.mock import patch

from paths import (
    PATH_ENV_VAR,
    get_data_path,
    get_repository_path,
    get_visuals_path,
)


def test_configured_repository_paths(tmp_path):
    with patch.dict(os.environ, {PATH_ENV_VAR: str(tmp_path)}):
        assert get_repository_path() == tmp_path
        assert get_data_path() == tmp_path / "data"
        assert get_visuals_path() == tmp_path / "visuals"


def test_repository_path_defaults_to_checkout():
    with patch.dict(os.environ, {}, clear=True):
        root = Path(__file__).resolve().parent
        assert get_repository_path() == root
        assert os.environ[PATH_ENV_VAR] == str(root)