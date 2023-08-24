import subprocess
import shlex


def shell(cmd: str) -> str:
    """
    Execute a shell statement and return the output.
    """
    subprocess.run(
        shlex.split(cmd),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def main():
    cmd = "git --git-dir=/etc/cfw/.git --work-tree=/etc/cfw pull https://github.com/Cyberbolt/cfw.git --quiet"
    shell(cmd)
    print("CFW has been updated.")


if __name__ == "__main__":
    main()
