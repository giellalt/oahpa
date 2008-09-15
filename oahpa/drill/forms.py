# -*- coding: utf-8 -*-
import string
import sys
from django import newforms as forms
from django.http import Http404
from django.db.models import Q
from django.utils.translation import ugettext as _
from random import randint
from models import *


POS_CHOICES = (
    ('N', _('noun')),
    ('V', _('verb')),
    ('A', _('adjective')),
    ('Num', _('numeral')),
)

CASE_CHOICES = (
    ('N-ACC', _('accusative')),
    ('N-ILL', _('illative')),
    ('N-LOC', _('locative')),
    ('N-COM', _('comitative')),
    ('N-GEN', _('genitive')),
    ('N-ESS', _('essive')),
)

VTYPE_CHOICES = (
    ('MAINV', _('tense')),
    ('V-COND', _('conditional')),
    ('V-IMPRT', _('imperative')),
    ('V-GO', _('go-questions')),
)

NUM_CONTEXT_CHOICES = (
    ('NUM-ATTR', _('attributive')),
    ('COLL-NUM', _('collective')),
)


VTYPE_BARE_CHOICES = (
    ('PRS', _('present')),
    ('PRT', _('past')),
   ('COND', _('conditional')),
    ('IMPRT', _('imperative')),
    ('POT', _('potential')),
)



BOOK_CHOICES = (
    ('d1', _('Davvin 1')),
    ('d2', _('Davvin 1-2')),
    ('d3', _('Davvin 1-3')),
    ('d4', _('Davvin 1-4')),
    ('algu', _('algu')),
    ('sara', _('sara')),
    ('bures', _('Bures bures fas')),
    ('oaidnalit', _('Oaidnalit')),
    ('all', _('All')),
)

GAME_CHOICES = (
    ('bare', _('bare')),
    ('context', _('context')),
)

TRANS_CHOICES = (
    ('smenob', _('North Sami to Norwegian')),
    ('nobsme', _('Norwegian to North Sami')),
)

LANGUAGE_CHOICES = (
    ('sme', _('North Sami')),
    ('smj', _('Lule Sami')),
    ('sma', _('South Sami')),
    ('smn', _('Inari Sami')),
)

SEMTYPE_CHOICES = (
    ('FAMILY', _('family')),
    ('PROFESSION', _('profession')),
    ('HUMAN-LIKE', _('human-like')),
    ('ANIMAL', _('animal')),
    ('FOOD/DRINK', _('food/drink')),
    ('TIME', _('time')),
    ('CONCRETES', _('concretes')),
    ('BODY', _('body')),
    ('CLOTHES', _('clothes')),
    ('BUILDINGS/ROOMS', _('buildings/rooms')),
    ('NATUREWORDS', _('naturewords')),
    ('LEISURETIME/AT_HOME', _('leisuretime/at_home')),
    ('PLACES', _('places')),
    ('LITERATURE', _('literature')),
    ('SCHOOL/EDUCATION', _('school/education')),
    ('ABSTRACTS', _('abstracts')),
    ('WORK/ECONOMY/TOOLS', _('work/economy/tools')),
    ('all', _('all')),
)

NUM_CHOICES = (
    ('10', _('0-10')),
    ('20', _('0-20')),
    ('100', _('0-100')),
    ('1000', _('0-1000')),
#    ('ALL', _('all')),
)

NUMGAME_CHOICES = (
    ('numeral', _('Numeral to string')),
    ('string', _('String to numeral')),
)



def is_correct(self):
    """
    Determines if the given answer is correct (for a bound form).
    """
    if not self.is_valid():
        return False

    self.userans = self.cleaned_data['answer']
    answer = self.userans.rstrip()
    answer = answer.lstrip()
    answer = answer.rstrip('.!?,')
    
    self.error = "error"

    #print "ANSWER", answer
    if answer in set(self.correct_anslist) or \
           answer.lower() in set(self.correct_anslist) or \
           answer.upper() in set(self.correct_anslist):
        self.error = "correct"

