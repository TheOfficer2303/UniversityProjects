chomp(@nums = <STDIN>);
foreach $num (@nums) {
    $sum += $num;
}
$size = @nums;
print "Mean: " . $sum/$size . "\n";