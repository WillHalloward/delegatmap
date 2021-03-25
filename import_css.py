import re
import time

from PIL import Image, ImageDraw, ImageFont

SCREEN_SIZE_X = 2560
SCREEN_SIZE_Y = 1440

file = open('input.css', 'r').read()
list_file = file.split('\n')
divided_list = []
for lines in list_file:
    css_id = re.search("#vt(\d{1,3})", lines)
    left = re.search("left.*?:.*?(\d{1,4}).*?", lines)
    top = re.search("[^-]top.*?:.*?(\d{1,4}).*?", lines)
    width = re.search("width.*?:.*?(\d{1,4}).*?", lines)
    height = re.search("height.*?:.*?(\d{1,4}).*?", lines)
    temp_list = {"id": int(css_id.group(1)), "left": int(left.group(1)), "top": int(top.group(1)),
                 "width": int(width.group(1)), "height": int(height.group(1))}
    divided_list.append(temp_list)

split_list = sorted(divided_list, key=lambda i: (i['id']))


def standardise_cords(list, cord):
    temp_list_2 = []
    for x in list:
        for y in range(x[cord] - 10, x[cord] + 10):
            if y in temp_list_2:
                cord = y
                temp_list_2.append(x['left'])


standardise_cords(split_list, 'left')
standardise_cords(split_list, 'top')
delegate_list = split_list[:57]
print(delegate_list)
replacement_list = split_list[57:]
print(replacement_list)
list_list = [delegate_list, replacement_list]
open('output.css', 'w').close()

im = Image.new('RGB', (SCREEN_SIZE_X, SCREEN_SIZE_Y), (255, 255, 255))
draw = ImageDraw.Draw(im)


def set_space(unsorted_list, width_space, height_space):
    sorted_list = sorted(unsorted_list, key=lambda i: (i['left'], i['top']))
    end_list = []
    for y in sorted_list:
        for x in sorted_list:
            if x['id'] == y['id']:
                continue
            if (y['top'] - y['height'] - y['height'] / 5 <= x['top'] <= y['top'] + y['height'] / 5) and x['top'] != y['top']:
                x['top'] = y['top']
            if (y['left'] - y['width'] - y['width'] / 5 <= x['left'] <= y['left'] + y['width'] / 5) and x['left'] != y['left']:
                x['left'] = y['left']
            if (y['left'] - y['width'] / 2 <= x['left'] <= y['left'] + y['width'] / 2 + y['width']) and x['top'] == y['top']:
                x['left'] = y['left'] + y['width'] + width_space
            if y['top'] + y['height'] - y['height'] / 5 <= x['top'] <= y['top'] + y['height'] + y['height'] * 0.8 and x['left'] == y['left']:
                x['top'] = y['top'] + y['height'] + height_space
        end_list.append(y.copy())
    return end_list


open("output.css", "a").write("/*Delegates*/\n")
spaced_delegate = set_space(delegate_list, 20, 20)
end_list = sorted(spaced_delegate, key=lambda i: (i['top'], i['left']))
open("output.css", "a").write("/*Stand ins*/\n")
spaced_replacement = set_space(replacement_list, 20, 20)
end_list = sorted(end_list, key=lambda i: (i['top'], i['left']))
bottom = max(spaced_replacement + spaced_delegate, key=lambda x: x['top'])
right = max(spaced_replacement + spaced_delegate, key=lambda x: x['left'])
top = min(spaced_replacement + spaced_delegate, key=lambda x: x['top'])
left = min(spaced_replacement + spaced_delegate, key=lambda x: x['left'])
move_x = round((SCREEN_SIZE_X - ((right['left'] + right['width']) - left['left'])) / 2)
move_y = round((SCREEN_SIZE_Y - ((bottom['top'] + right['height']) - top['top'])) / 2)
print(
    f"bottom: {bottom['top']}\ntop: {top['top']}\nleft: {left['left']}\nright: {right['left']}\n{move_x=}\n{move_y=}\n")

for wow in spaced_replacement + spaced_delegate:
    left_2 = wow['left'] + move_x - left['left']
    right_2 = wow['left'] + wow['width'] + move_x - left['left']
    top_2 = wow['top'] + move_y - top['top']
    bottom_2 = wow['top'] + wow['height'] + move_y - top['top']
    draw.rectangle((left_2, top_2, right_2, bottom_2), fill=(0, 192, 192), outline=(255, 255, 255))
    draw.text((left_2 + 10, top_2), str(wow['id']), font=ImageFont.truetype("Montserrat-Black", 36), fill=(0, 0, 0))
    with open("output.css", "a") as output:
        output.write(
            f"#vt{wow['id']}{{position:absolute; left:{left_2}px; padding-top:4px; top:{top_2}px; width:{wow['width']}px; height:{wow['height']}px}}\n")
    im.save('map.jpg', quality=95)
