import readchar as rc

def in_key():
    ESC=27

    key=ord(rc.readchar())
    if key == ESC:
        key=ord(rc.readchar())
        if key == 91:
            key = ord(rc.readchar())
            if key == 65:
                return key
            elif key == 66:
                return key
    return key
