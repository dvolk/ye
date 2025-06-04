# ye

ye (yaml execute) runs cli commands based on a YAML config file.

for example:

```yaml
kind: ye-command
metadata:
  name: rsync
  description: run rsync for backups
spec:
  command:
    command: /usr/bin/rsync
    workingDir: /home/dvolk/
    args:
      - name: options
        options:
          - '-aXxv'
          - '-aXxv --delete'
      - name: source
      - name: destination
        options:
          - '/tmp/backups'
```

## Setup & run

Install the system dependency for fuzzy finding:

```bash
sudo apt-get install -y fzf
```

Set up a virtual environment and install Python packages from
`requirements.txt`:

```bash
python3 -m venv env
./env/bin/pip install -r requirements.txt
chmod a+x ye.py
source env/bin/activate
```

```bash
./ye.py <yaml_conf_path>
```
