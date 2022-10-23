from ..helpers.global_constants import *

def parse_form(dict):
    bound = dict["Content-Type"].split("boundary=")[1]
    body = dict[B].decode()

    data = body.split(bound)

    for uinput in data:
        if "Content-Disposition" in uinput:
            uinput = uinput.split("name=")[1]
            uinput = uinput.split("/r/n/r/n")
            for char in uinput[0]:
                char.repalce("\"","")
            dict[uinput[0]] = uinput[1]
    
    return dict