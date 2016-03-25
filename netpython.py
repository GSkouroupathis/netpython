# Inspired by Black Hat Python, the book by Justin Seitz

import sys, socket, argparse, threading, subprocess

def read_and_send():
    while True:
        try:
            bffr = read_from_stdin()
        except KeyboardInterrupt:
            sys.exit(1)
        try:
            send_to_client(bffr)
        except KeyboardInterrupt:
            continue
        except:
            sys.exit(0)

def read_from_stdin():
    try:
        print
        print '___________________________ REQUEST ____________________________'
        bffr = raw_input()
        print '________________________________________________________________'
        print
        return bffr
    except KeyboardInterrupt:
        print '[*] Aborted'
        raise

def send_to_client(bffr):

    try:

        # send data if there is any
        if len(bffr):
            client.send(bffr)

        # wait for data back
        while True:

            response = client.recv(4096)
            if response and len(response) < 4096:
                break

        print
        print '*************************** RESPONSE ***************************'
        print response
        print '****************************************************************'
        print
        return 'wat'

    except KeyboardInterrupt:
        print '[*] Transfer Aborted'
        raise

    except Exception as exc:
        print '[*] Exiting:', exc
        raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', nargs=1, default='127.0.0.1',
        metavar='HOST')
    parser.add_argument('-p', '--port', nargs=1, default=1337, type=int,
        metavar='PORT')
    parser.add_argument('-l', '--listen', action='store_true',
        help='listen on [host]:[port] for incoming connections')
    parser.add_argument('-e', '--execute', nargs=1, metavar='FILE',
        help='execute the given file upon receiving a connection')
    parser.add_argument('-c', '--command', action='store_true',
        help='initialize a command shell')
    parser.add_argument('-u', '--upload', nargs=1, metavar='DESTINATION',
        help='upon receiving a connection, upload a file and write \
              to DESTINATION')
    args = parser.parse_args()

    # if running in server mode
    if args.listen:
        pass

    # if running in client mode
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((args.target, args.port))

        read_and_send()

        client.close()

    print args
