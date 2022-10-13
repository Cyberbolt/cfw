import pprint
import subprocess


def main():
    r = subprocess.run(
        "ss -Hntu | awk '{print $6}' | sort | uniq -c | sort -nr", 
        shell=True,
        capture_output=True
    )
    text = r.stdout.decode()
    
    new = [line.strip().rsplit(' ', 1) for line in text.split('\n')[:-1]]
    pprint.pprint(new)


if __name__ == '__main__':
    main()