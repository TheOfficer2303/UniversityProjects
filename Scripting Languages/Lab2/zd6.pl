# use open ':locale';
# use locale;

$n = pop(@ARGV);

while (<>) {
        chomp;
        tr/A-Z/a-z/;
        $line = $_;
        @a = ($line =~ m/\b(\w{$n})/g);

        foreach $word (@a) {
                $a{$word} += 1;
        }
}

@sorted_map = (sort keys %a);

foreach $key (@sorted_map) {
        print "$key : $a{$key}" . "\n";
}