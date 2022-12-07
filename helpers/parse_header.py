def parse_header(header_block):
    headers = {}
    all_headers = header_block.split("\r\n")

    req_line = all_headers[0].split(" ")
    header_lines = all_headers[1:]

    headers["TYPE"] = req_line[0]
    headers["PATH"] = req_line[1]

    for line in header_lines:
        header = line.split(": ")
        headers[header[0]] = header[1]

    return headers