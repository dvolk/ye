import yaml
import subprocess
import pathlib
from pyfzf.pyfzf import FzfPrompt
import argh


def main(cmd_config):
    # Load the YAML configuration
    with open(cmd_config, "r") as f:
        config = yaml.safe_load(f)

    spec = config["spec"]
    command_spec = spec["command"]

    interpreter = command_spec.get("interpreter", "")
    command = command_spec.get("command", "")
    working_dir = command_spec.get("workingDir", ".")
    args = command_spec.get("args", [])

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
            cmd_args.extend([argument, choice])
        else:
            cmd_args.append(choice)

    # Build the command
    if interpreter:
        cmd = [interpreter, command] + cmd_args
    else:
        cmd = [command] + cmd_args

    print("Running command: {}".format(" ".join(cmd)))
    # Run the command
    subprocess.run(cmd, cwd=working_dir)


if __name__ == "__main__":
    argh.dispatch_command(main)
