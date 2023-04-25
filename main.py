import os
import logging

from lib.pipeline import Pipeline
from lib.stages import get_stages


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    Pipeline(os.path.join('sample', 'config.yml'), get_stages()).execute()

if __name__ == "__main__":
    main()
