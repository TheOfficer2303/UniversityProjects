if [ ! -d $1 ] 
    then echo 'Directory doesnt exist!'
    exit 1
elif [ ! $# -eq 2 ]
    then echo 'Wrong number of parametars'
    echo 'Usage: ./zadatak5.sh dir_name pattern'
    exit 1
fi

dir_name=$1
wildcard=$2
declare -i total=0
echo $1 $2

for file in `find "$dir_name" -name "$wildcard"`; do
    echo $file
    broj=`wc -l $file | cut -d' ' -f7`
    total+=$(($broj))
done
echo $total

#pokreni chmod u+x ime 
#pa ./zadatak5.sh . '*.sh'