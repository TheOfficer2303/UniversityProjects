if [ ! -d $1 -o ! -d $2 ] 
    then echo 'One of the directories do not exist'
    exit 1
elif [ ! $# -eq 2 ]
    then echo 'Wrong number of parametars'
    echo 'Usage: ./zadatak6.sh dir_name1 dir_name2'
    exit 1
fi

dir_name1=$1
dir_name2=$2

for file in `ls "$dir_name1"`; do
    if [ ! -f "$dir_name2/$file" ]
        then  echo "$dir_name1/$file --> $dir_name2"
    elif [ "$dir_name1/$file" -nt "$dir_name2/$file" ]
        then echo "$dir_name1/$file --> $dir_name2"
    fi
done

for file in `ls "$dir_name2"`; do
    if [ ! -f "$dir_name1/$file" ]
        then  echo "$dir_name2/$file --> $dir_name1"
    elif [ "$dir_name2/$file" -nt "$dir_name1/$file" ]
        then echo "$dir_name2/$file --> $dir_name1"
    fi
done