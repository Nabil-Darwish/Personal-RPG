import random
import pygame

def pause(ticks):
    pygame.time.wait(ticks)

# Returns the max of 0 and the variable
def not_less_zero(variable):
    return max(0, variable)

# Returns a random element from a list
def pick_random_from(l):
    random_variable = random.randint(0, len(l)-1)
    return l[random_variable]

class Option:
    def __init__(self, text, function):
        self.text = text
        self.function = function

class OptionPicker:
    def __init__(self, question, options, error_message, backable=False):
        self.question = question
        self.options = options
        self.error_message = error_message
        self.backable = backable

    def pick(self):
        print(self.question)
        if self.backable:
            print("0. Back")
        while True:
            for index, option in enumerate(self.options):
                print(f"{index + 1}. " + option.text)
            choice = input()
            if choice.isdigit() and 1 <= int(choice) <= len(self.options):
                self.options[int(choice) - 1].function()
                break
            elif self.backable and choice == "0":
                return True
            else:
                print(self.error_message)