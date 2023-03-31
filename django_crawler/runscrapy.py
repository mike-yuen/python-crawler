import sys
from scrapy import cmdline


def main():
    arguments = sys.argv[1:]
    if not arguments:
        print("Spider name is required.\nExample: python runscrapy.py vnexpress")
        return
    cmdline.execute(f"scrapy crawl {arguments[0]}".split())


if __name__ == "__main__":
    main()
