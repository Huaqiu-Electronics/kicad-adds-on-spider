
import sys
from kicad_adds_on_spider.crawler.worker import Worker


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Usage: python main.py <save-dir>")
        sys.exit(1)  # Exit the script if arguments are missing

    save_dir = sys.argv[1]
    crawler = Worker(save_dir)
    crawler.run()

