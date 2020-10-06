#!/usr/bin/python3.7

import sys
import socket
import socket_helper as sh

def main(argv):
    cs = sh.socket_bind_listen(sh.controlHost, sh.controlPort)
    cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sh.create_fileshare()

    while True:
        csConnection, csAddress = cs.accept()
        print('Client Connection:', csAddress)
        sh.get_request(csConnection, csAddress)

    cs.close()

if __name__ == "__main__":
    main(sys.argv[1:])
