import requests
from csv import DictReader, DictWriter

data = []
with open("/Users/wulfmanc/princeton/projects/davies_project/data.csv") as f:
    reader = DictReader(f)
    for row in reader:
        image_uri = row['card_image']
        filename = image_uri.split('/')[-1]
        r = requests.get(image_uri, allow_redirects=True)
        open(f"/Users/wulfmanc/repos/github/pulibrary/davies-cb/_data/images/{filename}", "wb").write(r.content)

