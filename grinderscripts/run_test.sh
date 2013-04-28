#! /bin/bash -e

if (( $# < 4 ))
then
	echo "usage: run_test.sh <test_name> <baseid> <nruns> <script> [addl files]"
	echo "  <test_name>   Name to identify the test (will be used as the prefix of the request)"
	echo "  <baseid>      Number to indtify this test instance (used to ensure each client generates unique requests)"
	echo "  <nruns>       Number of run to execute the test for"
	echo "  <script>      The main grinder script to run"
	echo "  [addl files]  Additional files required by the script (e.g. modules, input files etc.)"
	echo 
	exit 1
fi

TESTNAME=$1
WORKDIR=$1$2
BASEID=$2
NRUNS=$3
shift 3

mkdir -pv $WORKDIR

# Generate a grinder properties file
cat >$WORKDIR/grinder.properties <<EOL
grinder.script = $1

grinder.runs = $NRUNS
grinder.threads = 1

grinder.useConsole = false
grinder.logDirectory = log

request.baseid = $BASEID
request.url = http://sdcranch10.ecn.purdue.edu
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