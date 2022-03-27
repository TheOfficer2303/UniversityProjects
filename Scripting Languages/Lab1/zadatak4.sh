if [ ! -d $1 ] 
    then echo 'Directory doesnt exist!'
    exit 1
elif [ ! $# -eq 1 ]
    then echo 'Wrong number of parametars'
    echo 'Usage: ./zadatak4.sh dir_name'
    exit 1
fi

groups="$(ls $1 | grep -E -o "[[:digit:]]{6}" | uniq)"

for group in $groups; do
    year=${group:0:4}
    month=${group:3:2}
    echo "$month-$year :"
    echo "------------"
    ls $1 | grep $group | sort -k1.7,1.13
done
