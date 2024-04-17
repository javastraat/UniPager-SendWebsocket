import json
import pprint
import websocket
import argparse

print('Send paging call directly via Unipager')
print('Websocket version: ' + websocket.__version__)

from websocket import create_connection

DEBUG = False

def debug( str ):
    if DEBUG:
        print (str)
    return

parser = argparse.ArgumentParser(description='f.e. unipager_send.py --hostname serverip --password passw0rd --ric 1234 --msg "yourtext here"')
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

args = parser.parse_args()
DEBUG |= args.debug
if DEBUG: print("Debug enabled")

if args.interactive:
    # Interactive input
    hostname = input("Enter the hostname (default: localhost): ") or args.hostname
    port = input("Enter the port (default: 8055): ") or args.port
    password = input("Enter the Unipager password (default: empty): ") or args.password

    # Prompt for RIC until a valid integer is provided
    while True:
        try:
            ric = int(input("Enter the RIC to send the message to: "))
            break
        except ValueError:
            print("Invalid RIC. Please enter a valid integer.")

    msg = args.msg
    while not msg:
        msg = input("Enter the message: ") or args.msg
    
    sender = args.sender
    while not sender:
        sender = input("Enter the sender: ") or args.sender

    if not msg:
        print('No message given, nothing to do')
        exit()
    if not sender:
        print('No sender given, nothing to do')
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
msg_with_sender = f"{sender}: {msg}"

# SendMessage with Variables
ws.send('{"Authenticate":"' + password + '"}')
string_to_send = "{\"SendMessage\": {\"addr\": %s, \"data\": \"%s\", \"mtype\": \"%s\", \"func\": \"%s\"}}" % (ric, msg_with_sender, m_type, m_func)
debug(string_to_send)
ws.send(string_to_send)
