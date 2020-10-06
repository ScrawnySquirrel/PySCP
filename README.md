# PySCP
Simple Python application to transfer files between client and server.

## Getting Started
These instructions will guide how to GET/SEND files between the client and the server. The transferred files will be stored in a dedicated location.

## Prerequisite
* Python3

## Usage
The server needs to be running first before the client can start up.

### Server
To start the server:
```
python3 server_main.py
```
### Client
To start the client, server's IP must be passed:
```
python3 client_main.py -i 192.168.1.69
```

## Author

**Gabriel Lee** - [ScrawnySquirrel](https://github.com/ScrawnySquirrel)
