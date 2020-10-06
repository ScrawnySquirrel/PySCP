#!/usr/bin/python3.7

import sys
import socket
import argparse
import socket_helper as sh

def main(argv):

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--ip', help='the server IP')
    args = parser.parse_args()

    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs.connect((sh.serverIP, sh.controlPort))

    sh.create_fileshare()

    while True:
        req_arr = sh.get_user_input()
        sh.client_request_handler(cs, req_arr)

    cs.close()

if __name__ == "__main__":
    main(sys.argv[1:])
