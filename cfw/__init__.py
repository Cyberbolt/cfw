import subprocess


def get_ip() -> list:
    """
        Sort by ip connections in descending order and convert to a list.
    """
    r = subprocess.run(
        "ss -Hntu | awk '{print $6}' | sort | uniq -c | sort -nr", 
        shell=True,
        capture_output=True
    )
    text = r.stdout.decode()
    form = [line.strip().rsplit(" ", 1) for line in text.split("\n")[:-1]]
    return form
