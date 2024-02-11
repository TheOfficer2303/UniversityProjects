while(<>) {
    @info = split /;/;

    $jmbag = $info[0];
    $last_name = $info[1];
    $first_name = $info[2];

    @termin = split /\s/, $info[3];
    @locked = split /\s/, $info[4];

    @termin_end = split /:/, $termin[1];
    @locked_end = split /:/, $locked[1];


    if ($termin[0] ne $locked[0] || ($locked_end[0] - $termin_end[0] > 0)) {
        print "Problem: $jmbag $last_name $first_name\n";
    }
}
