# Inspired by Black Hat Python, the book by Justin Seitz

import sys, socket, argparse, threading, subprocess

if __name__ == '__main__':
	print 'main'
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', nargs=1, metavar='HOST')
    parser.add_argument('-p', '--port', nargs=1, metavar='PORT')
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
		pass
