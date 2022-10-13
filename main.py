import pprint

from cfw import get_ip


def main():
    form = get_ip()
    pprint.pprint(form)


if __name__ == "__main__":
    main()
