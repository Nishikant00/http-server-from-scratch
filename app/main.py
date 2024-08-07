import socket
import threading
import sys
import gzip
def connection_handler(conn,address):
    data=conn.recv(4096).decode().split('\r\n')
    request=data[0].split(' ')
    response=f'HTTP/1.1 404 Not Found\r\n\r\n'
    if request[1]=='/':
        response=f'HTTP/1.1 200 OK\r\n\r\n'
    elif 'echo' in request[1]:
        endpoint=request[1].split('/')[2]
        response=f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(endpoint)}\r\n\r\n{endpoint}'
        if 'Accept-Encoding' in data[2]:
            compression_req=data[2].split(",")
            for i in compression_req:
                if 'encoding' in i:
                    response=f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n'
                else:
                    
                    body=request[1].split('/')[2].encode()
                    compressed_data=gzip.compress(body)
                    print(data)
                    print(request[1].split('/')[2])
                    print(compressed_data)
                    response=f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(compressed_data)}\r\nContent-Encoding: gzip\r\n\r\n".encode()+compressed_data
                    break  
    elif 'user-agent' in request[1]:
        response=f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(data[2].split(' ')[1])}\r\n\r\n{data[2].split(' ')[1]}'
    elif 'POST' in request[0] and 'files' in request[1]:
        try:
            with open(f'/{sys.argv[2]}/{request[1].split('/')[2]}','w') as f:
                file_contents=f.write(data[-1])
                response=f'HTTP/1.1 201 Created\r\n\r\n'
        except Exception as e:
            print(e)
    elif 'files' in request[1]:
        try:
            with open(f'/{sys.argv[2]}/{request[1].split('/')[2]}','r') as f:
                file_contents=f.read()
                response=f'HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length:{len(file_contents)}\r\n\r\n{file_contents}'
        except Exception as e:
            print(e)
    try:
        conn.sendall(response.encode())
    except AttributeError as e:
        conn.sendall(response)
    conn.close()

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    try:
        while True:
            conn,address=server_socket.accept() 
            threading.Thread(target=connection_handler, args=(conn, address)).start()
    except:
        print('Server is shutting down')
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
