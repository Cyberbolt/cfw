import argparse


def get_input() -> dict:
    '''
        Get input from the terminal
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=str, default = None)
    parser.add_argument('-username', type=str, default = None)
    parser.add_argument('-password', type=str, default = None)
    args = parser.parse_args()
    data = {}
    data['port'] = args.port
    data['username'] = args.username
    data['password'] = args.password
    return data


def main():
    pass


if __name__ == "__main__":
    main()
