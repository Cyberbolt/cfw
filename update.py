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
    shell("git --git-dir=/etc/cfw/.git --work-tree=/etc/cfw pull https://github.com/Cyberbolt/cfw.git --quiet")
    cmd("systemctl start cfw")
    print("CFW has been updated.")


if __name__ == "__main__":
    main()
