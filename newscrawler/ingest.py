import crawler
import os
import sys
import shutil
import json

sys.path.append("newscrawler/spiders")

def main(archivedir, tmp="tmp"):

  print(f"Running ingest with archivedir={archivedir}")
  if not os.path.exists(tmp):
    print ("Creating tmp directory")
    os.mkdir(tmp)
  if not os.path.exists(archivedir):
    print ("Creating archive directory")
    os.mkdir(archivedir)

  publishers = ["cbc", "star", "post", "global", "globe", "macleans", "herald"]
  # publishers = ["cbc"]

  for p in publishers:
    if not os.path.exists(f"{tmp}/{p}"):
      os.mkdir(f"{tmp}/{p}")
      os.mkdir(f"{tmp}/{p}/articles")
    os.chown(f"{tmp}/{p}", os.getuid(), -1)
    os.chown(f"{tmp}/{p}/articles", os.getuid(), -1)
    if not os.path.exists(f"{archivedir}/{p}"):
      os.mkdir(f"{archivedir}/{p}")
      os.mkdir(f"{archivedir}/{p}/articles")
    os.chown(f"{archivedir}/{p}", os.getuid(), -1)
    os.chown(f"{archivedir}/{p}/articles", os.getuid(), -1)

  print ("Crawling")
  crawler.crawl(publishers, tmp, archivedir, True)

  shutil.rmtree(tmp)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])