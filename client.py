from socket import socket
from zlib import decompress
import cv2
import numpy
from PIL import Image

# 截图大小
WIDTH = int(1366 / 1)
HEIGHT = int(768 / 1)


def recvall(conn, length):
    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


# host为server的ip
def main(host='10.100.40.52', port=5000):
    watching = True

    sock = socket()
    sock.connect((host, port))
    try:
        while watching:
            size_len = int.from_bytes(sock.recv(1), byteorder='big')
            size = int.from_bytes(sock.recv(size_len), byteorder='big')
            # 解压缩
            bgra = decompress(recvall(sock, size))
            img = Image.frombytes("RGB", (WIDTH, HEIGHT), bgra, "raw", "BGRX")
            np_ar = numpy.array(img, dtype=numpy.uint8)
            # 因为OpenCV模式色彩默认是BGR（红色和蓝色互换了）
            # 这里就是把BGR改成RGB
            np_ar = numpy.flip(np_ar[:, :, :3], 2)
            cv2.imshow("OpenCV show", np_ar)

            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
    finally:
        sock.close()


if __name__ == '__main__':
    main()
