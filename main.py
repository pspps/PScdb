#!/usr/bin/python3
import re
import sys
import json

# we can call it "I'm to lazy for argument parsing..."
ignore_files = [
    re.compile("libjpeg-turbo"),
]
ignore_arguments = {
    "-fPIC",
}
ignore_arguments_with_value = {
    "-O",
    "-Wall",
}


assert len(sys.argv) == 2

db = json.load(open(sys.argv[1], "r"))

def filter_files(cu):
    for pattern in ignore_files:
        if pattern.findall(cu["file"]):
            return False
    return True

def process_arguments(cu):
    def filter_arguments(arg):
        if filter_arguments.ignore_next:
            filter_arguments.ignore_next -= 1
            return False
        if arg in ignore_arguments:
            return False
        for ignored in ignore_arguments_with_value:
            if not arg.startswith(ignored):
                continue
            if arg == ignored:
                filter_arguments.ignore_next = 1
            return False
        return True
    filter_arguments.ignore_next = 0

    cu["arguments"] = list(filter(filter_arguments, cu["arguments"]))

db = list(filter(filter_files, db))
for cu in db:
    process_arguments(cu)


print(json.dumps(db, sort_keys=True, indent=4))
