#!/usr/bin/env python

import sys
import os
import argparse
import glob
import tempfile
import shutil
import subprocess
import uuid
import csv
from PIL import Image

def load_tsv(tsv_path):
    result = []
    with open(tsv_path, 'r') as tsvfile:
        tsv = csv.reader(tsvfile, delimiter='\t')
        for row in tsv:
            result.append(row)
    return result

def find_images(dirs_list):
    images = list()
    for root, dirs, files in os.walk(dirs_list):
        for file in files:
            if file.endswith(".jpg"):
                image_path = os.sep.join([root, file])
                im=Image.open(image_path)
                image_size = im.size
                bboxes_path = ".".join(image_path.split('.')[:-1] + ["bboxes", "tsv"]) 
                labels_path = ".".join(image_path.split('.')[:-1] + ["bboxes", "labels", "tsv"]) 
                if os.path.isfile(bboxes_path) and os.path.isfile(labels_path):
                    bboxes = load_tsv(bboxes_path)
                    labels = load_tsv(labels_path)
                    images.append({ "image_path":image_path, "image_size": image_size, "bboxes": bboxes, "labels": labels })
                else:
                    images.append({ "image_path":image_path, "image_size": image_size, "bboxes":[ [0,0,image_size[0],image_size[1]] ], "labels":[ list(["bg"]) ]  })
    return images

parser = argparse.ArgumentParser(description= 'Converts a VoTT export in CNTK Fast RCNN format to CSV')
parser.add_argument("--input_dir", dest='input_dir', required=True)
parser.add_argument("--output", dest="output", type=str, default="-")
args = parser.parse_args()

images = find_images(args.input_dir)
output = sys.stdout if args.output == "-" else open(args.output, "w")
with output as csvfile:
    csvwriter = csv.writer(csvfile)
    for image in images:
        for index, bbox in enumerate(image["bboxes"]):
          csvwriter.writerow([ image["image_path"] ] + bbox + image["labels"][index])

