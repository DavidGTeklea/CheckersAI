skillLevel = input("What skill level do you want to play against the Checkers AI? Beginner(b), medium(m), or hard(h): ")

stop = True

while stop:
    if skillLevel.lower() == "b":
        foresight = 1
        stop = False

    elif skillLevel.lower() == "m":
        foresight = 2
        stop = False

    elif skillLevel.lower() == "h":
        foresight = 7
        stop = False

    else:
        stop = True
