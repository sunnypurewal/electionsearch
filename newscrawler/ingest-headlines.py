import headline_updater
import os
import sys
import datetime
import shutil
import json

sys.path.append("newscrawler/spiders")

def main(archivedir, tmp="tmp"):

  print(f"Running ingest with archivedir={archivedir}")
  if not os.path.exists(tmp):
    print ("Creating tmp directory")
    os.mkdir(tmp)

  publishers = ["cbc", "star", "globe", "post", "global", "macleans", "herald"]

  for p in publishers:
    if not os.path.exists(f"{tmp}/{p}"):
      os.mkdir(f"{tmp}/{p}")
      os.mkdir(f"{tmp}/{p}/articles")

  print ("Updating headlines")
  headline_updater.update(publishers, tmp, False)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])