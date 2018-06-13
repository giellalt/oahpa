#!/bin/sh

P="python2.7"
DATA="sms_data"
META="$DATA/meta_data"
SMS="$DATA/src"
XXX="$DATA/*2sms"

rm -fv error.log

echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>error.log
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# for PARADGIM_FILE in $(ls $META/*_paradigms.txt)

# echo "feeding db with $DPS/N_sms2X.xml"
# $P install.py --file $DPS/N_sms2X.xml --tagfile $META/tags.txt --paradigmfile $META/$PARADGIM_FILE 2>>error.log
# echo " "
# echo "done"

# echo "==================================================="


#my_sms_oahpa>export DJANGO_SETTINGS_MODULE=my_sms_oahpa.settings

for xfile in $(ls $SMS/*.xml)
do
    fl=$(basename $xfile)
    POS=${fl%_*}
    PARA_FILE="${META}/${POS}_paradigms.txt"

    
    echo "feeding db with: $xfile"
    

    if [ -e "$PARA_FILE" ]; then
	echo "File exists $PARA_FILE"
	
	$P install.py --file $xfile --tagfile $META/tags.txt --paradigmfile $PARA_FILE 2>>error.log
	
    else 
	echo "File does not exist $PARA_FILE"
	
	$P install.py --file $xfile 2>>error.log
	
    fi 
    echo " "
    echo "done"
done

for xfile in $(ls $XXX/*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py -f $xfile 2>>error.log
  echo " "
  echo "done"
  echo "   "
done

echo "==================================================="
echo "feeding db with $META/semantic_sets.xml"
$P install.py --sem $META/semantic_sets.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="



$P manage.py mergetags
$P manage.py fixtagattributes



echo "==================================================="
echo "installing Morfa-C questions for nouns"
$P install.py -g $META/grammar_defaults.xml -q $META/noun_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "stopped at: "
date '+%T'
