import headline_updater
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

  publishers = ["cbc", "star", "post", "global", "globe", "macleans", "herald"]
  # publishers = ["cbc"]

  for p in publishers:
    if not os.path.exists(f"{tmp}/{p}"):
      os.mkdir(f"{tmp}/{p}")
      os.mkdir(f"{tmp}/{p}/articles")    
    os.chown(f"{tmp}/{p}", os.getuid(), -1)
    os.chown(f"{tmp}/{p}/articles", os.getuid(), -1)

  print ("Updating headlines")
  headline_updater.update(publishers, tmp, archivedir, False)

  shutil.rmtree(tmp)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])