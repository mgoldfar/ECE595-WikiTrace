#! /bin/bash -e

if (( $# != 4 ))
then
	echo "usage: run_test.sh <script> <nruns> <baseid> <workdir>"
	exit 1
fi

mkdir -p $4

# Generate a grinder properties file
cat >$4/grinder.properties <<EOL
grinder.script = $1

grinder.runs = $2
grinder.threads = 1

grinder.useConsole = false
grinder.logDirectory = log

request.baseid = $3
request.url = http://sdcranch10.ecn.purdue.edu
EOL

# copy script and deps to local dir
cp $1 $4
cp Wikiparser.py $4

cd $4
../startGrinderClient.sh grinder.properties
exit $?