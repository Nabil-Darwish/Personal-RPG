import random
import pygame

class ObserverNotFoundError(Exception):
    pass

def pause(ticks):
    pygame.time.wait(ticks)

# Returns the max of 0 and the variable
def not_less_zero(variable):
    return max(0, variable)

# Returns a random element from a list
def pick_random_from(l):
    random_variable = random.randint(0, len(l)-1)
    return l[random_variable]

def update_dict_with_valid_key(dictionary, key, value):
    if key in dictionary:
        dictionary[key] = value
    else:
        raise KeyError(f"Key {key} does not exist in the dictionary")

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

class Subject:
    def __init__(self):
        # Initialize an empty dictionary to store observers
        self.observers = {}

    def add_observer(self, notification_type, observer):
        # Add an observer to the dictionary for a specific notification type
        if notification_type not in self.observers:
            # Create a new list for the notification type if it doesn't exist
            self.observers[notification_type] = []
        # Add the observer to the list for the notification type
        self.observers[notification_type].append(observer)

    def remove_observer(self, notification_type, observer):
        # Remove an observer from the dictionary for a specific notification type
        if notification_type in self.observers:
            # Check if the observer is in the list for the notification type
            if observer in self.observers[notification_type]:
                # Remove the observer from the list
                self.observers[notification_type].remove(observer)
            else:
                # Raise an error if the observer is not found
                raise ObserverNotFoundError("Observer not found")
        else:
            # Raise an error if the notification type is not found
            raise ObserverNotFoundError("Notification type not found")

    def notify_observers(self, notification_type, *args, **kwargs):
        # Notify all observers for a specific notification type
        if notification_type in self.observers:
            # Iterate over the observers for the notification type
            for observer in self.observers[notification_type]:
                # Call the observer function or method, passing any additional arguments
                observer(*args, **kwargs)