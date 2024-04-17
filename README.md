# UniPager-SendWebsocket
## Version 1: unipager_send_websocket.py
Original from dk4pa
Send local Message over Websocket connection.

Options are:

ric, text, m_type(AlphaNum or Numeric), m_func(Func0-3)

## Version 2: unipager_send.py
* Password authentification implemented
* Command line arguments with default values

````
usage: unipager_send.py [-h] [--hostname HOSTNAME] [--port PORT]
                        [--password PASSWORD] [--ric RIC] [--type TYPE]
                        [--func FUNC] [--msg MSG] [--debug]

Send paging call direct via Unipager

optional arguments:
  -h, --help           show this help message and exit
  --hostname HOSTNAME  The host running Unipager, default localhost
  --port PORT          The port Unipager is listening, default 8055
  --password PASSWORD  The Unipager password, default empty
  --ric RIC            RIC to send the message to
  --type TYPE          0 = Numeric, 1 = Alphanumeric, default 1
  --func FUNC          Function Bits in POCSAG datagram, default 3
  --msg MSG            Message, if containing spaces: "TEXT WITH SPACES"
  --debug              Enable debug
````
## Version 2.1: unipager_send_v2.1.py
* Interactive mode 
* Sender option added to add before msg text f.e. PD2EMC: message
* Show websocket en python version 
````
Send paging call directly via Unipager
usage: unipager_send_v2.1.py [-h] [--hostname HOSTNAME] [--port PORT]
                             [--password PASSWORD] [--ric RIC] [--type TYPE]
                             [--func FUNC] [--msg MSG] [--sender SENDER]
                             [--debug] [-i] [-v]

unipager_send_v2.1.py --hostname serverip --password passw0rd --ric 1234567
--sender YOURCALL --msg "yourtext here"

optional arguments:
  -h, --help           show this help message and exit
  --hostname HOSTNAME  The host running Unipager, default localhost
  --port PORT          The port Unipager is listening, default 8055
  --password PASSWORD  The Unipager password, default empty
  --ric RIC            RIC to send the message to
  --type TYPE          0 = Numeric, 1 = Alphanumeric, default 1
  --func FUNC          Function Bits in POCSAG datagram, default 3
  --msg MSG            Message, if containing spaces: "TEXT WITH SPACES"
  --sender SENDER      Sender of the message
  --debug              Enable debug
  -i, --interactive    Enable interactive mode
  -v, --version        Display WebSocket and Python version
````
````
unipager_send_v2.1.py -i

Send paging call directly via Unipager
Enter the hostname (default: localhost): your unipager ip
Enter the port (default: 8055): 
Enter the Unipager password (default: empty): your unipager password
Enter the RIC to send the message to: receiver RIC/DMR ID
Enter the message: your text to send
Enter the sender callsign: sender callsign
````
