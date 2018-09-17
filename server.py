from socket import socket
from threading import Thread
from zlib import compress
from mss import mss

# 截图大小
WIDTH = int(1366 / 1)
HEIGHT = int(768 / 1)


def send_screenshot(conn):
    with mss() as sct:
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

        while 'recording':
            img = sct.grab(rect)
            # 压缩等级 (0-9)
            # 并不一定是压缩level越高越好，这里要综合考虑压缩占用时间和网络传输时间
            pixels = compress(img.bgra, 1)
            # 压缩对比
            # level:0 size:4196683
            # level:1 size:248329
            # level:2 size:246512
            # level:9 size:196212
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)
            conn.sendall(pixels)


def main(host='0.0.0.0', port=5000):
    sock = socket()
    sock.bind((host, port))
    try:
        sock.listen(5)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            thread = Thread(target=send_screenshot, args=(conn,))
            thread.start()
    finally:
        sock.close()


if __name__ == '__main__':
    main()
