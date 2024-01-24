"""
Generate CSV metadata file for use with CollectionBuilder.


The general skeleton of this script can be used for different
projects.
"""

from csv import DictReader, DictWriter
from collections import namedtuple
from pathlib import Path
import urllib.parse
import os
from functools import partial



def identifier_from_image_name(bucket, image_name):
    return urllib.parse.quote_plus(f"{bucket}/{os.path.splitext(image_name)[0].lower()}")

def iiif_uri(scheme, server, prefix, identifier, region, size, rotation, quality, format):
    return f"{scheme}://{server}/{prefix}/{identifier}/{region}/{size}/{rotation}/{quality}.{format}"


def object_location(image_name, bucket, object_uri):
    return object_uri(identifier=identifier_from_image_name(bucket, image_name),
                      size="full")

def image_small(image_name, bucket, object_uri):
    return object_uri(identifier=identifier_from_image_name(bucket, image_name),
                      size="800,")

def image_thumb(image_name, bucket, object_uri):
    return object_uri(identifier=identifier_from_image_name(bucket, image_name),
                      size="400,")



source_data = "/Users/wulfmanc/princeton/projects/davies_project/data.csv"
data_dir = "/tmp"

def convert_data(src_path, dest_path, server, bucket):
    object_uri = partial(iiif_uri,
                         scheme="https",
                         server="puliiif-staging.princeton.edu",
                         prefix="iiif/2",
                         region="full",
                         rotation=0,
                         quality="default",
                         format="jpg")

    data = []
    with open(src_path) as f:
        reader = DictReader(f)
        header = reader.fieldnames.copy()
        header.remove('card_image')
        header.append('objectid')
        header.append('subject')
        header.append('title')
        header.append('location')
        header.append('date')
        header.append('object_location')
        header.append('image_small')
        header.append('image_thumb')
        header.append('format')
        header.append('display_template')
        for counter, row in enumerate(reader):
            image_filename = Path(row['card_image']).stem + ".jpg"
            del row['card_image']
            row['object_location'] = object_location(image_filename, bucket,  object_uri)
            row['image_small'] = image_small(image_filename, bucket, object_uri)
            row['image_thumb'] = image_thumb(image_filename, bucket, object_uri)
            row['objectid'] = f"rec{counter}"
            row['display_template'] = 'item'
            row['format'] = 'image/jpg'
            row['title'] = row['Name']
            row['subject'] = row['Type']
            row['location'] = f"{row['Locality']}, {row['State']}"
            row['date'] = row['Found_Date']
            data.append(row)


    with open(f"{data_dir}/alb1876.csv", mode='w', newline='') as csvfile:
        writer = DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
