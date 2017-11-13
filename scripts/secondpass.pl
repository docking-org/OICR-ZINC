#!/usr/bin/perl -w 
#secondpass.pl
while (<STDIN>) {
	my $l = $_;
	chomp $l;
	my $zincid = $l;
	$l = <STDIN>;
	my @in = split(/\t/,$l);
	my $size = $#in;
	next if $size < 10;
	next if $in[5] eq " ";
	next unless $in[8] eq "world" || $in[8] eq "fda" || $in[8] eq "investigational";
	print "$zincid\t$in[8]\t$in[5]\n";
}
