import fire

from data_collector import Collector


def main(args=None):
    fire.Fire(Collector)


if __name__ == "__main__":
    main()
