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
    temp_list = {"id": int(css_id.group(1)), "left": int(left.group(1)), "top": int(top.group(1)),"width": int(width.group(1)),"height": int(height.group(1))}
    divided_list.append(temp_list)

split_list = sorted(divided_list, key = lambda i: (i['id']))
print(split_list)
delegate_list = split_list[:61]
print(delegate_list)
replacement_list = split_list[61:]
print(replacement_list)

list_list = []
list_list.append(delegate_list)
list_list.append(replacement_list)
open('output.css', 'w').close()
for z in list_list:
    sorted_list = sorted(z, key=lambda i: (i['left'], i['top']))
    print(sorted_list)
    for y in sorted_list:
        top_left = y
        height = top_left['height']
        width = top_left['width']
        for x in sorted_list:
            if x['id'] == y['id']:
                continue
            if (top_left['top'] - height/5 <= x['top'] <= top_left['top'] + height/5) and x['top'] != top_left['top']:
                # print(f"#vt{x['id']} top {x['top']} to {top_left['top']}")
                x['top'] = top_left['top']
            if (top_left['left'] - width / 2 <= x['left'] <= top_left['left'] + width / 2) and x['left'] != top_left['left']:
                # print(f"#vt{x['id']} left {x['left']} to {top_left['left']}")
                x['left'] = top_left['left']
            if (top_left['left'] - width / 2 <= x['left'] <= top_left['left'] + width / 2 + width) and x['top'] == top_left['top']:
                # print(f"#vt{x['id']} left {x['left']} to {x['left'] + width + 5} by {top_left['id']}")
                x['left'] = top_left['left'] + width + 9
            if top_left['top'] + height - height/5 <= x['top'] <= top_left['top'] + height + height/2:
                x['top'] = top_left['top'] + height + 9
        with open("output.css", "a") as output:
            output.write(
                f"#vt{y['id']}{{position:absolute; left:{y['left']}px; padding-top:4px; top:{y['top']}px; width:{y['width']}px; height:{y['height']}px}}\n")
    print(sorted_list)
