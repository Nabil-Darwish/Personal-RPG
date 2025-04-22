import random
import re

all_placeholders = {"unit_name" : "", "enemy_name" : "", "hit_chance" : "", "damage" : "", "former_unit_hp" : "", "current_unit_hp" : "", "former_enemy_hp": "", "current_enemy_hp": ""}

def get_placeholders(line):
    pattern = r'\{(\w+)\}'
    return re.findall(pattern, line)

def get_lines_of_text(text_name):
    lines = open("text_templates/" + text_name + ".txt", 'r').readlines()
    return lines

def render_text(text_name):
    possible_lines = get_lines_of_text(text_name)
    line = random.choice(possible_lines)

    line = line.format(**all_placeholders)

    # if len(placeholders) == len(args):
    #     dictionary = dict(zip(placeholders, args))
    #     line = line.format(**dictionary)
    # else:
    #     raise Exception("Not enough arguments to render text")
    print(line)