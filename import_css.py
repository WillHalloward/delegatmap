import re

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

left_points = []
top_points = []


# def standardise_cords(list, cord):
#     temp_list_2 = []
#     for x in list:
#         for y in range(cord - 10, cord + 10):
#             if y in left_points:
#                 cord = y
#                 temp_list_2.append(x['left'])
#                 break
#

for x in split_list:
    found = False
    for y in range(x['left'] - 10, x['left'] + 10):
        if y in left_points:
            found = True
            x['left'] = y
            break

    if not found:
        left_points.append(x['left'])

for x in split_list:
    found = False
    for y in range(x['top'] - 10, x['top'] + 10):
        if y in top_points:
            found = True
            x['top'] = y
            break

    if not found:
        top_points.append(x['top'])

delegate_list = split_list[:57]
print(delegate_list)
replacement_list = split_list[57:]
print(replacement_list)

list_list = [delegate_list, replacement_list]
open('output.css', 'w').close()
for z in list_list:
    sorted_list = sorted(z, key=lambda i: (i['left'], i['top']))
    for y in sorted_list:
        for x in sorted_list:
            if x['id'] == y['id']:
                continue
            if (y['top'] - y['height'] - y['height']/5 <= x['top'] <= y['top'] + y['height']/5) and x['top'] != y['top']:
                x['top'] = y['top']
            if (y['left'] - y['width'] - y['width']/5 <= x['left'] <= y['left'] + y['width']/5) and x['left'] != y['left']:
                x['left'] = y['left']
            if (y['left'] - y['width'] / 2 <= x['left'] <= y['left'] + y['width'] / 2 + y['width']) and x['top'] == y['top']:
                x['left'] = y['left'] + y['width'] + 20
            if y['top'] + y['height'] - y['height'] / 5 <= x['top'] <= y['top'] + y['height'] + y['height'] * 0.8 and x['left'] == y['left']:
                x['top'] = y['top'] + y['height'] + 20
        with open("output.css", "a") as output:
            output.write(
                f"#vt{y['id']}{{position:absolute; left:{y['left']}px; padding-top:4px; top:{y['top']}px; width:{y['width']}px; height:{y['height']}px}}\n")
