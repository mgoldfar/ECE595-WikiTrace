#! /bin/bash -e

if (( $# < 5 ))
then
	echo "usage: run_test.sh <test_name> <baseid> <nruns> <script> [addl files]"
	echo "  <test_name>   Name to identify the test (will be used as the prefix of the request)"
	echo "  <baseid>      Number to indentify this test instance (used to ensure each client generates unique requests)"
	echo "  <nruns>       Number of run to execute the test for"
	echo "  <cache_type>  Cache type. NONE, DBA, DB, MEMCACHED"
	echo "  <script>      The main grinder script to run"
	echo "  [addl files]  Additional files required by the script (e.g. modules, input files etc.)"
	echo 
	exit 1
fi

TESTNAME=$1
BASEID=$2
NRUNS=$3
CACHETYPE=$4
shift 4

WORKDIR=$TESTNAME-$BASEID

mkdir -pv $WORKDIR

# Generate a grinder properties file
cat >$WORKDIR/grinder.properties <<EOL
grinder.script = $1

grinder.runs = $NRUNS
grinder.threads = 1

grinder.useConsole = false
grinder.logDirectory = log

ece595.testname = $TESTNAME
ece595.baseid = $BASEID
ece595.traceserver = 128.46.214.190:11211
ece595.url = http://sdcranch10.ecn.purdue.edu
ece595.cachetype = $CACHETYPE
EOL

for f in $*
do
	if [[ -d $f ]]
	then
		cp -Rv $f $WORKDIR
	else
		cp -v $f $WORKDIR
	fi
done

cd $WORKDIR
../startGrinderClient.sh grinder.properties
exit $?