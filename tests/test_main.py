import yaml
from pathlib import Path
from unittest.mock import patch

from ye.ye import main


def write_config(path: Path, config: dict):
    path.write_text(yaml.dump(config))


def test_main_with_single_options(tmp_path):
    cfg = {
        "spec": {
            "exec": {"command": "/bin/echo", "workingDir": "/"},
            "args": [
                {"name": "greeting", "options": ["Hello"]},
                {"name": "name", "options": ["World"]},
            ],
        }
    }
    config_path = tmp_path / "cfg.yaml"
    write_config(config_path, cfg)

    with patch("subprocess.run") as run:
        main(str(config_path))
        run.assert_called_once()
        expected_cmd = ["bash", "-c", "/bin/echo Hello World"]
        assert run.call_args.args[0] == expected_cmd
        assert run.call_args.kwargs["cwd"] == "/"


def test_main_with_prompt(tmp_path):
    cfg = {
        "spec": {
            "exec": {"command": "/bin/echo", "workingDir": "/tmp"},
            "args": [
                {"name": "color", "options": ["red", "blue"]},
                {"name": "target", "options": ["sky"]},
            ],
        }
    }
    config_path = tmp_path / "cfg.yaml"
    write_config(config_path, cfg)

    with patch("ye.ye.FzfPrompt") as mock_fzf, patch("subprocess.run") as run:
        instance = mock_fzf.return_value
        instance.prompt.return_value = ["blue"]

        main(str(config_path))

        instance.prompt.assert_called_once_with(["red", "blue"])
        expected_cmd = ["bash", "-c", "/bin/echo blue sky"]
        run.assert_called_once()
        assert run.call_args.args[0] == expected_cmd
        assert run.call_args.kwargs["cwd"] == "/tmp"
