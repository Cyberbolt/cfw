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
    # clone cfw
    cmd("git clone https://github.com/Cyberbolt/cfw.git /etc/cfw/")
    # choose linux architecture
    architecture = shell("uname -m").strip()
    if architecture == "x86_64":
        cmd("curl -# -OL https://github.com/Cyberbolt/cfw/releases/download/v1.0.0/py39-Linux-x86_64.tar.gz")
    if architecture == "aarch64":
        cmd("curl -# -OL https://github.com/Cyberbolt/cfw/releases/download/v1.0.0/py39-Linux-aarch64.tar.gz")
    # Unzip the python3.9 version
    cmd("tar -zxvf py39-Linux-x86_64.tar.gz")
    cmd("mv py39 /etc/cfw/py39")
    cmd("rm -rf py39-Linux-x86_64.tar.gz")
    # Install Python dependencies
    cmd("/etc/cfw/py39/bin/python -m pip install -r /etc/cfw/requirements.txt")
    # run with systemd
    cmd("cp /etc/cfw/cfw.service /etc/systemd/system/cfw.service")
    cmd("systemctl daemon-reload")
    cmd("systemctl enable cfw")
    cmd("systemctl start cfw")
    # add environment variable
    cmd("echo alias cfw='/etc/cfw/py39/bin/python /etc/cfw/client.py'>>~/.bashrc")
    cmd("source ~/.bashrc")


if __name__ == "__main__":
    main()