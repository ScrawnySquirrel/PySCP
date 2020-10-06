#!/usr/bin/python3.7

import sys
import socket
import argparse
import socket_helper as sh

def main(argv):

    parser = argparse.ArgumentParser(description='Python client/server application to GET/SEND files.')
    parser.add_argument('-i', '--ip', help='the server IP', required=True)
    args = parser.parse_args()

    if args.ip is not None:
        server = args.ip
    else:
        server = sh.serverIP

    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs.connect((server, sh.controlPort))

    sh.create_fileshare()

    while True:
        req_arr = sh.get_user_input()
        sh.client_request_handler(cs, req_arr)

    cs.close()

if __name__ == "__main__":
    main(sys.argv[1:])
