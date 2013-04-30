#! /bin/sh -e

exec -a "grinder" java -Xmx1g -cp $CLASSPATH net.grinder.Grinder $1
