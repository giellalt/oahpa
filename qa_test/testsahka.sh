# finner fram de svarene som ikke gir error-tag etter å ha kjørt qa-test_dialogue.pl på errortest-fil

cat final_data.txt | grep -v "^;" | sed 's/^$/¥/' | tr "\n" "€" | tr "¥" "\n" | egrep -v "&(grm|orth|err|sem)" | egrep '[a-zA-Z]' | tr "€" "\n" | less


