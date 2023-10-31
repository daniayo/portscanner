#기본적인 TCP 포트 스캔
 
import socket
import threading
import time
import json
class NormalScanner:
    def __init__(self):
        self._results = {}
        self._threads = []

    def scan(self, ip, start_port, end_port, task_number=20):
        self._threads = []
        for i in range(start_port, end_port, task_number):
            t = threading.Thread(target=self.work, args=(ip, i, i+task_number-1))
            t.start()
            self._threads.append(t)

        for i, thread in enumerate(self._threads):
            thread.join()

        return json.dumps(self._results)

    def work(self, ip, start_port, end_port):
        if end_port >= 65536:
            end_port = 65535
        for port in range(start_port, end_port+1):
            try:
                with socket.socket() as s:
                    s.settimeout(2)
                    s.connect((ip, port))
                    s.send("Python Connect\n".encode())
                    banner = s.recv(1024) 
                    if banner:
                        self._results[str(port)] = banner.decode().split('\n')[0]
                            
            except Exception as e:
                if str(e) == "timed out":
                    pass
                else:
                    if 'Errno 61' in str(e):
                        pass
                    else:
                        # print(e, port)
                        pass
 
def main():
    scanner = NormalScanner()
    results = scanner.scan('3.142.251.166', 1, 65535)
    
if __name__ == '__main__':
    main()

