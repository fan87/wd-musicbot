def parse(seconds: int) -> str:
    sec: int = seconds % 60
    minute: int = int((seconds - sec)/60) % 60
    hours: int = int(seconds/3600)
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

def parse_milli(milli: int) -> str:
    ms: int = milli % 1000
    sec: int = int(milli/1000) % 60
    minute: int = int((int(milli/1000) - sec)/60) % 60
    hours: int = int(int(milli/1000)/3600)
    out = ""
    if not hours == 0:
        out += force_two_words(str(hours))
        out += ":"
        out += force_two_words(str(minute))
        out += ":"
        out += force_two_words(str(sec))
        out += "."
        out += force_two_words(str(ms))
        return out
    else:
        out += force_two_words(str(minute))
        out += ":"
        out += force_two_words(str(sec))
        out += "."
        out += force_two_words(str(ms))
    return out


def force_two_words(stringIn: str) -> str:
    while len(stringIn) <= 1:
        stringIn = "0" + stringIn
    return stringIn

def force_four_words(stringIn: str) -> str:
    while len(stringIn) <= 3:
        stringIn = "0" + stringIn
    return stringIn
