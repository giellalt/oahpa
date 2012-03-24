#!/bin/sh

P="python2.7"
GTHOME="/home/ryan/gtsvn"
LANGDIR="ped/sme"
DATA=$GTHOME/$LANGDIR
DPS="$DATA/src"
META="$DATA/meta"
DPN="$DATA/nobsme"
DPF="$DATA/finsme"
#DPW="$DATA/swesme"
#WORDS=$GTHOME/words/dicts/smenob/src

##
##  sme->X
##

echo "==================================================="
echo "feeding db with $DPS/n_smenob.xml"
$P install.py --file $DPS/n_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $META/names.xml"
$P install.py --file $DPS/names.xml --tagfile $META/tags.txt --paradigmfile $META/prop_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/prop_smenob.xml"
$P install.py --file $DPS/prop_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/prop_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $DPS/num_smenob.xml"
$P install.py --file $DPS/num_smenob.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
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
COMMENT
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

# echo "==================================================="
# echo "feeding db with $DPW/a_swesme.xml"
# $P install.py --file $DPW/a_swesme.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/n_swesme.xml"
# $P install.py --file $DPW/n_swesme.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/v_swesme.xml"
# $P install.py --file $DPW/v_swesme.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/adv_swesme.xml"
# $P install.py --file $DPW/adv_swesme.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/multiword_swesme.xml"
# $P install.py --file $DPW/multiword_swesme.xml
# echo " "
# echo "done"
# echo "==================================================="

# echo "==================================================="
# echo "feeding db with $DPW/prop_swesme.xml"
# $P install.py --file $DPW/prop_swesme.xml
# echo " "
# echo "done"
# echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/pron_sme.xml"
$P install.py --file $DPS/pron_sme.xml --tagfile $META/tags.txt 
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/pron_sme.xml"
$P install.py --file $DPS/derverb_sme.xml --tagfile $META/tags.txt 
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

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.swe.xml
echo " "
echo "done"
cho "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.fin.xml
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

echo "==================================================="
echo "installing Morfa-C questions for pronoun"
$P install.py -g $META/grammar_defaults.xml -q $META/pron_questions.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for adjectives"
$P install.py -g $META/grammar_defaults.xml -q $META/adjective_questions.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for numerals"
$P install.py -g $META/grammar_defaults.xml -q $META/numeral_questions.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing grammar links for norwegian"
$P install.py -i $META/grammatikklinker.txt
echo " "
echo "done"
echo "==================================================="

#######
# Vasta
#######
echo "==================================================="
echo "installing Vasta questions"
$P install.py -g $META/grammar_defaults.xml -q $META/questions_vasta.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Vasta-S questions"
$P install.py -g $META/grammar_defaults.xml -q $META/vastas_questions.xml
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "Installing feedback messages for vasta"
$P install.py --messagefile $META/messages_vasta.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in English"
$P install.py --messagefile $META/messages_vasta.eng.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in Finnish"
$P install.py --messagefile $META/messages_vasta.fin.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in North Sámi"
$P install.py --messagefile $META/messages_vasta.sme.xml
echo " "
echo "done"
echo "==================================================="

#####
# Sahka
#####
echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting"
$P install.py -k $META/dialogue_firstmeeting.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting - boy"
$P install.py -k $META/dialogue_firstmeeting_boy.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting - girl"
$P install.py -k $META/dialogue_firstmeeting_girl.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting - man"
$P install.py -k $META/dialogue_firstmeeting_man.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - grocery shop"
$P install.py -k $META/dialogue_grocery.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - adjectives in shop"
$P install.py -k $META/dialogue_shopadj.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - visit"
$P install.py -k $META/dialogue_visit.xml
echo " "
echo "done"
echo "==================================================="

# TODO: 
# fixtagattributes
# mergetags
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
echo "adding feedback to adjectives"
$P install.py -f $DPS/a_smenob.xml --feedbackfile $META/feedback_adjectives.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to numerals"
$P install.py -f $DPS/num_smenob.xml --feedbackfile $META/feedback_numerals.xml
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "Optimizing tables"
#cat optimize_analyze_tables.sql | $P manage.py dbshell
#echo " "
#echo "done"
#echo "==================================================="

