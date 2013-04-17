#! /usr/bin/env python2.6

import os, sys, threading
import SocketServer
import Queue 

trace_queue = Queue.Queue()
writer_threads = []

class Handler(SocketServer.StreamRequestHandler):
    def handle(self):
        trace_queue.put(self.rfile.read())

def WriterThread(*args):
	thread_id = args[0]
	trace_id = 0
	trace_dir = "trace_%d" % ( thread_id, )

	if not os.path.exists(trace_dir):
		os.mkdir(trace_dir)
	
	while True:
		trace = trace_queue.get()
		trace_id += 1
		file_name = os.path.join(trace_dir, "trace_%d" % (trace_id, ))
		outfile = open(file_name, "w")
		outfile.write(trace)
		outfile.close()

if len(sys.argv) < 2 or len(sys.argv) > 4:
	sys.stderr.write("usage: trace_log_server.py <port> [nthreads=4]\n")
	sys.exit(1)

try:
	port = int(sys.argv[1])
	if port <= 0 or port > 65535:
		raise ValueError
except:
	sys.stderr.write("error: bad port number: %s" % (sys.argv[1]))
	sys.exit(1)

if len(sys.argv) < 3:
	nthreads = 4
else:
	try:
		nthreads = int(sys.argv[2])
		if nthreads <= 0:
			raise ValueError
	except:
		sys.stderr.write("error: bad thread count: %s" % (sys.argv[2]))
		sys.exit(1)

for i in range(nthreads):
	t = threading.Thread(target=WriterThread, args=[i])
	writer_threads.append(t)
	t.setDaemon(True)
	t.start()
	
server = SocketServer.TCPServer(("localhost", port), Handler)
server.serve_forever()

sys.exit(0)