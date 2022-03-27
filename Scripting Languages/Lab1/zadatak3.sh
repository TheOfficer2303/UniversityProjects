if [ ! -d $1 ] 
    then echo 'Directory doesnt exist!'
    exit 1
elif [ ! $# -eq 1 ]
    then echo 'Wrong number of parametars'
    echo 'Usage: ./zadatak3.sh dir_name'
    exit 1
fi

for file in $(ls localhost_access_log.[0-9][0-9][0-9][0-9]-02-*) ; do
    echo $file | sed -r 's/.*\.([0-9]{4})-([0-9]{2})-([0-9]{2}).*/datum: \3-\2-\1/'
    echo '---------------------------------------'

    #cut s delimiterom ", uzimamo 2. field jer je tamo request koji nam treba za analizu
    #prvo sortiranje da bi brojanje istih uzastopnih redova radilo
    #drugo sortiranje obrnutim poretkom 
    cat $file | cut -d'"' -f 2 | sort | uniq -c | sort -rn
done