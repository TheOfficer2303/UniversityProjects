if [ ! -d $1 ] 
    then echo 'Directory doesnt exist!'
    exit 1
elif [ ! $# -eq 1 ]
    then echo 'Wrong number of parametars'
    echo 'Usage: ./zadatak4.sh dir_name'
    exit 1
fi

groups="$(ls $1 | grep -E -o "[[:digit:]]{6}" | uniq)"
echo $groups

for group in $groups; do
    year=${group:0:4}
    month=${group:4:2}
    echo "$month-$year :"
    echo "------------"
    ls $1 | grep $group | sort
    count=`ls $1 | grep $group | wc -l | cut -d' ' -f8`
    echo "--- Ukupno: $count slika ---"
    echo
done
