import os

from HostThread import SyncOutput, SyncQueue, HostThread
from MatchDomain import matchDomain


def main():
    queue = SyncQueue()
    output = SyncOutput()
    for domain in matchDomain("baidu***.com"):
        queue.put(domain)

    threads = []
    for i in range(0, 5):
        t = HostThread(queue, output)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

def foo():
    outdir = "outdir"
    dirname = os.path.join(os.path.dirname(__file__), outdir)
    filename = os.path.join(os.path.dirname(__file__), outdir, "hello")
    if not os.path.isdir(dirname): os.mkdir(dirname)


if __name__ == "__main__":
    main()
    #foo()

