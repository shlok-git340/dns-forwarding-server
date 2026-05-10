import socket 
import sys
from parser import parse_header,parse_question
from serializer import serialize_header,serialize_question
from resolver import forward_question

def main():
    print("server started")
    udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1",2053))
    resolver = sys.argv[2]
    resolver_ip,resolver_port = resolver.split(":")
    resolver_port = int(resolver_port)
    resolver_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            dns_header = parse_header(buf)
            questions = []
            offset = 12
            for _ in range(dns_header.ques_count):
                question,offset = parse_question(buf,offset)
                questions.append(question)
            #previous fake answer logic
            # answer_bytes = b""
            # for ques in questions:
            #     dns_answer = DnsAnswer()
            #     dns_answer.name = ques.name
            #     answer_bytes += dns_answer.answer_serializer()

            question_bytes = b""
            for question in questions:
                question_bytes += serialize_question(question)

            answer_bytes = b""
            for question in questions:
                answer_bytes += forward_question(question,dns_header,resolver_ip,resolver_port,resolver_socket)
            dns_header.ans_count = len(questions)
            response = serialize_header(dns_header) + question_bytes + answer_bytes
            
            udp_socket.sendto(response, source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            continue


if __name__ == "__main__":
    main()
