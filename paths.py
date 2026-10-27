"""Repository-local paths for the gravitational imaging teaching materials."""

from pathlib import Path

from tdpy.paths import RepositoryPaths


PATH_ENV_VAR = "GRAVITATIONAL_IMAGING_TEACHING_TEAM_PATH"
DEFAULT_REPOSITORY_PATH = Path(__file__).resolve().parent

_REPOSITORY_PATHS = RepositoryPaths(PATH_ENV_VAR, DEFAULT_REPOSITORY_PATH)
get_repository_path = _REPOSITORY_PATHS.get_repository_path
get_data_path = _REPOSITORY_PATHS.get_data_path
get_visuals_path = _REPOSITORY_PATHS.get_visuals_path
