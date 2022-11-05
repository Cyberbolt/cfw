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
    cmd("git clone https://github.com/Cyberbolt/cfw.git /etc/cfw")
    # Install Miniforge 3
    cmd('curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"')
    cmd("bash Miniforge3-$(uname)-$(uname -m).sh -b")
    cmd("/root/miniforge3/bin/conda create -n py39 python=3.9.12 -y")
    cmd("mv /root/miniforge3/envs/py39 /etc/cfw/py39")
    # Install Python dependencies
    cmd("/etc/cfw/py39/bin/python -m pip install -r requirements.txt")
    # run with systemd
    cmd("cp cfw.service /etc/systemd/system/cfw.service")
    cmd("systemctl daemon-reload")
    cmd("systemctl enable cfw")
    cmd("systemctl start cfw")
    # add environment variable
    cmd('echo alias cfw="/etc/cfw/py39/bin/python /etc/cfw/client.py">>~/.bashrc')


if __name__ == "__main__":
    main()