from models import DnsHeader,DnsQuestion
import struct


def parse_name(packet, offset): #-> (domain,cursor_pos)
    labels = []
    while True:
        length = packet[offset]
        if (length & 0xC0) == 0xC0:
            pointer = struct.unpack("!H", packet[offset:offset+2])[0]
            pointer_offset = pointer & 0x3FFF
            pointed_name, _ = parse_name(packet, pointer_offset)
            labels.append(pointed_name)
            offset += 2
            break
        if length == 0:
            offset += 1
            break
        offset += 1
        label = packet[offset:offset+length].decode("utf-8")
        labels.append(label)
        offset += length
    return ".".join(labels), offset

def parse_header(packet):
    header = DnsHeader()
    unpacked_header = struct.unpack("!HHHHHH", packet[:12])
    header.packet_id = unpacked_header[0]
    flags = unpacked_header[1]
    header.qr = 1
    header.opcode = (flags >> 11) & 0b1111
    header.aa = 0
    header.tc = 0
    header.rd = (flags >> 8) & 0b1
    header.ra = 0
    header.z = 0
    if header.opcode == 0:
        header.rcode = 0
    else:
        header.rcode = 4
    header.ques_count = unpacked_header[2]
    header.ans_count = unpacked_header[2]
    header.auth_count = 0
    header.add_rec_count = 0
    return header

def parse_question(packet, offset):
    question = DnsQuestion()
    question.name, offset = parse_name(packet, offset)
    question.qtype = struct.unpack("!H",packet[offset:offset+2])[0]
    offset += 2
    question.qclass = struct.unpack("!H",packet[offset:offset+2])[0]
    offset += 2
    return question, offset