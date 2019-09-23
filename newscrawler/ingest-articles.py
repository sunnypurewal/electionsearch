import article_updater
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
  
  if not os.path.exists(archivedir):
    print (f"Creating archive path")
    os.mkdir(archivedir)

  publishers = ["cbc", "star", "globe", "post", "global", "macleans", "herald"]

  for p in publishers:
    if not os.path.exists(f"{archivedir}/{p}"):
      os.mkdir(f"{archivedir}/{p}")
      os.mkdir(f"{archivedir}/{p}/articles")
    if not os.path.exists(f"{tmp}/{p}"):
      os.mkdir(f"{tmp}/{p}")
      os.mkdir(f"{tmp}/{p}/articles")

  print ("Updating articles")
  article_updater.update(publishers, archivedir, tmp, False)

  for p in publishers:
    with open(f"{archivedir}/{p}/headlines.jsonc", "r") as f:
      headlines = []
      fstring = f.read()
      if len(fstring) == 0:
        print("No existing headlines, writing out all new headlines")
        with open(f"{tmp}/{p}/headlines.jsonc", "r") as f3:
          f3string = f3.read()
          if len(f3string) > 0:
            headlines.extend(json.loads(f3string))
      else:
        headlines.extend(json.loads(fstring))
        print(f"{len(headlines)} existing headlines. Appending.")
        with open(f"{tmp}/{p}/headlines.jsonc", "r") as f3:
          f3string = f3.read()
          if len(f3string) > 0:
            newheadlines = []
            newheadlines.extend(json.loads(f3string))
            for newheadline in newheadlines:
              id = newheadline["id"]
              if os.path.exists(f"{tmp}/{p}/articles/{id}.txt"):
                print(id, "exists")
                headlines.append(newheadline)
                shutil.move(f"{tmp}/{p}/articles/{id}.txt", f"{archivedir}/{p}/articles/{id}.txt")
    print(f"Writing out {len(headlines)} updated headlines")
    with open(f"{archivedir}/{p}/headlines.jsonc", "w") as f:
      json.dump(headlines, f)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])