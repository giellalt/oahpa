#!/bin/sh

P="python2.6"
DATA="data_sme/"
DPS="data_sme/sme"
META="data_sme/meta"
DPN="data_sme/nob"
DPF="data_sme/fin"
DPW="data_sme/swe"
SRC="ped/sme/univ_oahpa_data/data_sme"
SP=$GTHOME/$SRC
WORDS=$GTHOME/words/dicts/smenob/src

##
##  sme->X
##

echo "==================================================="
echo "feeding db with $DPS/n_smenob.xml"
$P install.py --file $DPS/n_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>error.log
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with $META/names.xml" - does not exist for sme
#$P install.py --file $META/names.xml --tagfile $META/tags.txt --paradigmfile $META/prop_paradigms.txt 2>>error.log
#echo " "
#echo "done"
#echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/prop_smenob.xml"
$P install.py --file $DPS/prop_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/prop_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/prop_smenob.xml"
$P install.py --file $DPS/propPl_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/prop_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/num_smenob.xml"
$P install.py --file $META/num_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/a_smenob.xml"
$P install.py --file $DPS/a_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/a_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/v_smenob.xml"
$P install.py --file $DPS/v_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/v_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/adv_smenob.xml"
$P install.py --file $DPS/adv_smenob.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/multiword_smenob.xml"
$P install.py --file $DPS/multiword_smenob.xml
echo " "
echo "done"
echo "==================================================="

##
## nobsme
##

echo "==================================================="
echo "feeding db with $DPN/a_nobsme.xml"
$P install.py --file $DPN/a_nobsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/n_nobsme.xml"
$P install.py --file $DPN/n_nobsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/num_nobsme.xml"
$P install.py --file $DPN/num_nobsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/v_nobsme.xml"
$P install.py --file $DPN/v_nobsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/adv_nobsme.xml"
$P install.py --file $DPN/adv_nobsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/mwe_nobsme.xml"
$P install.py --file $DPN/mwe_nobsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/prop_nobsme.xml"
$P install.py --file $DPN/prop_nobsme.xml
echo " "
echo "done"
echo "==================================================="

##
## finsme
##

echo "==================================================="
echo "feeding db with $DPF/a_finsme.xml"
$P install.py --file $DPF/a_finsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/n_finsme.xml"
$P install.py --file $DPF/n_finsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/num_finsme.xml"
$P install.py --file $DPF/num_finsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/v_finsme.xml"
$P install.py --file $DPF/v_finsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/adv_finsme.xml"
$P install.py --file $DPF/adv_finsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/mwe_finsme.xml"
$P install.py --file $DPF/mwe_finsme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/prop_finsme.xml"
$P install.py --file $DPF/prop_finsme.xml
echo " "
echo "done"
echo "==================================================="

##
## swesme - has not been created for the new format yet
##
: <<'COMMENT'

echo "==================================================="
echo "feeding db with $DPW/a_swesme.xml"
$P install.py --file $DPW/a_swesme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/n_swesme.xml"
$P install.py --file $DPW/n_swesme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/v_swesme.xml"
$P install.py --file $DPW/v_swesme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/adv_swesme.xml"
$P install.py --file $DPW/adv_swesme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/multiword_swesme.xml"
$P install.py --file $DPW/multiword_swesme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPW/prop_swesme.xml"
$P install.py --file $DPW/prop_swesme.xml
echo " "
echo "done"
echo "===================================================
COMMENT

echo "==================================================="
echo "feeding db with data_sma/sma/pronPers_smanob.xml"
$P install.py --file /home/smaoahpa/smaoahpa/data_sma/sma/pronPers_smanob.xml --tagfile /home/smaoahpa/smaoahpa/data_sma/meta/tags.txt --paradigmfile /home/smaoahpa/smaoahpa/data_sma/meta/pron_paradigms.txt 
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $META/semantical_sets.xml"
$P install.py --sem $META/semantical_sets.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.sme.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.eng.xml
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "feeding db with messages to feedback"
#$P install.py --messagefile $META/messages.swe.xml
#echo " "
#echo "done"
#echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.fin.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to nouns"
$P install.py -f $DPS/n_smenob.xml --feedbackfile $META/feedback_nouns.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to verbs"
$P install.py -f $DPS/v_smenob.xml --feedbackfile $META/feedback_verbs.xml
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "adding feedback to nouns"
$P install.py -f $DPS/a_smenob.xml --feedbackfile $META/feedback_adjectives.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to nouns"
$P install.py -f $DPS/num_smenob.xml --feedbackfile $META/feedback_numerals.xml
echo " "
echo "done"
echo "==================================================="

#  ... for eastern dialect there are additional feedback files feedback_verbs_eastern, feedback_adjectives_eastern that we ignore right now

# Morfa-C 

echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C word fillings"
$P install.py -f $META/fillings_smenob.xml --paradigmfile $META/paradigms.txt --tagfile $META/tags.txt
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for nouns"
$P install.py -g $META/grammar_defaults.xml -q $META/noun_questions.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for verbs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions.xml
echo " "
echo "done"
echo "==================================================="
: <<'COMMENT'
echo "==================================================="
echo "installing Morfa-C questions for verbs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_problems.xml
echo " "
echo "done"
echo "==================================================="

# echo "==================================================="
# echo "installing Morfa-C questions for verbs"
# $P install.py -g $META/grammar_defaults.xml -q $META/more_verb_questions.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "installing Morfa-C questions for verbs"
# $P install.py -g $META/grammar_defaults.xml -q $META/imprt_questions.xml
# echo " "
# echo "done"
# echo "==================================================="
echo "==================================================="
echo "installing Morfa-C questions for pronoun"
$P install.py -g $META/grammar_defaults.xml -q $META/pron_questions.xml
echo " "
echo "done"
echo "==================================================="

COMMENT

echo "==================================================="
echo "installing Morfa-C questions for adjectives"
$P install.py -g $META/grammar_defaults.xml -q $META/adjective_questions.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing grammar links for norwegian"
$P install.py -i $META/grammatikklinker.txt
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Optimizing tables"
cat optimize_analyze_tables.sql | $P manage.py dbshell
echo " "
echo "done"
echo "==================================================="

