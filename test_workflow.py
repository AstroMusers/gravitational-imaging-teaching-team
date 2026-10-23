import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
import yaml


ROOT = Path(__file__).resolve().parent


@pytest.fixture
def workflow():
    path = ROOT / '.github/workflows/ci_validation.yml'
    print(f'Reading from {path}...')
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def execution_code(workflow):
    step = next(step for step in workflow['jobs']['build']['steps'] if step.get('name') == 'Executing changed notebooks')
    source = step['run']
    assert '${{' not in source
    assert step['env']['CHANGED_NOTEBOOKS'] == '${{ steps.changed-files.outputs.all_changed_files }}'
    return compile(source.split("python - <<'PY'\n", 1)[1].rsplit('\nPY', 1)[0], 'ci_validation.yml', 'exec')


@pytest.mark.parametrize('notebooks', [
    [], ['ordinary.ipynb'],
    ['lesson one.ipynb', "quote's lesson.ipynb", 'shell$(echo marker).ipynb', '-option.ipynb', 'line\nbreak.ipynb', 'caf\u00e9.ipynb'],
])
def test_changed_notebooks_are_passed_as_literal_arguments(workflow, monkeypatch, notebooks):
    run = Mock()
    monkeypatch.setenv('CHANGED_NOTEBOOKS', json.dumps(notebooks))
    monkeypatch.setattr(subprocess, 'run', run)

    exec(execution_code(workflow), {'__name__': '__main__'})

    assert run.call_count == len(notebooks)
    for call, notebook in zip(run.call_args_list, notebooks):
        assert call.args[0] == [sys.executable, '-m', 'nbconvert', '--template', 'classic', '--to', 'html', '--execute', os.path.join('.', notebook)]
        assert call.kwargs == {'check': True}


@pytest.mark.parametrize('payload', ['"ordinary.ipynb"', '{"path": "ordinary.ipynb"}', '["ordinary.ipynb", 42]'])
def test_invalid_notebook_output_fails_before_execution(workflow, monkeypatch, payload):
    run = Mock()
    monkeypatch.setenv('CHANGED_NOTEBOOKS', payload)
    monkeypatch.setattr(subprocess, 'run', run)

    with pytest.raises(ValueError, match='JSON array'):
        exec(execution_code(workflow), {'__name__': '__main__'})

    run.assert_not_called()


def test_notebook_failures_propagate(workflow, monkeypatch):
    original = subprocess.CalledProcessError(1, ['synthetic nbconvert'])
    run = Mock(side_effect=original)
    monkeypatch.setenv('CHANGED_NOTEBOOKS', '["first.ipynb", "second.ipynb"]')
    monkeypatch.setattr(subprocess, 'run', run)

    with pytest.raises(subprocess.CalledProcessError) as caught:
        exec(execution_code(workflow), {'__name__': '__main__'})

    assert caught.value is original
    run.assert_called_once()


def test_changed_file_output_and_permissions_match_safe_data_transport(workflow):
    changed = next(step for step in workflow['jobs']['build']['steps'] if step.get('id') == 'changed-files')
    assert changed['with']['json'] is True
    assert changed['with']['escape_json'] is False
    assert changed['with']['safe_output'] is False
    assert changed['with']['quotepath'] is False
    assert workflow['permissions'] == {'contents': 'read', 'pull-requests': 'read'}
