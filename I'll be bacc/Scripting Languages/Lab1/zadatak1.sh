proba='Ovo je proba'
echo $proba

lista_datoteka=*
echo $lista_datoteka

i=0
proba3=""
while [ $i -lt 3 ];
do
    proba3+="$proba. "
    i=$((i+1))
done
echo $proba3

a=4;
b=3;
c=7;
d=$(( $(($a + 4)) * $b % $c))
echo "d = $d"

broj_rijeci=`wc -w *.txt`
echo "brojRijeci = $broj_rijeci"
ls ~