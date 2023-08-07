from csv import DictReader, DictWriter
from collections import namedtuple
from pathlib import Path

source_data = "/Users/wulfmanc/princeton/projects/davies_project/data.csv"
data_dir = '/Users/wulfmanc/repos/github/pulibrary/davies-cb/_data'

data = []
with open(source_data) as f:
    reader = DictReader(f)
    header = reader.fieldnames.copy()
    header.remove('card_image')
    header.append('objectid')
    header.append('subject')
    header.append('title')
    header.append('object_location')
    header.append('image_small')
    header.append('image_thumb')
    header.append('format')
    header.append('display_template')
    for counter, row in enumerate(reader):
        old_image_path = Path(row['card_image'])
        image_filename = old_image_path.stem + ".jpg"
        del row['card_image']
        row['object_location'] = f"/objects/{image_filename}"
        row['image_small'] = f"/objects/small/{image_filename}"
        row['image_thumb'] = f"/objects/thumbs/{image_filename}"
        row['objectid'] = f"rec{counter}"
        row['display_template'] = 'item'
        row['format'] = 'image/jpg'
        row['title'] = row['Name']
        row['subject'] = row['Type']
        data.append(row)

with open(f"{data_dir}/alb1876.csv", mode='w', newline='') as csvfile:
    writer = DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

with open(f"{data_dir}/config-browse.csv", mode='w', newline='') as configfile:
    writer = DictWriter(configfile, fieldnames=['field', 'display_name', 'btn', 'hidden', 'sort_name'])
    writer.writeheader()
    writer.writerow({'field': 'subject', 'display_name': 'Subject', 'btn': 'true', 'sort_name': 'Subject'})
    writer.writerow({'field': 'location', 'display_name': 'State', 'btn': 'true', 'sort_name': 'State'})
    writer.writerow({'field': 'title', 'display_name': 'Name', 'sort_name': 'Name'})
