import os
import sys
output = os.popen('git describe --tags --abbrev=0')
current_version = output.read()
tag_str = ""

for values in current_version:
    converted_tag = [v for v in values if v.isalnum()] and [v for v in values if not v.isalpha()]
    if not len(converted_tag) == 0:
        tag_str += converted_tag[0]

tag_num = int(tag_str)
sys.stdout.write(tag_str)
