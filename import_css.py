import re
file = open('input.css', 'r').read()
list_file = file.split('\n')
print(list_file)
divided_list = []
for lines in list_file:
    css_id = re.search("#vt(\d{1,3})", lines)
    left = re.search("left.*?:.*?(\d{1,4}).*?", lines)
    top = re.search("[^-]top.*?:.*?(\d{1,4}).*?", lines)
    width = re.search("[^-]width.*?:.*?(\d{1,4}).*?", lines)
    height = re.search("[^-]height.*?:.*?(\d{1,4}).*?", lines)
    temp_list = {"id": int(css_id.group(1)), "left": int(left.group(1)), "top": int(top.group(1)),"width": int(width.group(1)),"height": int(height.group(1))}
    divided_list.append(temp_list)
print(divided_list)
divided_list_copy = divided_list
sorted_list = sorted(divided_list, key = lambda i: (i['left'], i['top']))
print(sorted_list)
for y in sorted_list:
    top_left = y
    height = top_left['height']
    width = top_left['width']
    for x in sorted_list:
        if x['id'] == y['id']:
            continue
        if (top_left['top'] - height/5 <= x['top'] <= top_left['top'] + height/5) and x['top'] != top_left['top']:
            print(f"#vt{x['id']} top {x['top']} to {top_left['top']}")
            x['top'] = top_left['top']
        if (top_left['left'] - width / 2 <= x['left'] <= top_left['left'] + width / 2) and x['left'] != top_left['left']:
            print(f"#vt{x['id']} left {x['left']} to {top_left['left']}")
            x['left'] = top_left['left']
        if (top_left['left'] - width / 5 <= x['left'] <= top_left['left'] + width / 5 + width) and top_left['top'] - height/5 <= x['top'] <= top_left['top'] + height/5:
            print(f"#vt{x['id']} left {x['left']} to {x['left'] + width + 5} by {top_left['id']}")
            x['left'] = top_left['left'] + width + 5

print(sorted_list)
with open("output.css", "w") as output:
    for x in sorted_list:
        output.write(f"#vt{x['id']}{{position:absolute; left:{x['left']}px; padding-top:4px; top:{x['top']}px; width:{x['width']}px; height:{x['height']}px}}\n")
