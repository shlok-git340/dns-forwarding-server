from protocol import TYPE_A, CLASS_IN, DEFAULT_TTL
class DnsHeader:
    def __init__(self):
        self.packet_id = None
        self.qr = None
        self.opcode = None
        self.aa = None
        self.tc = None
        self.rd = None
        self.ra = None
        self.z = None
        self.rcode = None
        self.ques_count = None
        self.ans_count = None
        self.auth_count = None
        self.add_rec_count = None
  

class DnsQuestion:
        def __init__(self):
            self.name = None
            self.qtype = None
            self.qclass = None
 
class DnsAnswer:
    """Resource Records"""
    def __init__(self):
        self.name = ""
        self.rtype = TYPE_A
        self.rclass = CLASS_IN
        self.ttl = DEFAULT_TTL
        self.rdlength = 4
        self.rdata = "8.8.8.8"
   