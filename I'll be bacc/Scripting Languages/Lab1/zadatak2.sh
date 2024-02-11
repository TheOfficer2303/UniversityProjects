grep -i -E 'dinja|lubenica|banana|jabuka|jagoda' namirnice.txt

grep -i -E -v 'dinja|lubenica' namirnice.txt #-v je negacija

grep -r -E '(^| )[A-Z]{3}[0-9]{6} ' ~/projekti/ #sifra se nalazi ili na pocetku reda ili je odvojena razmakom od drugih rijeci

find . -mtime +7 -mtime -14 -ls

for i in {1..15}; do echo $i; done

for i in {1..15}; do if [ $i -eq 15 ]; then kraj=$i; echo $kraj; fi; echo $i; done