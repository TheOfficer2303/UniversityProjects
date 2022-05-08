$start=0;

while (<>) {
    $file_name = $ARGV;
    ($date) = $file_name =~ /(\d{4}-\d{2}-\d{2})/;
    ($hour) = $_ =~ m/[\d]{4}:([\d]{2}):[\d]{2}:[\d]{2}/;

    if ($start == 0) {
      $start = 1;
      print "\nDatum: $date\n";
      print "sat : broj ponavljanja\n";
      print "----------------------------\n";
      $requests{$hour}++;
    } else {
      $requests{$hour}++;
    }

    if (eof) {
      foreach $time (sort keys %requests) {
        print "$time : $requests{$time}\n";
      }

      $start = 0;
      %requests = ();
    }
}

