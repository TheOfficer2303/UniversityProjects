print "Unesi niz\n";
chomp($niz = <STDIN>);
print "Unesi broj\n";
chomp($broj = <STDIN>);

$niz = "$niz\n" x $broj;
print $niz;