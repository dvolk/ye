# ye

ye (yaml execute) runs cli commands based on a YAML config file.

The selected options are passed to bash for expansion. Options with eg. space characters should be escaped with `\`.

for example:

```yaml
kind: ye-command
metadata:
  name: ls
  description: try ls command for manual testing
spec:
  exec:
    command: /usr/bin/ls
    workingDir: /
  args:
    - name: options
      options:
        - '-a'
        - '-ltrh'
    - name: no_options_dir
    - name: one_option_dir
      options:
        - '/'
    - name: multi_options_dir
      options:
        - '/'
        - '/tmp'
        - '/usr'
    - name: variables
      options:
        - '$HOME'
    - name: spaces
      options:
        - '/tmp/dir\ with\ spaces'
    - name: braces
      options:
        - '/etc/{hosts,crontab}'
```

## Setup & run

```bash
sudo apt update
sudo apt install python3-pip fzf

python3 -m venv env
env/bin/pip install git+https://github.com/dvolk/ye
```

```bash
env/bin/ye test.yaml
```
