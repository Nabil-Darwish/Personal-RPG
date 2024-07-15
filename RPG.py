import random
import os
import sys
    

def main():
    HP = 5
    while HP > 0:
        text = input("Press Enter for next turn")
        if text == "":
            randomVariable = random.randint(0, 100)
            if randomVariable < 70:
                print("Hit!")
                HP -= 1
            else:
                print("Miss!")
            print(str(randomVariable) + "\n")
    print("Enemy defeated")

if __name__ == '__main__':
    sys.exit(main())