def set_correct(self):
    """
    Adds correct wordforms to the question form.
    """
    for e in self.correct_anslist:
        self.correct_answers += " "+e

def set_settings(self):

    # Construct arrays for book choices.
    self.books = {}
    self.books['all'] = []
    for b in BOOK_CHOICES:
        if b[0] != 'all':
            self.books[b[0]] = []
            self.books['all'].append(b[0])

        self.books[b[0]].append(b[0])

        
    self.books['d2'].append('d1')
    for b in ['d1', 'd2']:
        self.books['d3'].append(b)
    for b in ['d1', 'd2', 'd3']:
        self.books['d4'].append(b)

    self.allsem = []
    for b in SEMTYPE_CHOICES:
        self.allsem.append(b[0])        
        
    self.allcase = []
    for b in CASE_CHOICES:
        self.allcase.append(b[0])                

            
class MorphForm(forms.Form):

    set_settings = set_settings

    num_context = forms.ChoiceField(initial='NUM-ATTR', choices=NUM_CONTEXT_CHOICES, widget=forms.Select)
    case = forms.ChoiceField(initial='N-ILL', choices=CASE_CHOICES, widget=forms.Select)
    vtype = forms.ChoiceField(initial='MAINV', choices=VTYPE_CHOICES, widget=forms.Select)
    vtype_bare = forms.ChoiceField(initial='PRS', choices=VTYPE_BARE_CHOICES, widget=forms.Select)
    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    gametype = forms.ChoiceField(initial='bare', choices=GAME_CHOICES, widget=forms.Select)
    bisyllabic = forms.BooleanField(required=False, initial='1')
    trisyllabic = forms.BooleanField(required=False,initial='1')
    contracted = forms.BooleanField(required=False,initial='1')
    default_data = {'pos': 'N'}

    def __init__(self, *args, **kwargs):
        self.set_settings()
        super(MorphForm, self).__init__(*args, **kwargs)
        
