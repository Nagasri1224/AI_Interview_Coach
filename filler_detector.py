fillers = [
    "um",
    "uh",
    "like",
    "actually",
    "basically",
    "you know"
]

def analyze_fillers(text):

    text = text.lower()

    filler_count = 0

    for word in fillers:
        filler_count += text.count(word)

    if filler_count <= 2:
        penalty = 0
    elif filler_count <= 5:
        penalty = 5
    elif filler_count <= 10:
        penalty = 10
    else:
        penalty = 20

    return filler_count, penalty