import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(
    max_workers = multiprocessing.cpu_count() * 2 + 1
)


def test(i, j):
    print(i, ' ', j)
    time.sleep(1)


def main():
    for i in range(10):
        executor.submit(test, i, i+1)


if __name__ == "__main__":
    main()