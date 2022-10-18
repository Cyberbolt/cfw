import time

import cfw
from cfw.extensions.iptables import cfw_init


def main():
    # while True:
    #     time.sleep(60 * 60 * 24 * 365 * 100)
    print("====", cfw_init())


if __name__ == "__main__":
    main()
