#! /bin/bash 

if (( $# < 5 ))
then
	echo "usage: launch_tests_ecelinux.sh <num_hosts> <test_name> <nruns> <script> [addl files]"
	echo "  <num_hosts>   The number of ecelinux hosts to run on."
	echo "  <test_name>   Name to identify the test (will be used as the prefix of the request)"
	echo "  <nruns>       Number of run to execute the test for"
	echo "  <cache_type>  Cache type. NONE, DBA, DB, MEMCACHED"
	echo "  <script>      The main grinder script to run"
	echo "  [addl files]  Additional files required by the script (e.g. modules, input files etc.)"
	echo 
	exit 1
fi

GRINDER_SCRIPT_DIR=wiki_trace/grinderscripts

TRACE_SERVER_USER=office
TRACE_SERVER_HOST=128.46.214.190
TRACE_SERVER_MEM=512

NUMHOSTS=$1
TESTNAME=$2
NRUNS=$3
CACHETYPE=$4
shift 4

# get NUMHOSTS live hosts
hosts=($(get_live_ecelinux_hosts.sh $NUMHOSTS))

# create a local directory for all of the stuff
WORKDIR=$TESTNAME
mkdir -pv $WORKDIR

# all hosts share files so make sure git is uptodate
ssh -o StrictHostKeyChecking=no mgoldfar@${hosts[0]} "cd ${GRINDER_SCRIPT_DIR}; git pull;"

# make sure memcached is running on the trace collector
memcache_pid=$(ssh -o StrictHostKeyChecking=no $TRACE_SERVER_USER@$TRACE_SERVER_HOST "pidof memcached;")
if [[ -z $memcache_pid ]]
then
		echo "Starting memcached on $TRACE_SERVER_HOST..."
		CMDSTR="nohup memcached -m $TRACE_SERVER_MEM > memcached.out 2> memcached.err < /dev/null &"
		ssh -o StrictHostKeyChecking=no $TRACE_SERVER_USER@$TRACE_SERVER_HOST $CMDSTR		
else
		echo "memcached is running on $TRACE_SERVER_HOST with PID $memcache_pid"
fi

# Launce the grinder jobs
((baseid=0))
pids=()
for h in ${hosts[*]}
do
		CMDINITSTR="source ~/.bash_profile; cd ${GRINDER_SCRIPT_DIR};"
		CMDSTR="./run_test.sh $TESTNAME $baseid $NRUNS $CACHETYPE $@"
		ssh -o StrictHostKeyChecking=no mgoldfar@$h "$CMDINITSTR $CMDSTR" 2>$WORKDIR/${h}.err >$WORKDIR/${h}.log &
		pids[$baseid]=$!
		((baseid++))
done

# wait for all remote hosts to exit
echo "Launched remote sessions: ${pids[*]}"
echo "Waiting for remote grinder processes to complete..."
wait ${pids[*]}

# copy the trace stats from the run to the local directory
((baseid=0))
for h in ${hosts[*]}
do	
		echo "Copying grinder results from $h..."
		scp -r -o StrictHostKeyChecking=no mgoldfar@$h:${GRINDER_SCRIPT_DIR}/${TESTNAME}-${baseid} ${WORKDIR}
		((baseid++))
done

# Download the traces from the trace cache
cd $WORKDIR
set -x
(( NTRACES=NRUNS*NUMHOSTS - 1 ))
../../parse_trace.py $TESTNAME 0 $NTRACES --trace_server=$TRACE_SERVER_HOST
cd ..

exit 0