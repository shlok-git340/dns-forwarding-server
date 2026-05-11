import time
from models import DnsHeader
from serializer import (serialize_header,serialize_question)
from protocol import DEFAULT_TTL

cache = {}
#cache dictonary == cache = {"google.com":(answer_section_bytes,expiry_time)}


def forward_question(question,dns_header,resolver_ip,resolver_port,resolver_socket):
    current_time = time.time()
    if question.name in cache:
        cached_answer , expiry = cache[question.name]
        if current_time < expiry:
            print(f"cache hit: {question.name}")
            return cached_answer
        else:
            del cache[question.name]
    
    forward_header = DnsHeader()
    forward_header.packet_id = dns_header.packet_id
    forward_header.qr = 0
    forward_header.opcode = dns_header.opcode
    forward_header.aa = 0
    forward_header.tc = 0
    forward_header.rd = dns_header.rd
    forward_header.ra = 0
    forward_header.z = 0
    forward_header.rcode = 0
    forward_header.ques_count = 1
    forward_header.ans_count = 0
    forward_header.auth_count = 0
    forward_header.add_rec_count = 0
    forward_packet = (serialize_header(forward_header)+ serialize_question(question))
    resolver_socket.sendto(forward_packet,(resolver_ip, resolver_port))
    resolver_response, _ = resolver_socket.recvfrom(512)
    question_size = len(serialize_question(question))
    answer_section = resolver_response[12 + question_size:]

    expiry_time = current_time + DEFAULT_TTL
    cache[question.name] = (answer_section,expiry_time)

    return answer_section