class MorphQuestion(forms.Form):
    """
    Questions for morphology game 
    """
    is_correct = is_correct
    set_correct = set_correct
    
    answer = forms.CharField()

    def get_feedback(self,word,tag):
        
        feedbacks=None
        
        if tag.pos=="N":
            print "filtering feedbacks"
            print "stem:", word.stem, "gradation:", word.gradation, "diphthong:", word.diphthong, "rime:", word.rime, "soggi:", word.soggi,tag.case,tag.pos,tag.number
            feedbacks = Feedback.objects.filter(Q(stem=word.stem) & Q(gradation=word.gradation) & \
                                                Q(diphthong=word.diphthong) & Q(rime=word.rime) & \
                                                Q(soggi=word.soggi) & Q(case=tag.case) & \
                                                Q(pos=tag.pos) &\
                                                Q(number = tag.number))
        if tag.pos=="A":
            grade =""
            if tag.grade:
                grade = tag.grade
            else:
                if tag.attributive == "Attr":
                    grade = "Attr"
                else:
                    grade = "Pos"
            feedbacks = Feedback.objects.filter(Q(stem=word.stem) & Q(gradation=word.gradation) & \
                                                Q(diphthong=word.diphthong) & Q(rime=word.rime) & \
                                                Q(soggi=word.soggi) & Q(case=tag.case) & \
                                                Q(pos=tag.pos) & Q(grade=grade) &\
                                                Q(number = tag.number))

        if tag.pos == "V":
            feedbacks = Feedback.objects.filter(Q(stem=word.stem) & Q(gradation=word.gradation) & \
                                               Q(diphthong=word.diphthong) & Q(soggi=word.soggi) & \
                                               Q(mood=tag.mood) & Q(tense=tag.tense) & \
                                               Q(personnumber = tag.personnumber))
            
        if feedbacks:
            for f in feedbacks:
                msgs = f.messages.all()
                for m in msgs:
                    self.feedback = self.feedback + " " + m.message
            self.feedback = self.feedback.replace("LEMMA", "\"" + word.lemma + "\"") 
            print self.feedback


    def __init__(self, word, tag, fullforms, translations, question, userans_val, correct_val, *args, **kwargs):

        lemma_widget = forms.HiddenInput(attrs={'value' : word.id})
        tag_widget = forms.HiddenInput(attrs={'value' : tag.id})

        super(MorphQuestion, self).__init__(*args, **kwargs)
        self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
        self.fields['tag_id'] = forms.CharField(widget=tag_widget, required=False)
        self.lemma=word.lemma

        # Get lemma and feedback
        self.feedback=""
        messages = []
        if tag.pos=="N" or tag.pos=="A":
            If tag.number=="Sg":
                self.lemma = word.lemma
            else:
                tagstring = tag.pos + "+Pl+Nom"
                self.lemma = Form.objects.filter(Q(word__pk=word.id) & Q(tag__string=tagstring))[0].fullform

        # Retrieve feedback information
        self.get_feedback(word,tag)
            
        self.correct_answers =""
        self.case = ""
        self.userans = userans_val
        self.correct_anslist = []
        self.error="empty"
        self.problems="error"
        self.pron=""
        self.PronPNBase={'Sg1':'mun','Sg2':'don','Sg3':'son',\
                         'Pl1':'mun','Pl2':'don','Pl3':'son',\
                         'Du1':'mun','Du2':'don','Du3':'son'}
        
        tmp_translations = []
        for item in translations:
            tmp_translations.append(item.lemma.encode('utf-8'))
        self.translations = string.join(tmp_translations, ', ' )
        
        for item in fullforms:
            self.correct_anslist.append(item.fullform)
        
        if tag.pos=="N":
            self.tag = ""
            self.case = tag.case
        if tag.pos=="V":
            self.tag = ""
        else:
            self.tag = tag.string

        if tag.pos=="V" and tag.personnumber and not tag.personnumber == "ConNeg" :
            pronbase = self.PronPNBase[tag.personnumber]
            self.pron = Form.objects.filter(Q(word__lemma=pronbase) & \
                                            Q(tag__string="Pron+Pers+" +tag.personnumber+ "+Nom"))[0].fullform

            print self.pron

        self.is_correct()

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"


class QuizzForm(forms.Form):

    set_settings = set_settings

    semtype = forms.ChoiceField(initial='all', choices=SEMTYPE_CHOICES, widget=forms.Select)
    transtype = forms.ChoiceField(initial='smenob', choices=TRANS_CHOICES, widget=forms.Select)
    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        self.set_settings()
        super(QuizzForm, self).__init__(*args, **kwargs)


class QuizzQuestion(forms.Form):
    """
    Questions for word quizz
    """
    answer = forms.CharField()

    is_correct = is_correct
    set_correct = set_correct
    
    def __init__(self, transtype, word, translations, question, userans_val, correct_val, *args, **kwargs):

        lemma_widget = forms.HiddenInput(attrs={'value' : word.id})
        super(QuizzQuestion, self).__init__(*args, **kwargs)
        self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
        self.lemma = word.lemma
        self.userans = userans_val
        self.correct_anslist = []
        self.correct_answers =""
        self.error="empty"
        self.problems="error"
        oo = "å "
        
        if word.pos == 'V' and transtype=="nobsme":
            self.lemma = oo.decode('utf-8') + self.lemma
            
        for item in translations:
            self.correct_anslist.append(item.lemma)

        self.is_correct()

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"

