from .req_parser import *
from ..helpers.global_constants import *

def con_parse(input, dict):
    parsed = req_parser(input)
    curr_length = int(dict.get(CL,0))
    add_length = int(parsed.get(CL,0))
    dict[CL] = str(curr_length + add_length)
    dict[B] += parsed[B]
    return dict