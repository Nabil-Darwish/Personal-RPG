import random
import re

def get_placeholders(line):
    pattern = r'\{(\w+)\}'
    return re.findall(pattern, line)

def get_lines_of_text(text_name):
    lines = open("text_templates/" + text_name + ".txt", 'r').readlines()
    return lines

def render_text(text_name, *args):
    possible_lines = get_lines_of_text(text_name)
    line = random.choice(possible_lines)
    placeholders = get_placeholders(line)
    if len(placeholders) == len(args):
        dictionary = dict(zip(placeholders, args))
        line = line.format(**dictionary)
    else:
        raise Exception("Not enough arguments to render text")
    return line