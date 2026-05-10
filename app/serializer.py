import struct
from protocol import NULL_TERMINATOR
def encode_name(name):
    labels = name.split(".")
    name_bytes = b""
    for lab in labels:
        label_bytes =  len(lab).to_bytes(1,'big') + lab.encode('utf-8')
        name_bytes = name_bytes + label_bytes
    return name_bytes + NULL_TERMINATOR

def serialize_header(header):
    flags = (
        (header.qr << 15)
        | (header.opcode << 11)
        | (header.aa << 10)
        | (header.tc << 9)
        | (header.rd << 8)
        | (header.ra << 7)
        | (header.z << 4)
        | (header.rcode)
    )
    return struct.pack(
        "!HHHHHH",
        header.packet_id,
        flags,
        header.ques_count,
        header.ans_count,
        header.auth_count,
        header.add_rec_count
    )

def serialize_question(question):
    return (
        encode_name(question.name)
        + struct.pack("!H", question.qtype)
        + struct.pack("!H", question.qclass)
    )

def serialize_answer(answer):
    ip_parts = map(int, answer.rdata.split("."))
    data_bytes = b""
    for part in ip_parts:
        data_bytes += struct.pack("!B", part)
    return (
        encode_name(answer.name)
        + struct.pack("!H", answer.rtype)
        + struct.pack("!H", answer.rclass)
        + struct.pack("!I", answer.ttl)
        + struct.pack("!H", answer.rdlength)
        + data_bytes
    )
