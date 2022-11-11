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
    if architecture != "aarch64" and architecture != "x86_64":
        print("This CPU architecture is not supported, only x86_64 and arm64 are supported.")
        sys.exit(1)
    cmd("curl -# -OL https://github.com/Cyberbolt/cfw/releases/download/v1.0.0/py39-Linux-{}.tar.gz".format(architecture))
    # Unzip the python3.9 version
    cmd("tar -zxvf py39-Linux-{}.tar.gz".format(architecture))
    cmd("mv py39 /etc/cfw/py39")
    cmd("rm -rf py39-Linux-{}.tar.gz".format(architecture))
    # Install Python dependencies
    cmd("/etc/cfw/py39/bin/python -m pip install -r /etc/cfw/requirements.txt")
    # run with systemd
    cmd("cp /etc/cfw/cfw.service /etc/systemd/system/cfw.service")
    cmd("systemctl daemon-reload")
    cmd("systemctl enable cfw")
    cmd("systemctl start cfw")
    # add environment variable
    cmd("""echo "alias cfw='/etc/cfw/py39/bin/python /etc/cfw/client.py'">>~/.bashrc""")
    print("""
CFW installation is complete, please enter the following command to activate 'cfw'.
            
    source ~/.bashrc
""")


if __name__ == "__main__":
    main()
