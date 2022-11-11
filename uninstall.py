import sys
import subprocess


def cmd(cmd: str):
    try:
        subprocess.run(
            cmd, 
            shell=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        sys.exit(1)


def shell(cmd: str) -> str:
    """
        Execute a shell statement and return the output.
    """
    r = subprocess.run(
        cmd, 
        shell=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return r.stdout.decode()


def main():
    # Remove cfw
    cmd("rm -rf /etc/cfw/")
    # Delete environment variable
    with open("/root/.bashrc", "r") as f:
        text = f.read()
    lines = text.splitlines()
    text_new = ""
    for line in lines:
        if "alias cfw='/etc/cfw/py39/bin/python /etc/cfw/client.py'" not in line:
            text_new += line + "\n"
    with open("/root/.bashrc", "w") as f:
        f.write(text_new)


if __name__ == "__main__":
    main()
