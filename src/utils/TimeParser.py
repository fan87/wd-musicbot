def parse(seconds: int) -> str:
    sec: int = seconds % 60
    minute: int = int((seconds - sec)/60) % 60
    hours: int = int(seconds/3600)
    print(hours)
    out = ""
    if not hours == 0:
        out += force_two_words(str(hours))
        out += ":"
        out += force_two_words(str(minute))
        out += ":"
        out += force_two_words(str(sec))
        return out
    else:
        out += force_two_words(str(minute))
        out += ":"
        out += force_two_words(str(sec))
    return out

def force_two_words(stringIn: str) -> str:
    while len(stringIn) <= 1:
        stringIn = "0" + stringIn
    return stringIn
