# Credits: https://github.com/ultmaster/video-thumbnail/blob/master/thumbnail.py

import os
import random
import re
import string
import subprocess
import traceback

import av
from PIL import Image, ImageDraw

# Tune these settings...
IMAGE_WIDTH = 1536
IMAGE_HEIGHT = IMAGE_WIDTH // 2
IMAGE_SET = 10
BACKGROUND_COLOR = "#fff"


def get_time_display(time):
    return "%02d:%02d:%02d" % (time // 3600, time % 3600 // 60, time % 60)


def get_random_filename(ext):
    return ''.join([random.choice(string.ascii_lowercase) for _ in range(20)]) + ext


def create_thumbnail(filename):
    print('Processing:', filename)

    jpg_name = '%s.jpg' % filename
    if os.path.exists(jpg_name):
        print('Thumbnail assumed exists!')
        return

    _, ext = os.path.splitext(filename)
    random_filename = get_random_filename(ext)
    random_filename_2 = get_random_filename(ext)
    print('Rename as %s to avoid decode error...' % random_filename)
    try:
        os.rename(filename, random_filename)
        try:
            container = av.open(random_filename)
        except UnicodeDecodeError:
            print('Metadata decode error. Try removing all the metadata...')
            subprocess.run(["ffmpeg", "-i", random_filename, "-map_metadata", "-1", "-c:v", "copy", "-c:a", "copy",
                            random_filename_2], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            container = av.open(random_filename_2)

        metadata = [
            "File name: %s" % filename,
            "Size: %d bytes (%.2f MB)" % (container.size, container.size / 1048576),
            "Duration: %s" % get_time_display(container.duration // 1000000),
        ]

        start = min(container.duration // (IMAGE_SET), 5 * 1000000)
        end = container.duration - start
        time_marks = []
        for i in range(IMAGE_SET):
            time_marks.append(start + (end - start) // (IMAGE_SET - 1) * i)

        images = []
        for idx, mark in enumerate(time_marks):
            container.seek(mark)
            for frame in container.decode(video=0):
                images.append(frame.to_image())
                break                

        img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), BACKGROUND_COLOR)
        draw = ImageDraw.Draw(img)
        selected_img = random.sample(images, 1)[0]
        selected_img = selected_img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), resample=Image.BILINEAR)
        img.paste(selected_img, box = (0,0))
        
        img.save(jpg_name)
        print('OK!')
    except Exception as e:
        traceback.print_exc()
    finally:
        os.rename(random_filename, filename)
        if os.path.exists(random_filename_2):
            os.remove(random_filename_2)


if __name__ == "__main__":
    p = input("Input the path you want to process: ")
    p = os.path.abspath(p)

    for root, dirs, files in os.walk(p):
        print('Switch to root %s...' % root)
        os.chdir(root)
        for file in files:
            ext_regex = r"\.(webm)$"
            if re.search(ext_regex, file, re.IGNORECASE):
                create_thumbnail(file)
