from .parse_header import *

def req_parser(input):
    # isolate the headers, separate and decode them, split into individual header lines
    blocks = input.split("\r\n\r\n".encode(),1)
    headers = parse_header(blocks[0].decode())
    headers["BODY"] = blocks[1]

    return headers

    # returns a map containing the information in the request parsed according to:
        # [VERSION] -> the version of http
        # [PATH] -> the path for the request
        # [TYPE] -> request type
        # [BODY] -> the (encoded) body of the request if it exists, otherwise an empty string
        # ["HEADER"] -> "HEADER-VALUE" for all other header lines