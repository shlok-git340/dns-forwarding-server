

````markdown
# DNS Forwarding Server

A DNS forwarding server built from scratch in Python using UDP sockets and raw DNS packet parsing.

This project implements core DNS protocol mechanics including:

- DNS packet parsing and serialization
- DNS header bitfield handling
- DNS question and answer sections
- DNS name compression parsing
- UDP socket communication
- DNS forwarding to upstream recursive resolvers
- Multi-question query handling

The server forwards incoming DNS queries to an upstream recursive resolver (such as Google's `8.8.8.8`) and relays the response back to the client.

---

# Features

- Built completely using Python standard library
- Manual DNS packet parsing using `struct`
- DNS compression pointer support
- Dynamic DNS query forwarding
- Multiple question parsing support
- Clean modular architecture

---

# Project Structure

```text
dns-forwarding-server/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── parser.py
│   ├── serializer.py
│   ├── resolver.py
│   └── protocol.py
│
├── tests/
│   └── client.py
│
├── README.md
├── requirements.txt
└── .gitignore
````

---

# Architecture

The project is split into multiple layers to separate protocol parsing, serialization and networking concerns.

## `main.py`

Application entrypoint.

Responsibilities:

* Create UDP sockets
* Receive DNS packets
* Parse incoming queries
* Forward questions to upstream resolver
* Construct and send final DNS response

---

## `models.py`

Contains semantic DNS protocol objects.

Classes:

* `DnsHeader`
* `DnsQuestion`
* `DnsAnswer`

These classes represent DNS structures internally.

---

## `parser.py`

Responsible for converting raw DNS packet bytes into Python objects.

Implements:

* DNS header parsing
* DNS question parsing
* DNS compression pointer parsing
* Domain label decoding

---

## `serializer.py`

Responsible for converting Python DNS objects back into raw bytes.

Implements:

* DNS header serialization
* Question serialization
* Answer serialization
* Domain name encoding

---

## `resolver.py`

Handles communication with upstream DNS resolvers.

Responsibilities:

* Build forwarding DNS packets
* Send DNS queries upstream
* Receive upstream responses
* Extract answer sections

---

## `protocol.py`

Contains protocol-level constants such as:

* DNS record types
* DNS classes
* TTL defaults
* Packet size constants

---

# DNS Compression Support

The server supports DNS compressed label parsing as defined in RFC 1035.

Example compression pointer:

```text
c0 0c
```

This allows DNS packets to reuse previously encoded domain labels efficiently.

---

# How It Works

```text
Client
   ↓
DNS Forwarding Server
   ↓
Upstream Recursive Resolver (8.8.8.8)
   ↓
DNS Forwarding Server
   ↓
Client
```

The server acts as a DNS proxy:

1. Receives DNS query
2. Parses packet structure
3. Forwards query upstream
4. Receives actual DNS response
5. Relays response back to client

---

# Running The Server

## Start the DNS forwarding server

```bash
python3 app/main.py --resolver 8.8.8.8:53
```

This starts the server on:

```text
127.0.0.1:2053
```

---

# Testing The Server

The server runs locally on your machine.

You can test it using the `dig` command.

Example:

```bash
dig @127.0.0.1 -p 2053 google.com
```

Example output:

```text
;; ANSWER SECTION:
google.com.    172 IN A 142.250.183.238
```

You can also test multiple queries:

```bash
dig @127.0.0.1 -p 2053 openai.com
```

---

---

# Technologies Used

* Python
* UDP sockets
* DNS protocol (RFC 1035)
* Binary packet parsing
* Bitwise operations

---

# Learning Outcomes

This project helped me understand:

* Binary protocol parsing
* UDP networking
* DNS packet structure
* Bitfield manipulation
* Recursive resolver forwarding
* Compression pointer parsing
* Network protocol interoperability

---

# References

* RFC 1035
* DNS packet format documentation
* Codecrafters DNS Server Challenge
* dig utility