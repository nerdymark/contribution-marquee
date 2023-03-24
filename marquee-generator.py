"""
Contribution Marquee
Populate your GitHub profile with a contribution graph with your preferred message.
"""

from __future__ import print_function
import datetime
import os
import random
import sys
import time
import string
import json
import argparse
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np

# Parse args, get message, data file
parser = argparse.ArgumentParser(description='Contribution Marquee')
parser.add_argument('--message', dest='message', type=str, default='nerdymark')
parser.add_argument('--data-file', dest='data_file', type=str, default='marquee-data.json')
opt = parser.parse_args()

# Set your message
message = opt.message

# Set your data file
data_file = opt.data_file

data = []

all_dates = set()

# When is next Sunday?
start_date = (datetime.datetime.now() + datetime.timedelta(days=(6 - datetime.datetime.now().weekday()))).date()

def char_to_pixels(text, path='arialbd.ttf', fontsize=14):
    """
    Based on https://stackoverflow.com/a/27753869/190597 (jsheperd)
    """
    font = ImageFont.truetype(path, fontsize) 
    w, h = font.getsize(text)  
    h *= 2
    image = Image.new('L', (w, h), 1)  
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font) 
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    arr = arr[(arr != 0).any(axis=1)]
    return arr

def display(arr):
    result = np.where(arr, '#', ' ')
    print('\n'.join([''.join(row) for row in result]))

for c in message:
    fontfile = '7.ttf'  # a simple pixel font, find your own.
    fontsize = 14

    arr = char_to_pixels(
        c, 
        path=fontfile, 
        fontsize=fontsize)
    
    display(arr)
    print()

    sched_dates = []
    for val in arr:
        for idx, pixel in enumerate(val):

            if idx == 0:
                sched_date = start_date
            else:
                sched_date = start_date + datetime.timedelta(weeks=idx)
            if pixel == 1:
                plain_date = sched_date.isoformat()
                # print('index of pixel is {}, sched_date is {}'.format(idx, sched_date))
                sched_data = {
                    'date': plain_date,
                    'index': idx
                }
                sched_dates.append(sched_data)
            # start_date = start_date + datetime.timedelta(weeks=1)
            all_dates.add(sched_date)
        start_date = start_date + datetime.timedelta(days=1)
        # start_date = start_date + datetime.timedelta(days=1)
        # print(sched_dates)
        # # time.sleep(999)
    
    # Sort sched_dates to be readable
    sched_dates = json.loads(json.dumps(sched_dates, sort_keys='date'))
    letter_data = {c: sched_dates}
    data.append(letter_data)

    # Find the next Sunday after the last sched_date
    start_date = (sched_date + datetime.timedelta(days=(6 - sched_date.weekday() - 14)))

    # Space between letters
    # start_date = start_date + datetime.timedelta(days=6)

# print(json.dumps(data, indent=4))

# Get the first and last dates from the data
first_date = min(all_dates)
last_date = max(all_dates)

# Get the number of weeks between the first and last dates
weeks = (last_date - first_date).days / 7
print('The duration of the marquee is {} weeks'.format(weeks))
if weeks > 52:
    print('The marquee is too long, please shorten your message')
    sys.exit(1)

# Save the data to the json
with open(data_file, 'w') as outfile:
    outfile.write(json.dumps(data, indent=4))
