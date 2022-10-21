import time

import cfw


def main():
    cfw.run()
    while True:
        time.sleep(60 * 60 * 24 * 365 * 100)


if __name__ == "__main__":
    main()
