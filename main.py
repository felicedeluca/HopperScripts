doc = Document.getCurrentDocument()


def is_valid_ascii(byte):
    return b'0x20' <= byte <= b'0x7e'


def is_null(byte):
    return byte == 0x00


def is_sb_start(string: str):
    if string == "appleevent-send":
        doc.log("found sb start")
        return True
    return False


MIN_LEN = 8

num_strings = 0
start_string = 0
string_len = 0

for seg_id in range(0, doc.getSegmentCount()):
    seg = doc.getSegment(seg_id)

    seg_start = seg.getStartingAddress()
    seg_stop = seg_start + seg.getLength()
    seg_len = seg.getLength()

    string_bytes = bytearray()

    i = 0
    for adr in range(seg_start, seg_stop):
        val = seg.readByte(adr)
        i += 1
        # if i % 10000 == 0:
        # doc.log("%.1f%% " % (i * 100.0 / seg_len))

        if is_valid_ascii(val):
            string_bytes.append(val)
            string_len += 1
            if start_string == 0:
                start_string = adr
        elif is_null(val):
            if string_len >= MIN_LEN:
                # seg.setTypeAtAddress(start_string, string_len + 1, Segment.TYPE_ASCII)
                num_strings += 1
                string_len = 0
                start_string = 0
                string_bytes.append(val)
                encoded_string = string_bytes.decode("utf-8")
                string_bytes = bytearray()
                if is_valid_ascii(encoded_string):
                    exit(1)
            else:
                start_string = 0
                string_len = 0
                string_bytes = bytearray()
        else:
            start_string = 0
            string_len = 0
            string_bytes = bytearray()

doc.log("Found and marked " + str(num_strings) + " strings.")
doc.refreshView()
