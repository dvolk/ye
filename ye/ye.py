#!/usr/bin/env python3

import yaml
import subprocess

from pyfzf.pyfzf import FzfPrompt
import argh


def main(cmd_config):
    # Load the YAML configuration
    with open(cmd_config, "r") as f:
        config = yaml.safe_load(f)

    spec = config["spec"]
    exec_cfg = spec["exec"]
    args = spec.get("args", [])

    interpreter = exec_cfg.get("interpreter", "")
    command = exec_cfg.get("command", "")
    working_dir = exec_cfg.get("workingDir", ".")

    cmd_args = []

    fzf = FzfPrompt()

    for arg in args:
        name = arg.get("name", "")
        argument = arg.get("argument", "")
        options = arg.get("options", [])

        if len(options) == 1:
            choice = options[0]
        elif options:
            # Use pyfzf to present options
            selected = fzf.prompt(options)
            if selected:
                choice = selected[0]
            else:
                print(f"No option selected for {name}")
                return
        else:
            # Prompt the user for input
            choice = input(f"Enter value for {name}: ")

        if argument:
            cmd_args.append(argument)
        cmd_args.append(choice)

    # Build the command
    if interpreter:
        cmd = [interpreter, command] + cmd_args
    else:
        cmd = [command] + cmd_args

    print(cmd)
    cmd = ["bash", "-c", " ".join(cmd)]

    print(f"Running command: {cmd}")
    # Run the command
    subprocess.run(cmd, cwd=working_dir, check=True)


if __name__ == "__main__":
    argh.dispatch_command(main)
