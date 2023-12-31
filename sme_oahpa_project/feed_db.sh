#!/bin/sh

# run the script:
# sh feed_db.sh sme (= LLL1)

P="python"
LLL1=$1
log_file="db_install_error.log"
DATA="${LLL1}_data"
META="$DATA/meta_data"
SRC="$DATA/src"
XXX="$DATA/*2${LLL1}"

# perhaps an error file per task would be
# better (install sme2x, install x2sme, install messages, etc.)
rm -fv $log_file

# echo "==================================================="
# echo "fixing collation to utf-8"
# cat fix_collation.sql | $P manage.py dbshell
# echo "==================================================="
# echo " "
# echo "done"
# echo "==================================================="


echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>$log_file
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "installing grammar links for norwegian"
$P install.py -i $META/grammatikklinker.txt 2>>$log_file
echo " "
echo "done"
echo "==================================================="

##
##  sme->X
##

for xfile in $(ls $SRC/*.xml)
do
    fl=$(basename $xfile)
    # the first substring before the first '_' in the xml file name is the POS ('prop' for both pers and geo)
    POS=${fl%%_*}
    PARA_FILE="${META}/${POS}_paradigms.txt"
    echo "feeding db with $xfile: pos $POS"
    if [ "$fl" != "derverb_sme2x.xml" ] && [ "$fl" != "pron_sme2x.xml" ] && [ "$fl" != "npx_sme2x.xml" ]  && [ "$fl" != "vpass_sme2x.xml" ] ; then

	if [ -e "$PARA_FILE" ]; then
	    echo "... both w paradime and w tags"
	    $P install.py --file $xfile --tagfile $META/tags.txt --paradigmfile $PARA_FILE 2>>$log_file
	else
	    echo "... both w/o paradime and w/o tags"
	    $P install.py --file $xfile 2>>$log_file
	fi
    # special treatment
    elif [ "$fl" == "derverb_sme2x.xml" ] ; then
    	echo "... append w tags but w/o paradime: append derverb_"
	# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
    	$P install.py --file $xfile --tagfile $META/tags.txt --append  2>>$log_file
    elif [ "$fl" == "npx_sme2x.xml" ] || [ "$fl" == "vpass_sme2x.xml" ] ; then
	# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
    	echo "... append both w tags and w paradime: append npx_ or vpass_"
    	$P install.py --file $xfile --tagfile $META/tags.txt  --paradigmfile $PARA_FILE --append  2>>$log_file
    elif [ "$fl" == "pron_sme2x.xml" ] ; then
    	echo "... w tags but w/o paradime: pron_"
    	$P install.py --file $xfile --tagfile $META/tags.txt 2>>$log_file
    fi
    echo "done"
    echo " "
done



##
## xxx2sme/*.xml
##

for xfile in $(ls $XXX/*.xml)
do
  echo "feeding db with: $xfile"
  $P install.py --file $xfile 2>>$log_file
  echo " "
  echo "done"
  echo "   "
done


echo "==================================================="
echo "feeding db with $META/semantic_sets.xml"
$P install.py --sem $META/semantic_sets.xml 2>>$log_file
echo " "
echo "done"
echo "==================================================="

MESSAGE_FILES="messages.xml
messages.sme.xml
messages.eng.xml
messages.swe.xml
messages.fin.xml"

for mf in $MESSAGE_FILES
do
    echo "==================================================="
    echo "messages to feedback: $META/$mf"
    $P install.py --messagefile $META/$mf 2>>$log_file
    echo " "
    echo "done"
    echo "==================================================="
done

#  ... for eastern dialect there are additional feedback files feedback_verbs_eastern,
# feedback_adjectives_eastern that we ignore right now

echo "==================================================="
echo "installing Morfa-C word fillings"
$P install.py -f $META/fillings_smenob.xml --paradigmfile $META/paradigms_all.txt --tagfile $META/tags.txt 2>>$log_file
echo " "
echo "done"
echo "==================================================="

$P manage.py mergetags
$P manage.py fixtagattributes


# installing question files for MorfaC, Vasta and VastaS
question_files=$(ls $META/*_questions.xml)

# adjective_questions.xml
# derivation_questions.xml
# noun_questions.xml
# numeral_questions.xml
# pron_questions.xml
# pron_reflexive_questions.xml ==> not installed in the older version of the script: why?
# px_questions.xml
# vasta_questions.xml
# vastas_questions.xml
# verb_questions.xml

for q_file in $question_files
do
    echo "installing questions: $q_file"
    $P install.py -g $META/grammar_defaults.xml -q $q_file 2>>$log_file
    echo "done"
    echo "   "
done

# installing message files for Vasta
vasta_message_files=$(ls $META/messages_vasta*.xml)

for mv_file in $vasta_message_files
do
    echo "installing vasta messages: $mv_file"
    $P install.py --messagefile $mv_file 2>>$log_file
    echo "done"
    echo "   "
done

echo "==================================================="
echo "Checking for differences in feedback files"
$P check_feedback.py $vasta_message_files
echo " "
echo "done"
echo "==================================================="



### below this line no abstraction: TODO

#####
# Sahka
#####

# installing dialogue files for Sahka
sahka_dialogue_files=$(ls $META/dialogue_*.xml)

# dialogue_car.xml
# dialogue_coffee.xml
# dialogue_firstmeeting.xml
# dialogue_firstmeeting_boy.xml ==> not installed in the older version of the script: why?
# dialogue_firstmeeting_girl.xml ==> not installed in the older version of the script: why?
# dialogue_firstmeeting_man.xml ==> not installed in the older version of the script: why?
# dialogue_grocery.xml
# dialogue_hello.xml
# dialogue_shopadj.xml
# dialogue_visit.xml

for sd_file in $sahka_dialogue_files
do
    echo "installing sahka dialogue: $sd_file"
    $P install.py -k $sd_file 2>>$log_file
    echo "done"
    echo "   "
done

# @cip 20181130: why todo?
# TODO:
# fixtagattributes
# mergetags

$P manage.py fixattributes
$P manage.py mergetags
$P manage.py fixattributes

FB_FILE_PREFIX="n
v
a
num"

for fbfp in $FB_FILE_PREFIX
do
    echo "==================================================="
    echo "adding feedback to: $fbfp"
    $P install.py -f $SRC/${fbfp}_sme2x.xml --feedbackfile $META/${fbfp}_feedback.xml
    echo " "
    echo "done"
    echo "==================================================="
done

# appending the passive verbs to the already installed ones
echo "adding feedback to passive verbs"
$P install.py -f $SRC/v_sme2x.xml --feedbackfile $META/vpass_feedback.xml --append
echo "adding feedback to possessives"
$P install.py -f $SRC/npx_sme2x.xml --feedbackfile $META/npx_feedback.xml --append

# ... for eastern dialect there are additional feedback files feedback_verbs_eastern, feedback_adjectives_eastern that we ignore right now

#echo "==================================================="
#echo "Optimizing tables"
#cat optimize_analyze_tables.sql | $P manage.py dbshell
#echo " "
#echo "done"
#echo "==================================================="

echo "stopped at: "
date '+%T'
