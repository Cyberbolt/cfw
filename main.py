import os
import subprocess


def main():
    r = subprocess.run(
        "ss -Hntu | awk '{print $6}' | sort | uniq -c | sort -nr", 
        shell=True,
        capture_output=True
    )
    text = r.stdout.decode()
    print(text)
    


if __name__ == '__main__':
    main()