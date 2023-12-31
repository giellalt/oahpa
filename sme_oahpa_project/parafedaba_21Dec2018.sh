#!/bin/sh

P="python2.7"
DATA="sme_data"
DPS="$DATA/src"
META="$DATA/meta_data"
DPN="$DATA/nob2sme"
DPF="$DATA/fin2sme"
DPE="$DATA/eng2sme"
#DPW="$DATA/swesme"
#WORDS=$GTHOME/words/dicts/smenob/src

echo "==================================================="
echo "fixing collation to utf-8"
cat fix_collation.sql | $P manage.py dbshell
echo "==================================================="
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing tags and paradigms for Morfa-C"
$P install.py -r $META/paradigms.txt -t $META/tags.txt -b 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing grammar links for norwegian"
$P install.py -i $META/grammatikklinker.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
##  sme->X
##

echo "==================================================="
echo "feeding db with $DPS/n_sme2x.xml"
$P install.py --file $DPS/n_sme2x.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $META/prop_pers_names_sme2x.xml"
$P install.py --file $DPS/prop_pers_names_sme2x.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/prop_geo_sme2x.xml"
$P install.py --file $DPS/prop_geo_sme2x.xml --tagfile $META/tags.txt --paradigmfile $META/n_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
echo "==================================================="
echo "feeding db with $DPS/npx_sme2x.xml"
$P install.py --file $DPS/npx_sme2x.xml --tagfile $META/tags.txt --paradigmfile $META/npx_paradigms.txt --append 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/num_sme2x.xml"
$P install.py --file $DPS/num_sme2x.xml --tagfile $META/tags.txt --paradigmfile $META/num_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/a_sme2x.xml"
$P install.py --file $DPS/a_sme2x.xml --tagfile $META/tags.txt --paradigmfile $META/a_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/v_sme2x.xml"
$P install.py --file $DPS/v_sme2x.xml --tagfile $META/tags.txt --paradigmfile $META/v_paradigms.txt 2>>error.log
echo " "
echo "done"
echo "==================================================="

# NOTE: --append here, so that the install only adds the forms, but doesn't delete existing ones.
echo "==================================================="
echo "feeding db with $DPS/vpass_sme2x.xml"
$P install.py --file $DPS/vpass_sme2x.xml --tagfile $META/tags.txt --paradigmfile $META/vpass_paradigms.txt --append 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $DPS/adv_sme2x.xml"
$P install.py --file $DPS/adv_sme2x.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/multiword_smenob.xml"
$P install.py --file $DPS/multiword_sme2x.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## nobsme
##

echo "==================================================="
echo "feeding db with $DPN/a_nobsme.xml"
$P install.py --file $DPN/a_nobsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/n_nobsme.xml"
$P install.py --file $DPN/n_nobsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/num_nobsme.xml"
$P install.py --file $DPN/num_nobsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/v_nobsme.xml"
$P install.py --file $DPN/v_nobsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/adv_nobsme.xml"
$P install.py --file $DPN/adv_nobsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/mwe_nobsme.xml"
$P install.py --file $DPN/mwe_nobsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPN/prop_nobsme.xml"
$P install.py --file $DPN/prop_nobsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

##
## finsme
##

echo "==================================================="
echo "feeding db with $DPF/a_finsme.xml"
$P install.py --file $DPF/a_finsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/n_finsme.xml"
$P install.py --file $DPF/n_finsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/num_finsme.xml"
$P install.py --file $DPF/num_finsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/v_finsme.xml"
$P install.py --file $DPF/v_finsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/adv_finsme.xml"
$P install.py --file $DPF/adv_finsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/mwe_finsme.xml"
$P install.py --file $DPF/mwe_finsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPF/prop_finsme.xml"
$P install.py --file $DPF/prop_finsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


##
## engsme
##

echo "==================================================="
echo "feeding db with $DPE/a_engsme.xml"
$P install.py --file $DPE/a_engsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/n_engsme.xml"
$P install.py --file $DPE/n_engsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/num_engsme.xml"
$P install.py --file $DPE/num_engsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/v_engsme.xml"
$P install.py --file $DPE/v_engsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/adv_engsme.xml"
$P install.py --file $DPE/adv_engsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/mwe_engsme.xml"
$P install.py --file $DPE/mwe_engsme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPE/prop_engsme.xml"
$P install.py --file $DPE/prop_engsme.xml 2>>error.log
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
echo "feeding db with $DPS/grammaticalwords_smenob.xml"
$P install.py --file $DPS/grammaticalwords_smenob.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/pron_sme2x.xml"
$P install.py --file $DPS/pron_sme2x.xml --tagfile $META/tags.txt  2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with $DPS/derverb_sme2x.xml"
$P install.py --file $DPS/derverb_sme2x.xml --tagfile $META/tags.txt --append  2>>error.log # TODO: test append with this
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "feeding db with $META/semantic_sets.xml"
$P install.py --sem $META/semantic_sets.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.sme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.eng.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.swe.xml 2>>error.log
echo " "
echo "done"
cho "==================================================="

