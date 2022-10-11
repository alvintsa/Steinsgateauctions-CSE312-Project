def req_parser(input):
    request = {}

    # isolate the headers, separate and decode them, split into individual header lines
    input_split = input.split("\r\n\r\n".encode())
    header_block = input_split[0].decode() 
    header_lines = header_block.split("\r\n")
    num_lines = len(header_lines)

    # request line formatted differently, handled separately.
    req_line = header_lines[0].split(" ")
    request["VERSION"] = req_line[0] 
    request["PATH"] = req_line[1] 
    request["TYPE"] = req_line[2] 

    # iterate through each other header, map header label to value in dictionary
    for lines in range(1,num_lines):
        line = lines.split(": ")
        request[line[0]] = line[1]

    if (len(input_split) > 1):
        request["BODY"] = input_split[1]
    else:
        request["BODY"] = ""

    return request

    # returns a map containing the information in the request parsed according to:
        # [VERSION] -> the version of http
        # [PATH] -> the path for the request
        # [TYPE] -> request type
        # [BODY] -> the (encoded) body of the request if it exists, otherwise an empty string
        # ["HEADER"] -> "HEADER-VALUE" for all other header lines