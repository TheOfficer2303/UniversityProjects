$first_line = 0;
while(<>) {
    if ($_ =~ m/^#/) {
        next;
    }
    if ($first_line == 0) {
        @shares = split /;/;
        $first_line = 1;
    } else {
        @info = split /;/;
        $jmbag = $info[0];
        $last_name = $info[1];
        $first_name = $info[2];

        for(my $i = 3; $i <= 9; $i++){
            if ($info[$i] eq '-') {
                next;
            }
	        $sum += $info[$i] * $shares[$i - 3];
        }

        $key = join(' ', "$last_name,", "$first_name", "($jmbag)");
        $scores{$key} = $sum;
        $sum = 0;
    }
}

print "Lista po rangu:\n";
print "----------------------------\n";
for my $jmbag ( reverse sort { $scores{$a} <=> $scores{$b} } keys %scores ) {
    print "  $jmbag : " . $scores{$jmbag} . "\n";
}
