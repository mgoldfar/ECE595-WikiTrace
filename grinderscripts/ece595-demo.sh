#! /bin/bash -x

for c in MEMCACHED
do
		./launch_tests_ecelinux.sh 10 ECE595Demo-$c 2 $c simple_reader_demo.py Wikiparser.py
		cd ECE595Demo-$c
		for s in small
		do
				../../parse_trace.py ECE595Demo-$c-$s 0 19 --trace_server=128.46.214.190 --download_only
		done
		cd ..
done
