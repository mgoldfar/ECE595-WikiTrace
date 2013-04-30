#! /bin/bash -e

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

NUMHOSTS=$1
TESTNAME=$2
NRUNS=$3
CACHETYPE=$4
shift 4

# get NUMHOSTS live hosts
hosts=($(get_live_ecelinux_hosts.sh $NUMHOSTS))

# all hosts share files so make sure git is uptodate
ssh -o StrictHostKeyChecking=no mgoldfar@${hosts[0]} "cd ${GRINDER_SCRIPT_DIR}; git pull;"

((baseid=0))
pids=()
for h in ${hosts[*]}
do
		CMDINITSTR="source ~/.bash_profile; cd ${GRINDER_SCRIPT_DIR};"
		CMDSTR="./run_test.sh $TESTNAME $baseid $NRUNS $CACHETYPE $@"
		ssh -o StrictHostKeyChecking=no mgoldfar@$h "$CMDINITSTR $CMDSTR" &
		pids[$baseid]=$!
		((baseid++))
done

# wait for all remote hosts to exit
echo "Waiting for processes to finish: ${pids[*]}"
wait ${pids[*]}

exit 0