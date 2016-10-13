import threading
import Queue
import time
import socket
import os

class SyncQueue :
    def __init__(self) :
        self.lock = threading.Lock()
        self.queue = Queue.Queue()
    def put(self, element) :
        self.lock.acquire()
        self.queue.put(element)
        self.lock.release()
    def get(self) :
        self.lock.acquire()
        element = None if self.queue.empty() else self.queue.get()
        self.lock.release()
        return element

class SyncOutput:
    def __init__(self):
        self.lock = threading.Lock()
        filename = self.getFileName()
        self.fhandle = open(filename, "w")
    def __del__(self):
        self.fhandle.close()
    def getFileName(self):
        outdir = "outdir"
        dirname = os.path.join(os.path.dirname(__file__), outdir)
        if not os.path.isdir(dirname): os.mkdir(dirname)
        filename = time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".out"
        return os.path.join(dirname, filename)

    def out(self, value):
        self.lock.acquire()
        print value
        line = value.strip() + "\n"
        self.fhandle.write(line)
        self.lock.release()

class HostThread(threading.Thread) :
    def __init__(self, domain_queue, output) :
        threading.Thread.__init__(self)
        self.domains_ = domain_queue
        self.outout_ = output
    def run(self):
        domain = self.domains_.get()
        while domain:
            try:
                host = socket.gethostbyname(domain)
                self.outout_.out(host + '\t' + domain)
            except: pass
            domain = self.domains_.get()
