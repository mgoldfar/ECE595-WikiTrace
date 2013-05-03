#! /bin/bash

set -e
set -o pipefail

if (( $# < 1 || $# > 5 ))
then
    echo "usage: put_wiki_dump.sh <--file=dump_file.xml> [--host=<db host>] [--user=<user>] [--password=<password>] [--rebuild]"
    exit 1
fi

FILE=""
HOST="localhost"
USER="wikiuser"
PASS="wikiuser"
REBUILD=0
for arg in "$@"
do
    IFS='='
    set -- ${arg#--}
    
    case $1 in
	"file")
	    FILE=$2
	    ;;
	"host")
	    HOST=$2
	    ;;
	"user")
	    USER=$2
	    ;;
	"password")
	    PASSWORD=$2
	    ;;
	"rebuild")
	    REBUILD=1
	    ;;
	*)
	    echo "error: unknown option $1"
	    exit 1
	    ;;
    esac
done

# generate the SQL dump file
SQL=$FILE.sql
LOG=$FILE.log
java -jar ./mwdumper-1.16.jar --format=sql:1.5 $FILE > $SQL 2> $LOG


# update the table names for out wiki
sed -i 's/INSERT INTO revision/INSERT INTO wiki_revision/g' $SQL 2>> $LOG
sed -i 's/INSERT INTO page/INSERT INTO wiki_page/g' $SQL 2>> $LOG
sed -i 's/INSERT INTO text/INSERT INTO wiki_text/g' $SQL 2>> $LOG

# update the DB
cat $SQL | mysql --host=$HOST --user=$USER --password=$PASS wiki 2>> $LOG

# run maintenance scripts
if (( $REBUILD == 1 ))
then
    php /var/www/maintenance/rebuildall.php 2>> $LOG
fi

exit 0