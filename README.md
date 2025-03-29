## Reverse-Shell-Using-TCP-Socket
The Reverse Shell project is a network-based application that allows a machine to gain command-line access to a remote target machine (client) through a reverse shell connection.

## Overview

This project implements a reverse shell using TCP sockets in Python. A reverse shell allows a machine to gain control of a target machine (client) by establishing a connection back to the attacker's machine. This project is intended for educational purposes only, to demonstrate the concepts of network programming, socket communication, and threading in Python.

## Libraries Used

- `socket`: For creating the TCP connection between the client and server.
- `sys`: For system-specific parameters and functions.
- `threading`: To handle multiple connections simultaneously.
- `time`: To manage timing and delays in the execution.
- `queue`: To manage command queues for processing.

## Features

- Establishes a TCP connection from the client to the server.
- Executes commands on the client machine and returns the output to the server.
- Supports multiple clients using threading.
- Simple command interface for interaction.

## Prerequisites

- Python 3.x installed on your machine.
- Basic understanding of Python and networking concepts.

## How to run?
Make sure to change the server ip in the client.py before running client.py
type the following in the shell of server machine: python3 server.py
and on client machine run: python3 client.py

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DivyanshSharmaji/Reverse-Shell-Project.git
   cd reverse-shell
