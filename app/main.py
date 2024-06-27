# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn,address=server_socket.accept() # wait for client
    data=conn.recv(4096).decode().split('\r\n')
    request=data[0].split(' ')
    response=f'HTTP/1.1 404 Not Found\r\n\r\n'.encode()
    if request[1]=='/':
        response=f'HTTP/1.1 200 OK\r\n\r\n'.encode()
    elif 'echo' in request[1]:
        endpoint=request[1].split('/')[2]
        response=f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(endpoint)}\r\n\r\n{endpoint}'.encode()
    conn.sendall(response)

if __name__ == "__main__":
    main()
