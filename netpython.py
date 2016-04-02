# Inspired by Black Hat Python, the book by Justin Seitz

import sys, socket, argparse, threading, subprocess

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((args.target[0], args.port[0]))
        read_and_send(client)
    except:
        print "[*] Client exited"
        client.close()
        raise

def read_and_send(client):
    while True:
        try:
            bffr = read_from_stdin() + '\n'
            send_to_client(client, bffr)
        except:
            raise

def read_from_stdin():
    try:
        #bffr = sys.stdin.read()
        bffr = raw_input()
        print repr(bffr)
        return bffr
    except KeyboardInterrupt:
        print '[*] Reading STDIN aborted'
        raise

def send_to_client(client, bffr):
    print client
    try:

        # send data if there is any
        print len(bffr)
        if len(bffr):
            print len(bffr)
            client.send(bffr)

        # wait for data back
        while True:

            response = client.recv(4096)
            if response and len(response) < 4096:
                break
            elif response:
                print "Response here"
            else:
                print len(response)
            sfdsfsdf=raw_input()

        print response,
        return

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
        try:
            client_socket, client_addr = server.accept()

            # spin off a thread to handle our new client
            client_thread = threading.Thread(target=client_handler,
                args=(client_socket,))
            client_thread.start()
        except KeyboardInterrupt:
            print '[*] Server exited'
            raise

def client_handler(client_socket):
    # check for keepalive
    if args.keepalive:

        try:
            while True:
                # show prompt
                data_buffer = ''
                while '\n' not in data_buffer:
                    data_buffer += client_socket.recv(1024)
                    print data_buffer

                print repr(data_buffer)

                # send back response to client
                client_socket.send('\n')
        except:
            pass

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
    parser.add_argument('-k', '--keepalive', action='store_true',
        help='keep alive the connection by responding with null packets')
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
        start_client()