class NumForm(forms.Form):

    set_settings = set_settings

    maxnum = forms.ChoiceField(initial='10', choices=NUM_CHOICES, widget=forms.RadioSelect)
    numgame = forms.ChoiceField(initial='numeral', choices=NUMGAME_CHOICES, widget=forms.RadioSelect)
    language = forms.ChoiceField(initial='sme', choices=LANGUAGE_CHOICES, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        self.set_settings
        super(NumForm, self).__init__(*args, **kwargs)

class NumQuestion(forms.Form):
    """
    Questions for numeral quizz
    """
    answer = forms.CharField()

    is_correct = is_correct
    set_correct = set_correct
    
    def __init__(self, numeral, num_string, num_list, gametype, userans_val, correct_val, *args, **kwargs):

        numeral_widget = forms.HiddenInput(attrs={'value' : numeral})
        super(NumQuestion, self).__init__(*args, **kwargs)
        self.fields['numeral_id'] = forms.CharField(widget=numeral_widget, required=False)
        if gametype == "string":
            self.numstring = num_string
        self.numeral = numeral
        self.userans = userans_val
        self.correct_anslist = []
        self.correct_answers =""
        self.error="empty"
        self.problems="error"

        if gametype == "string":
            self.correct_anslist.append(numeral)
        else:
            for item in num_list:
                self.correct_anslist.append(item)
                
        self.is_correct()

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"


def select_words(self, qwords, awords):
    """
    Fetch words and tags from the database.
    """

    selected_awords = {}

    for syntax in awords.keys():
        print "SYNTAX", syntax
        word = None        
        tag = None
        selected_awords[syntax] = {}

        # Select answer words and fullforms for interface
        # Use first the answer elements, but if there are none,
        # take the corresponding question element        
        if awords.has_key(syntax) and len(awords[syntax]) > 0:
            aword = awords[syntax][randint(0,len(awords[syntax])-1)]
            if aword.has_key('tag'):
                selected_awords[syntax]['tag'] = aword['tag']
            if aword.has_key('word') and aword['word']:
                selected_awords[syntax]['word'] = aword['word']
            else:
                if aword.has_key('qelement') and selected_awords[syntax].has_key('tag'):

                    form_list = None
                    max=50
                    i=0
                    while not form_list and i<max:
                        i=i+1
                        word_count = WordQElement.objects.filter(qelement__id=aword['qelement']).count()
                        wqel = WordQElement.objects.filter(qelement__id=aword['qelement'])[randint(0,word_count-1)]
                        selected_awords[syntax]['word'] = wqel.word.id
                        form_list = Form.objects.filter(Q(word__id=selected_awords[syntax]['word']) &\
                                                        Q(tag__id=selected_awords[syntax]['tag']))
                    if form_list:
                        fullf=[]
                        for f in form_list:
                            fullf.append(f.fullform)
                        selected_awords[syntax]['fullform'] = fullf[:]

                else:
                    if aword.has_key('fullform') and len(aword['fullform'])>0:
                        selected_awords[syntax]['fullform'] = aword['fullform'][:]
        else:
            # If there was no word form, take the same word form as in question
            if qwords.has_key(syntax):
                qword = qwords[syntax]
                if qwords[syntax].has_key('word'):
                    selected_awords[syntax]['word'] = qwords[syntax]['word']
                if qwords[syntax].has_key('tag'):
                    selected_awords[syntax]['tag'] = qwords[syntax]['tag']
                
        if not selected_awords[syntax].has_key('fullform'):
            if selected_awords[syntax].has_key('word') and selected_awords[syntax].has_key('tag'):

                form_list = None
                max=50
                i=0
                while not form_list and i<max:
                    i=i+1
                    form_list = Form.objects.filter(Q(word__id=selected_awords[syntax]['word']) &\
                                                    Q(tag__id=selected_awords[syntax]['tag']))
                if form_list:
                    fullf=[]
                    for f in form_list:
                        fullf.append(f.fullform)
                    selected_awords[syntax]['fullform'] = fullf[:]
                        
        # make sure that theres is something to print
        if not selected_awords[syntax].has_key('fullform'):
            selected_awords[syntax]['fullform'] = []
            selected_awords[syntax]['fullform'].append(syntax)

    #print "SELECTED2:", selected_awords
    return selected_awords


def qa_is_correct(self, atext, awords):
    """
    Determines if the given answer is correct (for a bound form).
    """
    if not self.is_valid():
        return False

    
    self.userans = self.cleaned_data['answer']
    answer = self.userans.rstrip()
    answer = answer.lstrip()
    answer = answer.rstrip('.!?,')

    self.error = "error"

    problems = []
    answer_words = answer.split()
                
    for word in atext.split():
        if word.count("(") > 0:
            continue

        if awords.has_key(word):
            found = False
            for a in answer_words:
                if not a: continue
                
                aword_list = awords[word]
                for aw in aword_list:
                    form_elements=None
                    if aw.has_key('fullform') and a in set(aw['fullform']):
                        found = True
                        break

                    if aw.has_key('qelement') and aw.has_key('tag'):
                        qelement = aw['qelement']
                        tag = aw['tag']
                        fullforms = Form.objects.filter(fullform=a.lower(), tag__id=tag)
                        if not fullforms:
                            fullforms = Form.objects.filter(fullform=a, tag__id=tag)
                        if fullforms:
                            for f in fullforms:
                                if WordQElement.objects.filter(word=f.word, qelement=qelement).count()>0:
                                    found = True
                                    break
            if not found:
                problems.append(word)

    print "********************", problems
    self.problems = string.join(problems, ', ' )
    if not problems:
        self.error = "correct"

    return


class QAForm(forms.Form):

    set_settings = set_settings

    num_context = forms.ChoiceField(initial='NUM-ATTR', choices=NUM_CONTEXT_CHOICES, widget=forms.Select)
    vtype = forms.ChoiceField(initial='MAINV', choices=VTYPE_CHOICES, widget=forms.Select)
    vtype_bare = forms.ChoiceField(initial='PRS', choices=VTYPE_BARE_CHOICES, widget=forms.Select)
    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    default_data = {'pos': 'N'}

    def __init__(self, *args, **kwargs):
        self.set_settings()
        super(QAForm, self).__init__(*args, **kwargs)


class QAQuestion(forms.Form):
    """
    Questions for vasta
    """

    select_words = select_words
    set_correct = set_correct
    is_correct = is_correct
    qa_is_correct = qa_is_correct
    qtype_verbs = set(['MAINV','V-COND','V-IMPRT','V-GO'])

        
    def __init__(self, gametype, question, qanswer, \
                 qwords, awords, userans_val, correct_val, *args, **kwargs):

        self.userans = userans_val
        self.correct_anslist = []
        self.qa_correct_anslist = {}
        self.correct_answers =""
        self.error='empty'
        self.problems="error"
        self.lemma = ""
        self.pron = ""
        
        qtype=question.qtype
        if qtype in self.qtype_verbs:
            qtype = 'MAINV'

        question_widget = forms.HiddenInput(attrs={'value' : question.id})
        answer_widget = forms.HiddenInput(attrs={'value' : qanswer.id})
        atext = qanswer.string

        super(QAQuestion, self).__init__(*args, **kwargs)

        answer_size = 20
        if gametype == 'context':
            answer_size=20
        if gametype == 'qa':
            answer_size=50

        self.fields['answer'] = forms.CharField(max_length = answer_size, \
                                                widget=forms.TextInput(attrs={'size': answer_size}))
        self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)
        self.fields['answer_id'] = forms.CharField(widget=answer_widget, required=False)

        # Select words for the the answer
        selected_awords = self.select_words(qwords, awords)

        # In qagame, all words are considered as answers.
        #print awords
        form_list=[]
        if (gametype == 'qa'):
            self.qa_is_correct(atext,awords)

            #    for word in atext.split():
            #    self.qa_correct_anslist[word] = []
             #   if awords.has_key(word):
             #       aword_list = awords[word]
             #       for aw in aword_list:
             #           form_elements=None
             #           if aw.has_key('fullform'):
             #               form_list.append(aw['fullform'])
             #           else:
             #               if aw.has_key('qelement'):
             #                   wq_els = WordQElement.objects.filter(qelement__id=aw['qelement'])
             #                   for w in wq_els:
             #                       form_elements = Form.objects.filter(Q(word=w.word) &\
             #                                                           Q(tag__pk=aw['tag']))
             #           if form_elements:
             #               for f in form_elements:
             #                   form_list.append(f.fullform)

              #      if not form_list:
              #          self.qa_correct_anslist[word].append(word)
              #      else:
              #          self.qa_correct_anslist[word] = [ form_list ]

            #self.qa_is_correct(atext,awords)
            
        if (gametype == 'context'):
            self.correct_anslist = selected_awords[qtype]['fullform'][:]
            self.is_correct()
                
            
        self.qattrs= {}
        self.aattrs= {}        
        for syntax in qwords.keys():
            qword = qwords[syntax]
            if qword.has_key('word'):
                self.qattrs['question_word_' + syntax] = qword['word']
            if qword.has_key('tag') and qword['tag']:
                self.qattrs['question_tag_' + syntax] = qword['tag']
            if qword.has_key('fullform') and qword['fullform']:
                self.qattrs['question_fullform_' + syntax] = qword['fullform'][0]

        for syntax in selected_awords.keys():
            if selected_awords[syntax].has_key('word'):
                self.aattrs['answer_word_' + syntax] = selected_awords[syntax]['word']
            if selected_awords[syntax].has_key('tag'):
                self.aattrs['answer_tag_' + syntax] = selected_awords[syntax]['tag']
            if selected_awords[syntax].has_key('fullform') and len(selected_awords[syntax]['fullform']) == 1:
                self.aattrs['answer_fullform_' + syntax] = selected_awords[syntax]['fullform'][0]

        # Forms question string and answer string out of grammatical elements and other strings.
        qstring = ""
        astring= ""

        # Format question string
        qtext = question.string
        for w in qtext.split(' '):
            if not qwords.has_key(w): qstring = qstring + " " + w
            else:
                if qwords[w].has_key('fullform'):
                    qstring = qstring + " " + qwords[w]['fullform'][0]
                else:
                    qstring = qstring + " " + w
                    
        if gametype == 'context':
            answer_word= selected_awords[qtype]['word']
            answer_tag =selected_awords[qtype]['tag']
            selected_awords[qtype]['fullform'][0] = 'Q'
                
            # Get lemma for contextual morfa
            answer_word_el = Word.objects.get(id=answer_word)
            answer_tag_el = Tag.objects.get(id=answer_tag)
            self.lemma = answer_word_el.lemma
            
            # If the asked word is in Pl, generate nominal form
            if answer_tag_el.pos=="N":
                if answer_tag_el.number=="Sg":
                    self.lemma = answer_word_el.lemma
                else:
                    self.lemma = Form.objects.filter(Q(word__pk=answer_word) & \
                                                     Q(tag__string="N+Pl+Nom"))[0].fullform

                
        # If there are errors in the qa input, give the user the opportunity to try again
        # with the problematic fields
        #if gametype == 'qa':
        #    for p in self.problems:
        #        selected_awords[p]['fullform'][0] = Q
            
        # Format answer string
        #print "SELECTED", selected_awords
        for w in atext.split():
            if w.count("(") > 0: continue
            if w== 'ANSWERSUBJECT': w='SUBJ'
            
            if not selected_awords.has_key(w) or not selected_awords[w].has_key('fullform'):
                astring = astring + " " + w
            else:
                astring = astring + " " + selected_awords[w]['fullform'][0]
                    
        # Remove leading whitespace and capitalize.
        astring = astring.lstrip()
        qstring = qstring.lstrip()
        astring = astring[0].capitalize() + astring[1:]
        qstring = qstring[0].capitalize() + qstring[1:]

        qstring = qstring + "?"
        self.question=qstring

        # Format answer strings for context
        q_count = astring.count('Q')
        if q_count > 0:
            astrings = astring.split('Q')
            if astrings[0]:
                self.answertext1=astrings[0]
            if astrings[1]:
                self.answertext2=astrings[1]

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"