echo "==================================================="
echo "feeding db with messages to feedback"
$P install.py --messagefile $META/messages.fin.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


#  ... for eastern dialect there are additional feedback files feedback_verbs_eastern, feedback_adjectives_eastern that we ignore right now

# Morfa-C


echo "==================================================="
echo "installing Morfa-C word fillings"
$P install.py -f $META/fillings_smenob.xml --paradigmfile $META/paradigms_all.txt --tagfile $META/tags.txt 2>>error.log
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

echo "==================================================="
echo "installing Morfa-C questions for verbs"
$P install.py -g $META/grammar_defaults.xml -q $META/verb_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for pronoun"
$P install.py -g $META/grammar_defaults.xml -q $META/pron_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for adjectives"
$P install.py -g $META/grammar_defaults.xml -q $META/adjective_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for numerals"
$P install.py -g $META/grammar_defaults.xml -q $META/numeral_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for derivation"
$P install.py -g $META/grammar_defaults.xml -q $META/derivation_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Morfa-C questions for noun possessive suffixes"
$P install.py -g $META/grammar_defaults.xml -q $META/px_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

###################
# Vasta and VastaS
###################
echo "==================================================="
echo "installing Vasta questions"
$P install.py -g $META/grammar_defaults.xml -q $META/vasta_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "installing Vasta-S questions"
$P install.py -g $META/grammar_defaults.xml -q $META/vastas_questions.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


echo "==================================================="
echo "Installing feedback messages for vasta"
$P install.py --messagefile $META/messages_vasta.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in English"
$P install.py --messagefile $META/messages_vasta.eng.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in Finnish"
$P install.py --messagefile $META/messages_vasta.fin.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in North Sámi"
$P install.py --messagefile $META/messages_vasta.sme.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing feedback messages for vasta - in Swedish"
$P install.py --messagefile $META/messages_vasta.swe.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Checking for differences in feedback files"
$P check_feedback.py $META/messages_vasta.xml \
    $META/messages_vasta.fin.xml \
    $META/messages_vasta.sme.xml \
    $META/messages_vasta.eng.xml \
    $META/messages_vasta.swe.xml
echo " "
echo "done"
echo "==================================================="

#####
# Sahka
#####
echo "==================================================="
echo "Installing dialogues for Sahka - firstmeeting"
$P install.py -k $META/dialogue_firstmeeting.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - hello"
$P install.py -k $META/dialogue_hello.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - car"
$P install.py -k $META/dialogue_car.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - coffee break"
$P install.py -k $META/dialogue_coffee.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - grocery shop"
$P install.py -k $META/dialogue_grocery.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - adjectives in shop"
$P install.py -k $META/dialogue_shopadj.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "Installing dialogues for Sahka - visit"
$P install.py -k $META/dialogue_visit.xml 2>>error.log
echo " "
echo "done"
echo "==================================================="


# TODO:
# fixtagattributes
# mergetags

$P manage.py fixattributes
$P manage.py mergetags
$P manage.py fixattributes

echo "==================================================="
echo "adding feedback to nouns"
$P install.py -f $DPS/n_sme2x.xml --feedbackfile $META/n_feedback.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to verbs"
$P install.py -f $DPS/v_sme2x.xml --feedbackfile $META/v_feedback.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to passive verbs"
$P install.py -f $DPS/v_sme2x.xml --feedbackfile $META/vpass_feedback.xml --append
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to adjectives"
$P install.py -f $DPS/a_sme2x.xml --feedbackfile $META/a_feedback.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to numerals"
$P install.py -f $DPS/num_sme2x.xml --feedbackfile $META/num_feedback.xml
echo " "
echo "done"
echo "==================================================="

echo "==================================================="
echo "adding feedback to possessives"
$P install.py -f $DPS/npx_sme2x.xml --feedbackfile $META/npx_feedback.xml --append
echo " "
echo "done"
echo "==================================================="

#echo "==================================================="
#echo "Optimizing tables"
#cat optimize_analyze_tables.sql | $P manage.py dbshell
#echo " "
#echo "done"
#echo "==================================================="

echo "stopped at: "
date '+%T'
