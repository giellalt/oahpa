# sh scripts/checkgrammartags.sh
# the output will be tags which are not in paradigm-files in ../meta_data
# and tags in task, but missing in tags.txt


grep grammar ../meta_data/verb_questions/* ../meta_data/noun_questions.xml ../meta_data/transl_questions.xml |cut -d '"' -f2  | sed 's/Animacy/AN/g' |sort -u > tasktags
cat ../meta_data/v_paradigms.txt ../meta_data/n_paradigms.txt ../meta_data/pron_paradigms.txt |sort > paradigmtags
cat ../meta_data/tags.txt |grep -v '#' |sort -u > taglist
cat tasktags | tr '+' '\n' | sort -u > tasklist

echo "Checking grammar strings in tasks. Problematic ones:"
comm -23 tasktags paradigmtags
echo "Checking tags in tags.txt. Problematic ones:"
comm -23 tasklist taglist
echo "Checking grammar tags. (only testing verbs and nouns)  Problematic ones:"
grep 'N+IN' tasktags | sed 's/^/mahkahk\+/' |$HLOOKUP $GTHOME/langs/crk/gtoahpa_fst/generator-gt-norm.hfst |grep '?'
grep 'N+AN' tasktags | sed 's/^/kohkôs\+/' |$HLOOKUP $GTHOME/langs/crk/gtoahpa_fst/generator-gt-norm.hfst |grep '?'
grep 'V+AI' tasktags | sed 's/^/atoskêw\+/' |$HLOOKUP $GTHOME/langs/crk/gtoahpa_fst/generator-gt-norm.hfst |grep '?'

grep 'V+II' tasktags | sed 's/^/wâpan\+/' |$HLOOKUP $GTHOME/langs/crk/gtoahpa_fst/generator-gt-norm.hfst |grep '?'
grep 'V+TI' tasktags | sed 's/^/pêtâw\+/' |$HLOOKUP $GTHOME/langs/crk/gtoahpa_fst/generator-gt-norm.hfst |grep '?'
grep 'V+TA' tasktags | sed 's/^/pêhtawêw\+/' |$HLOOKUP $GTHOME/langs/crk/gtoahpa_fst/generator-gt-norm.hfst |grep '?'

rm tasktags paradigmtags tasklist taglist
