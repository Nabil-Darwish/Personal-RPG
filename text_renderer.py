import random
import re

all_placeholders = {"unit_name" : "", "enemy_name" : "", "hit_chance" : "", "damage" : "", "former_unit_hp" : "", "current_unit_hp" : "", "former_enemy_hp": "", "current_enemy_hp": ""}

# Search in text for placeholders
def get_placeholders(line):
    pattern = r'\{(\w+)\}'
    return re.findall(pattern, line)

# Get lines of text
def get_lines_of_text(text_name):
    lines = open("text_templates/" + text_name + ".txt", 'r').readlines()
    return lines

# Render text
def render_text(text_name):
    possible_lines = get_lines_of_text(text_name)
    line = random.choice(possible_lines)

    line = line.format(**all_placeholders)
    print(line)
