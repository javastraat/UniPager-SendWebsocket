#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
##!/opt/homebrew/bin/python3.11
##!/usr/bin/python3
import json
import pprint
import websocket
import argparse
import sys

def user_input(prompt):
    if sys.version_info.major == 3:
        return input(prompt)
    elif sys.version_info.major == 2:
        return raw_input(prompt)
    else:
        raise NotImplementedError("Unsupported Python version")

print('Send paging call directly via Unipager v2.1')

from websocket import create_connection

DEBUG = False

def debug(str):
    if DEBUG:
        print(str)
    return

# Function to display WebSocket version
def display_websocket_version():
    print('Websocket version: ' + websocket.__version__)

# Function to display Python version
def display_python_version():
    print('Python version: {}.{}.{}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))

parser = argparse.ArgumentParser(description='unipager_send_v2.1.py --hostname serverip --password passw0rd --ric 1234567 --sender YOURCALL --msg "yourtext here"')
parser.add_argument('--hostname', default='localhost',
                    help='The host running Unipager, default localhost')
parser.add_argument('--port', default='8055',
                    help='The port Unipager is listening, default 8055')
parser.add_argument('--password', default=None, type=str,
                    help='The Unipager password, default empty')
parser.add_argument('--ric', dest='ric', default=None, type=int,
                    help='RIC to send the message to')
parser.add_argument('--type', dest='type', default=1,
                    help='0 = Numeric, 1 = Alphanumeric, default 1')
parser.add_argument('--func', dest='func', default=3,
                    help='Function Bits in POCSAG datagram, default 3')
parser.add_argument('--msg', dest='msg', default='',
                    help='Message, if containing spaces: "TEXT WITH SPACES"')
parser.add_argument('--sender', dest='sender', default='',
                    help='Sender of the message')
parser.add_argument('--debug', dest='debug', action='store_true',
                    help='Enable debug')
parser.add_argument('-i', '--interactive', action='store_true', help='Enable interactive mode')
parser.add_argument('-v', '--version', action='store_true', help='Display WebSocket and Python version')

args = parser.parse_args()

# Display WebSocket and Python version if -v flag is provided
if args.version:
    display_websocket_version()
    display_python_version()
    exit()

DEBUG |= args.debug
if DEBUG: print("Debug enabled")

if args.interactive:
    # Interactive input
    hostname_input = user_input("Enter the hostname (default: localhost): ")
    hostname = hostname_input or args.hostname

    port_input = user_input("Enter the port (default: 8055): ")
    port = port_input or args.port

    password_input = user_input("Enter the Unipager password (default: empty): ")
    password = password_input or args.password

    # Prompt for RIC until a valid integer is provided
    while True:
        try:
            ric_input = user_input("Enter the RIC to send the message to: ")
            ric = int(ric_input)
            break
        except ValueError:
            print("Invalid RIC. Please enter a valid integer.")

    msg_input = user_input("Enter the message: ")
    msg = msg_input or args.msg

    sender_input = user_input("Enter the sender callsign: ")
    sender = sender_input or args.sender

    print("\nPlease confirm the following inputs:")
    print("Hostname:", hostname)
    print("Port:", port)
    print("Password:", password)
    print("RIC:", ric)
    print("Message:", msg)
    print("Sender:", sender)

    confirmation = user_input("\nConfirm sending the message (yes/no, default: yes): ").lower()
    if confirmation != 'no':
        confirmation = 'yes'

    if confirmation == 'yes':
        if not msg:
            print('No message given, nothing to do')
            exit()
        if not sender:
            print('No sender given, nothing to do')
            exit()
    else:
        print("Message sending cancelled.")
        exit()
else:
    # Use command-line arguments
    hostname = args.hostname
    port = args.port
    password = args.password
    ric = args.ric
    msg = args.msg
    sender = args.sender

if not msg:
    print('No message given, nothing to do')
    exit()
if not ric:
    print('No RIC given, nothing to do')
    exit()
if not sender:
    print('No sender given, nothing to do')
    exit()

#websocket.enableTrace(True)

ws = create_connection('ws://' + hostname + ":" + port + '/')

# Switch Messagetype AlphaNum, Numeric
m_type = "AlphaNum" if args.type == "1" else "Numeric"

# Switch Messagefunction Func0, Func1, Func2, Func3
funcs = ["Func0", "Func1", "Func2", "Func3"]
m_func = funcs[int(args.func)]

# Prepend sender to the message
msg_with_sender = "{}: {}".format(sender, msg)

# SendMessage with Variables
ws.send('{"Authenticate":"' + password + '"}')
string_to_send = "{\"SendMessage\": {\"addr\": %s, \"data\": \"%s\", \"mtype\": \"%s\", \"func\": \"%s\"}}" % (ric, msg_with_sender, m_type, m_func)
debug(string_to_send)
ws.send(string_to_send)

