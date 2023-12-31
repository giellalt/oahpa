#!/opt/local/bin/perl -w
# Perl script to test question-answers pairs for sahka and vasta

use File::Spec;
use XML::Twig;

my $infile = $ARGV[0];
my $mode = 'sahka';
if ($ARGV[1] ne "")
{
  $mode = $ARGV[1];
  print "mode is $mode\n";
}

#my $twig = XML::Twig->new(keep_encoding => 1);
my $twig = XML::Twig->new();
# to extend for vasta, too
my $s = '^'.$mode;
if (($mode eq "sahka") or ($mode eq "vastas"))
{
  $s = '^'.$mode;
} else {
  $s = '^qst';
}

#my $lon = 'lookup -flags mbTT -utf8 ~/gtsvn/gt/sme/bin/sme-norm.fst';
my $lon = 'lookup -flags mbTT -utf8 ~/errortag-gt/gt/sme/bin/ped-sme.fst';
my $tmp_file = "tmp_data.txt";
my $out_file = "final_data.txt";
my $command0 = "rm $tmp_file $out_file" ;
system ($command0) ;

$twig->parsefile($infile);
my $root = $twig->root;

foreach my $test ($root->children('test')){
  my $i =  $test->att('name');
  $i = "QDL ".$i;
  print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n";
  print "processing =>ID: $i\n";
  my $q = $test->first_child_text('q');
  foreach my $r ($test->children('a')){
    my $a = $r->text();
    print "question: $q\n";
    print "answer: $a\n";

    my $command1 = "echo '$q $s $a' | preprocess --abbr=../../gt/sme/bin/abbr.txt | $lon | lookup2cg |" ;
    open (TMPFILE, ">>$tmp_file");
    open (CMD1, $command1);
    while (<CMD1>){
      #s/^(\s+\"\^sahka\"\s+)(\?.*)$/$1$i/;
      if ($mode eq "sahka")
	{
	  s/^(\s+\"\^sahka\"\s+)(\?.*)$/$1$i/;
	}
      
      if ($mode eq "vastas")
	{
	  s/^(\s+\"\^vastas\"\s+)(\?.*)$/$1$i/;
	}

      if ($mode eq "vastaf")
	{
	  s/^(\s+\"\^qst\"\s+)(\?.*)$/$1$i/;
	}
      
      print TMPFILE;
    }
    print TMPFILE "\n\"<\.>\"\n\n";
    print "=========================================================\n";

    close CMD1;
    close (TMPFILE);     
  }
  print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n";
}

my $command2 = "cat $tmp_file | vislcg3 -g ../sme/src/sme-ped.cg3 --trace |" ;

#    print "$command2\n";

open (ENDFILE, ">>$out_file");

open (CMD2, $command2);
while (<CMD2>){
  print ENDFILE;
}
close CMD2;
close (ENDFILE);     

__END__

