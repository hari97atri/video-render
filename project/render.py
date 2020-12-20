import os
import glob
import imageio
import time
import subprocess

from PIL import Image

import settings

# render using ffmpeg
# command = 'ffmpeg -r 1/5 -i img%03d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p out.mp4'


def crop(input_file):
    im = Image.open(input_file)
    imgwidth, imgheight = im.size
    height = imgheight // 2
    width = imgwidth // 2
    cropped_images = []
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            cropped_images.append(im.crop(box))
    return cropped_images


# start process here
init_time = time.time()
images0, images1, images2, images3 = [], [], [], []

img_base_name = settings.IMAGES_FOLDER + 'IMG_20181101_160822_BURST'
img_format = settings.IMAGE_FORMAT

for img_index in range(1, 100):
    filename = img_base_name + str(img_index) + img_format
    cropped_imgs = crop(filename)
    images0.append(cropped_imgs[0])
    images1.append(cropped_imgs[1])
    images2.append(cropped_imgs[2])
    images3.append(cropped_imgs[3])


def render_video(image_set, index):
    imageio.mimsave('./intermediaries/%s' % 'movie' + str(index) + settings.OUTPUT_FORMAT, image_set)


render_video(images0, 0)
render_video(images1, 1)
render_video(images2, 2)
render_video(images3, 3)


def execute_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output, error


def horizontal_stack(v1, v2, o):
    command = 'ffmpeg -i %s -i %s -filter_complex hstack %s' % (v1 + settings.OUTPUT_FORMAT, v2 + settings.OUTPUT_FORMAT, o + settings.OUTPUT_FORMAT)
    return execute_command(command)


def vertical_stack(v1, v2, o):
    command = 'ffmpeg -i %s -i %s -filter_complex vstack=inputs=2 %s' % (v1 + settings.OUTPUT_FORMAT, v2 + settings.OUTPUT_FORMAT, o + settings.OUTPUT_FORMAT)
    return execute_command(command)


def remove_intermediaries():
    files = glob.glob('./intermediaries/*')
    for f in files:
        os.remove(f)


horizontal_stack('./intermediaries/movie0', './intermediaries/movie1', './intermediaries/output_u')
horizontal_stack('./intermediaries/movie2', './intermediaries/movie3', './intermediaries/output_b')
vertical_stack('./intermediaries/output_u', './intermediaries/output_b', './final')

remove_intermediaries()

execute_command('rm -rf ')
fin_time = time.time()
tot_time = fin_time - init_time
print(tot_time)
