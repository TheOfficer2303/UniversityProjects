$start=0;
$file_name = $ARGV;

print "\nDatum: $datum\n";
  print "sat : broj ponavljanja\n";
  print "----------------------------\n";

while (<>) {
    ($date) = $file_name =~ /(\d{4}-\d{2}-\d{2})/;
    ($hour) = $_ =~ m/[\d]{4}:([\d]{2}):[\d]{2}:[\d]{2}/;

    $requests{$hour}++;
}

foreach $time (sort keys %requests) {
    print "$time : $requests{$time}\n";
}