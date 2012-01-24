# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
import univ_oahpa.settings as settings

from univ_oahpa.conf.tools import switch_language_code

from models import *
#from game import * 
#from univ_oahpa.univ_drill.game import relax
import datetime
import socket
import sys, os
import itertools
from random import choice

# TODO: These should be accessible in the admin interface, not hardcoded.

PRONOUNS_LIST = {'Sg1':'mun', 'Sg2':'don', 'Sg3':'son',
		  'Pl1':'mii', 'Pl2':'dii', 'Pl3':'sii',
		  'Du1':'moai', 'Du2':'doai', 'Du3':'soai'}

NEGATIVE_VERB_PRES = {'Sg1':'in', 'Sg2':'it', 'Sg3':'ii',
		  'Pl1':'mii', 'Pl2':'dii', 'Pl3':'sii',
		  'Du1':'moai', 'Du2':'doai', 'Du3':'soai'}

RECIPROCATIVE_PRESENTATION = {
	'Du': u'guhtet',
	'Pl': u'goabbat',
}

DEMONSTRATIVE_PRESENTATION = {
	'Sg': u'okta',
	'Pl': u'máŋga',
}

POS_CHOICES = (
	('N', _('noun')),
	('V', _('verb')),
	('A', _('adjective')),
	('Num', _('numeral')),
	('Pron', _('pronoun')),
)

CASE_CHOICES = (
	('NOMPL', _('plural')),
	('N-ACC', _('accusative')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
	('N-GEN', _('genitive')),
	('N-ESS', _('essive')),
)

# Pers - akk, gen, ill, lok, kom
# Dem - akk, gen, ill, lok, kom
CASE_CHOICES_PRONOUN = (
	('N-ACC', _('accusative')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
	('N-GEN', _('genitive')),
	# ('N-ESS', _('essive')),
)

# Refl - ill, lok, kom
# Recipr - ill, lok, kom
RECIP_REFL_CHOICES = (
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
)

PRONOUN_SUBCLASSES = (
	('Pers', _('personal')),
	('Dem', _('demonstrative')),
	('Recipr', _('reciprocative')),
	('Refl', _('reflexive')),
)

CASE_CONTEXT_CHOICES = (
	('N-NOM-PL', _('plural')),
	('N-ACC', _('accusative')),
	('N-GEN', _('genitive')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
	('N-ESS', _('essive')),
	('N-MIX', _('mix')),
)

# 
# No inessive or essive, and no choice between nom sg. and pl, but nom sg and pl come together.
# 
PRON_CONTEXT_CHOICES = (
	#('P-NOM', _('nominative')), Morfa C pronomen nominativ skal fjernes fra menyen dersom oppgavene har ingen hensikt.
    ('P-PERS', _('personal')),
    ('P-DEM', _('demonstrative')),
    ('P-RECIPR', _('reciprocative')),
    ('P-REFL', _('reflexive')),
)

ADJCASE_CHOICES = (
	('NOMPL', _('plural')),
	('ATTR', _('attributive')),
	('N-ACC', _('accusative')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
	('N-GEN', _('genitive')),
	('N-ESS', _('essive')),
)

ADJEX_CHOICES = (
	('A-ATTR', _('attributive')), 	# A+Nom+Sg -> A+Attr
 	('A-COMP', _('comparative')),		# A+Nom+Sg -> Comp	TODO: A+Attr -> Comp
 	('A-SUPERL', _('superlative')),	# A+Nom+Sg -> Superl	TODO: A+Attr -> Comp

)

ADJ_CONTEXT_CHOICES = (
	('ATTRPOS', _('attributive positive')),
	('ATTRCOMP', _('attributive comparative')),
	('ATTRSUP', _('attributive superlative')),
	('PREDPOS', _('predicative positive')),
	('PREDCOMP', _('predicative comparative')),
	('PREDSUP', _('predicative superlative')),
)

GRADE_CHOICES = (
	('POS', _('positive')),
	('COMP', _('comparative')),
	('SUPERL', _('superlative')),
)

NUM_CONTEXT_CHOICES = (
	('NUM-ATTR', _('attributive')),
	('NUM-NOM-PL', _('plural')),
	('NUM-ACC', _('accusative')),
	('NUM-ILL', _('illative')),
	('NUM-LOC', _('locative')),
	('NUM-COM', _('comitative')),
	('COLL-NUM', _('collective')),
	('ORD-NUM', _('ordinals')),
)

NUM_BARE_CHOICES = (
	('NOMPL', _('plural')),
	('N-ACC', _('accusative')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
)

NUM_LEVEL_CHOICES = (
	('1', _('First level')),
	('2', _('Second level')),
)

VTYPE_CHOICES = (
	('PRS', _('present')),
	('PRT', _('past')),
	('PRF', _('perfect')),
	('GER', _('gerund')),
	('COND', _('conditional')),
	('IMPRT', _('imperative')),
	('POT', _('potential')),
)

VTYPE_CONTEXT_CHOICES = (
	('V-PRS', _('present')),
	('V-PRT', _('past')),
	('V-PRF', _('perfect')),
	('V-GER', _('gerund')),
	('V-COND', _('conditional')),
	('V-IMPRT', _('imperative')),
	('V-POT', _('potential')),
	('V-MIX', _('mix')),
	('TEST', _('test questions')),
 )

LEVEL_CHOICES = (
	('l1', _('Level 1')),
	('l2', _('Level 1-2')),
	('l3', _('Level 1-3')),
	('all', _('All')),
)

BOOK_CHOICES = (
    ('d1', _('Davvin 1')),
    ('d2', _('Davvin 1-2')),
    ('d3', _('Davvin 1-3')),
    ('d4', _('Davvin 1-4')),
    ('AA', _('Aikio komp.')),
    ('c1', _('Cealkke 1')),
    ('c2', _('Cealkke 1-2')),
    ('c3', _('Cealkke 1-3')),
    ('c4', _('Cealkke 1-4')),
    ('sam1031_1', _('SAM-1031-1')),
    ('sam1031_2', _('SAM-1031-2')),
    ('algu', _('algu')),
    ('sara', _('sara')),
    ('bures', _('Bures bures fas')),
    ('oaidnalit', _('Oaidnalit')),
    ('all', _('All')),
)

FREQUENCY_CHOICES = (
	('rare', _('rare')),
	('common', _('common')),
)

GEOGRAPHY_CHOICES = (
	('world', _('world')),
	('sapmi', _('sapmi')), # was: sápmi, maybe characters with diacritics not allowed in drop-down menus
	('suopma', _('suopma')),
)

VASTA_LEVELS = (
	('1', _('First level')),
	('2', _('Second level')),
	('3', _('Third level')),
)

TRANS_CHOICES = (
	('smenob', _('North Sami to Norwegian')),
	('nobsme', _('Norwegian to North Sami')),
#	('smeswe', _('North Sami to Swedish')),
#	('swesme', _('Swedish to North Sami')),
	('smefin', _('North Sami to Finnish')),
	('finsme', _('Finnish to North Sami')),
#	('smeeng', _('North Sami to English')),
#	('engsme', _('English to North Sami')),
#	('smedeu', _('North Sami to German')),
#	('deusme', _('German to North Sami')),
)

NUMLANGUAGE_CHOICES = (
	('sme', _('North Sami')),
#	('smj', _('Lule Sami')),
#	('sma', _('South Sami')),
#	('smn', _('Inari Sami')),
#	('sjd', _('Kildin Sami')),
#	('sms', _('Skolt Sami')),
#	('fin', _('Finnish')),
)

SEMTYPE_CHOICES = (
	('FAMILY', _('family')), 
	('HUMAN', _('human')),
	('HUMAN-LIKE', _('human-like')),
	('ANIMAL', _('animal')),
	('FOOD/DRINK', _('food/drink')),
	('TIME', _('time')),
	('CONCRETES', _('concretes')),
	('BODY', _('body')),
	('CLOTHES', _('clothes')),
	('BUILDINGS/ROOMS', _('buildings/rooms')),
	('CITY', _('city')), 
	('NATUREWORDS', _('naturewords')),
	('LEISURETIME/AT_HOME', _('leisuretime/at_home')),
	('CHRISTMAS', _('christmas')),
	('PLACES', _('places')),
	('LITERATURE', _('literature')),
	('SCHOOL/EDUCATION', _('school/education')),
	('ABSTRACTS', _('abstracts')),
	('WORK/ECONOMY/TOOLS', _('work/economy/tools')),
	('MULTIWORD', _('Multiword')),
	('all', _('all')),
)

NUM_CHOICES = (
	('10', _('0-10')),
	('20', _('0-20')),
	('100', _('0-100')),
	('1000', _('0-1000')),
#	('ALL', _('all')),
)

NUMGAME_CHOICES = (
	('string', _('String to numeral')),
	('numeral', _('Numeral to string')),
)

NUMGAME_CHOICES_PL = (
	('string', _('Strings to numerals')),
	('numeral', _('Numerals to strings')),
)

# These are not actually used in Forms, but used as a way to sneak these
# into the locale files so that the trans tag may be applied to
# form.wordclass without altering code here

VERB_CLASSES = (
	('I', _('I')),
	('II', _('II')),
	('III', _('III')),
	('IV', _('IV')),
	('V', _('V')),
	('VI', _('VI')),
	('Odd', _('Odd')),
)

KLOKKA_CHOICES = (
	('kl1', _('easy')),
	('kl2', _('medium')),
	('kl3', _('hard')),
)

DIALOGUE_CHOICES = (
	('firstmeeting', _('Firstmeeting')),
	('firstmeeting_boy', _('Firstmeeting boy')),
	('firstmeeting_girl', _('Firstmeeting girl')),
	('firstmeeting_man', _('Firstmeeting man')),
	('visit', _('Visit')),
	('grocery', _('Grocery')),
	('shopadj', _('Shopadj')),
)

# BOOK_CHOICES = tuple(
# 	[(source.name, source.name) for source in Source.objects.all()] + \
# 	[('all', _('ALL'))]
# )


# Syllables are manually coded in the templates, but it's useful to get the
# translation strings here, also for the courses module logging.

SYLLABLE_VALUES = (
	('2syll', _('bisyllabic')),
	('3syll', _('trisyllabic')),
	('Csyll', _('contracted')),
)

ALL_CHOICES = [
	ADJCASE_CHOICES, 
	ADJEX_CHOICES, 
	ADJ_CONTEXT_CHOICES,
	BOOK_CHOICES, 
	CASE_CHOICES, 
	CASE_CHOICES_PRONOUN, 
	CASE_CONTEXT_CHOICES,
	DIALOGUE_CHOICES, 
	FREQUENCY_CHOICES, 
	GEOGRAPHY_CHOICES, 
	GRADE_CHOICES,
	KLOKKA_CHOICES, 
	LEVEL_CHOICES, 
	NUMGAME_CHOICES, 
	NUMGAME_CHOICES_PL,
	NUMLANGUAGE_CHOICES, 
	NUM_BARE_CHOICES, 
	NUM_CHOICES, 
	NUM_CONTEXT_CHOICES,
	NUM_LEVEL_CHOICES, 
	POS_CHOICES, 
	PRONOUN_SUBCLASSES, 
	PRON_CONTEXT_CHOICES,
	RECIP_REFL_CHOICES, 
	SEMTYPE_CHOICES, 
	SYLLABLE_VALUES,
	TRANS_CHOICES, 
	VASTA_LEVELS, 
	VERB_CLASSES,
	VTYPE_CHOICES, 
	VTYPE_CONTEXT_CHOICES]



# #
#
# Form validation
#
# #


import re

from univ_oahpa.settings import INFINITIVE_SUBTRACT as infinitives_sub
from univ_oahpa.settings import INFINITIVE_ADD as infinitives_add

def relax(strict):
	"""Returns a list of relaxed possibilities, making changes by relax_pairs.
		
		Many possibilities are generated in the event that users are
		inconsistent in terms of substituting one letter but not substituting 
		another, however, *all* possibilities are not generated.
		
		E.g., *ryøjnesjäjja is accepted for ryöjnesjæjja
				(user types ø instead of ö consistently)
				
				... but ...
			  
			  *töølledh is not accepted for töölledh
				(user mixes the two in one word)
		
		Similarly, directionality is included. <i> is accepted for <ï>, but
		not vice versa.
		
		E.g.:  *ååjmedïdh is not accepted for ååjmedidh, 
				... but ...
				*miele is accepted for mïele.
	"""
	from django.utils.encoding import force_unicode
	
	relaxed = strict
	sub_str = lambda _string, _target, _sub: _string.replace(_target, _sub)
	
	relax_pairs = {
		# key: value
		# key is accepted for value
		u'ø': u'ö',
		u'ä': u'æ',
		u'i': u'ï'
	}
	
	# Create an iterator. We want to generate as many possibilities as 
	# possible (very fast), so more relaxed options are available.
	searches = relax_pairs.items()
	permutations = itertools.chain(itertools.permutations(searches))
	perms_flat = sum([list(a) for a in permutations], [])
	
	# Individual possibilities
	relaxed_perms = [sub_str(relaxed, R, S) for S, R in perms_flat]
	
	# Possibilities applied one by one
	for S, R in perms_flat:
		relaxed = sub_str(relaxed, R, S)
		relaxed_perms.append(relaxed)
	
	# Return list of unique possibilities
	relaxed_perms = list(set(relaxed_perms))
	relaxed_perms = [force_unicode(item) for item in relaxed_perms]

	return relaxed_perms

def is_correct(self, game, example=None):
	"""
	Determines if the given answer is correct (for a bound form).
	"""
	self.game = game
	self.example = example

	if not self.is_valid():
		return False
		
	self.userans = self.cleaned_data['answer']
	
	self.answer = self.userans.strip()
	
	if not game == "numra":
		self.answer = self.answer.rstrip('.!?,')
	
	self.error = "error"
	self.iscorrect = False
	
	if self.answer in set(self.correct_anslist) or \
			self.answer.lower() in set(self.correct_anslist) or \
			self.answer.upper() in set(self.correct_anslist):
		self.error = "correct"
		self.iscorrect = True
	
	# Log information about user answers.
	
	correctlist = u",".join([a for a in self.correct_anslist])
	self.correctlist = correctlist
	self.log_response()

def set_correct(self):
	"""
	Adds correct wordforms to the question form.
	"""
	if self.correct_ans:
		self.correct_answers = self.correct_ans[:]
		if type(self.correct_answers) == list:
			self.correct_answers = ', '.join(self.correct_answers)
	
	

def set_settings(self):
	# self.levels = { 
	# 		'l1':  ['l1'],
	# 		'l2':  ['l2', 'l1'], 
	# 		'l3':  ['l3', 'l2', 'l1'], 
	# 		'all': ['l3', 'l2', 'l1', 'all'], 
	# 	}
	
	# Construct arrays for level choices.
	
	# Commenting this out because I don't see yet why this needs to be constructed this way.
	# If it's done automatically so that more levels can be added, the code here will still need
	# to be altered... So it seems easiest to just hard-code this for now.
	
	# self.levels = {}
	# self.levels['all'] = [] 
	# for b in LEVEL_CHOICES:
	# 	if b[0] != 'all':
	# 		self.levels[b[0]] = [] 
	# 		self.levels['all'].append(b[0])
	# 		
	# 	self.levels[b[0]].append(b[0])
	# 
	# self.levels['l2'].append('l1')
	# for b in ['l1', 'l2']:
	# 	self.levels['l3'].append(b)
	
	
	# Turning these into dictionary type means there's no need to iterate to 
	# get the first tuple item. Also makes it easier to read. And, there are 
	# no many-to-many relationships in these tuples of tuples
	
	self.allsem = dict(SEMTYPE_CHOICES).keys()
	self.allcase = dict(CASE_CHOICES).keys()
	self.allcase_context = dict(CASE_CONTEXT_CHOICES).keys()
	self.proncase_context = dict(PRON_CONTEXT_CHOICES).keys()
	self.allvtype_context = dict(VTYPE_CONTEXT_CHOICES).keys()
	self.alladjcase = dict(ADJCASE_CHOICES).keys()  # added by Heli
	self.allgrade = dict(GRADE_CHOICES).keys() # added by Heli
	self.alladj_context = dict(ADJ_CONTEXT_CHOICES).keys()
	self.allnum_context = dict(NUM_CONTEXT_CHOICES).keys()
	self.allnum_bare = dict(NUM_BARE_CHOICES).keys()
	self.sources = dict(BOOK_CHOICES).keys()
	self.geography = dict(GEOGRAPHY_CHOICES).keys()
	self.frequency = dict(FREQUENCY_CHOICES).keys() # added by Heli


# comment
# DEBUG = open('/dev/ttys001', 'w')
# DEBUG = open('/dev/null', 'w')


def get_feedback(self, word, tag, wordform, language, dialect):
	"""
		FEEDBACK AND XML-SOURCE
		
		Nouns: attributes required: pos, soggi, stem, case/case2, number

			<l> nodes in messages.xml and n_smanob must match for
				pos, soggi, stem
			
			Remaining inflectional items, case and number, come from the tag.
						
			feedback_nouns.xml: 
			
			<feedback pos="N">
			  <stems>
				<l stem="2syll">
				  <msg pos="n">bisyllabic_stem</msg>
				</l>
				<l stem="3syll">
				  <msg pos="n">trisyllabic_stem</msg>
				</l>

				<l stem="3syll" soggi="a">
				  <msg case="Ill">soggi_a</msg>
				  <msg case="Ine">soggi_a</msg>
				  <msg case="Ela">soggi_a</msg>
				  <msg case="Com" number="Sg">soggi_a</msg>
				  <msg case="Ess">soggi_a</msg>
				  <note>daktarasse, vuanavasse, e/o > a</note>
				</l>
			 </stems>
			</feedback>
			
			
			n_smanob.xml:
			
			<e>
			  <lg>
				 <l margo="e" pos="n" soggi="e" stem="3syll">aagkele</l>
			  </lg>
			  { ... SNIP ... }
			</e>
			
		Verbs: Mostly the same. <l/>s match for class, stem, pos
		inflectional information from Tag object pertaining to mood, tense, personnumber.
		
		FEEDBACK DATA STRUCTURE
		
		Remember that this code runs once per word, and not on a huge set of words,
		so it should ideally be returning only one Feedback object.
		
		Feedback objects are then linked to Feedbackmsg objects, which contain
		message IDs, such as soggi_o, class_1, which then link to Feedbacktext objects
		which contain the corresponding messages in other languages.
		
		Feedback objects should be linked to multiple Feedbackmsg items (typically, 3)
		which individually contain class, syllable and umlaut information.
		
		Feedback.messages.all()
		
		CHANGES
		
		Altering the way the code functions should be as simple as adding new attributes
		to the dictionary objects below, and making sure that they have access to the
		variable with the data to be included.
		
				word_attrs = {
					'POS': {
						'soggi' : word.soggi,
					},
				}
		
	"""
	
	# Dictionaries here contain mapping of attributes, and where the data is stored.

	
	# Word -> Feedback
	# These should generally match up with attributes in <l /> in source data
	word_attrs = {
		'N': {
			'pos': word.pos,
			'soggi': word.soggi,
			'stem': word.stem,
			'diphthong': word.diphthong,
			'gradation': word.gradation,
			'rime': word.rime,
		},
		'V': {
			'pos': word.pos,
			'soggi': word.soggi,
			'wordclass': word.wordclass,
			'stem': word.stem,
			'diphthong': word.diphthong,
			'gradation': word.gradation,
			'rime': word.rime,
		},
		'A': {
			'wordclass': word.wordclass,
			'stem': word.stem,
			'pos': word.pos,
			'diphthong': word.diphthong,
			'gradation': word.gradation,
			'attrsuffix': word.attrsuffix,
			'rime': word.rime,
		},
	}
	
	# Tag -> Feedback
	# inflectional information
	tag_attrs = {
		'N': {
			'case2': tag.case,
			'number': tag.number,
		},
		'V': {
			'mood': tag.mood,
			'tense': tag.tense,
			'personnumber': tag.personnumber,
		},
		'A': {
			'case2': tag.case,
			'number': tag.number,
			'attributive': tag.attributive,
			'grade':tag.grade  # added by Heli
		}
	}
		
	if tag.pos in ["N", "Num"]:
		POS = 'N'
		# build Q for noun
	elif tag.pos == "A":
		POS = 'A'
		# build Q for verb
	elif tag.pos == "V":
		POS = 'V'
	else:
		POS = tag.pos

	# Combine the filter sets...
	try:
		FILTERS = dict(word_attrs[POS], **tag_attrs[POS])
	except KeyError:
		return False
	
	# Now make changes.
	if POS == 'V':
		# stem and wordclass are in complementary distribution
		# when one is set the other is not. All 2syll verbs
		# have class information, but all 3syll verbs do not.
		
		if FILTERS['stem'] == '3syll':
			FILTERS.pop('wordclass')
		elif FILTERS['stem'] == '2syll':
			FILTERS.pop('stem')
	
	if POS == 'A':
		if 'grade' not in FILTERS:
			FILTERS['grade'] = 'POS' # was 'Pos'

		if 'attributive' not in FILTERS:
			FILTERS['attributive'] = 'NoAttr'

	# Adopt this to new code.
	# elif tag.pos == "A":
	# 	if tag.grade: 
	# 		grade = tag.grade
	# 	else:
	# 		grade = "Pos"
	# 	
	# 	if tag.attributive:
	# 		attributive = "Attr"
	# 		attrsuffix = word.attrsuffix
	# 	else:
	# 		attributive = "NoAttr"
	# 	
	# 	FEEDBACK_Q = Q(case2=tag.case) & \
	# 					Q(pos=tag.pos) & Q(grade=grade) &\
	# 					Q(attributive=attributive) & Q(attrsuffix=attrsuffix) & \
	# 					Q(number=tag.number)
	# 
	
	language = switch_language_code(language)
	
	if FILTERS:
		feedbacks = Feedback.objects.filter(**FILTERS)
	
	message_list = []
	if feedbacks:
		for f in feedbacks:
			msgs = f.messages.all()
			for m in msgs:
				messages = m.feedbacktext_set.filter(language=language)
				if messages.count() > 0:
					text = messages[0].message
					text = text.replace('WORDFORM', '"%s"' % wordform)
					message_list.append(text)
	
	self.feedback = ' \n '.join(list(message_list))
	

def select_words(self, qwords, awords):
	"""
		Fetch words and tags from the database.
	"""
	from random import choice
	selected_awords = {}
	
	for syntax in awords.keys():
		word = None
		tag = None
		selected_awords[syntax] = {}

		# Select answer words and fullforms for interface
		if awords.has_key(syntax) and len(awords[syntax]) > 0:
			aword = choice(awords[syntax])
			if aword.has_key('tag'):
				selected_awords[syntax]['tag'] = aword['tag']
			if aword.has_key('word') and aword['word']:
				selected_awords[syntax]['word'] = aword['word']
			else:
				if aword.has_key('qelement') and selected_awords[syntax].has_key('tag'):
					# get form_list for a given qelement

					wqelems = WordQElement.objects.filter(qelement__id=aword['qelement'])

					# Some WordQElements are associated with words that have no
					# Forms, as such we have to randomly select one until we
					# find an element with forms. This is faster than filtering
					# by annotating and Count() 

					if wqelems.count() > 0:

						form_list = None
						i, max = 0, 50

						while not form_list and i < max:
							i += 1

							wqel = wqelems.order_by('?')[0]

							selected_awords[syntax]['word'] = wqel.word.id

							form_list = wqel.word.form_set.filter(
								tag__id = selected_awords[syntax]['tag']
							)

					if form_list:
						fullf = [f.fullform for f in form_list]
						selected_awords[syntax]['fullform'] = fullf[:]

				if not selected_awords[syntax].has_key('fullform'):
					if aword.has_key('fullform') and len(aword['fullform']) > 0:
						selected_awords[syntax]['fullform'] = aword['fullform'][:]

		if not selected_awords[syntax].has_key('fullform'):

			if selected_awords[syntax].has_key('word')\
				and selected_awords[syntax].has_key('tag'):

				form_list = Form.objects.filter(
								word__id=selected_awords[syntax]['word'],
								tag__id=selected_awords[syntax]['tag'],
							)
				
				excl = form_list.exclude(dialects__dialect='NG')

				if excl.count() > 0:
					form_list = excl

				form_list_dialects = form_list.filter(dialects__dialect=self.dialect)

				if form_list_dialects.count() > 0:
					form_list = form_list_dialects

				if form_list.count() > 0:
					fullf = []
					for f in form_list:
						fullf.append(f.fullform)
					selected_awords[syntax]['fullform'] = fullf[:]

		# make sure that there is something to print
		if not selected_awords[syntax].has_key('fullform'):
			selected_awords[syntax]['fullform'] = []
			selected_awords[syntax]['fullform'].append(syntax)

	return selected_awords



# #
#
# Oahpa form meta-classes
#
# #



class OahpaSettings(forms.Form):
	"""
		The metaform for game settings. Various games subclass from this form.
	"""
	set_settings = set_settings
	
	def clean(self):
		x = self.cleaned_data['bisyllabic']
		print 'clean: ', x
		return self.cleaned_data
	
	def set_default_data(self):
		self.default_data = {
					'language' : 'sme', # why rus ?
					'syll' : ['2syll'],
					'bisyllabic': 'on',
					'trisyllabic': False,
					'contracted': False,
					'level' : 'all',
					'case': 'N-ILL',
					'pos' : 'N',
					'vtype' : 'PRS',
					'adjcase' : 'ATTR',
					'number' : '',
					'pron_type': 'Pers',
					'proncase' : 'N-ILL',
					'grade' : '',  # was: '' 'Pos' is not a good idea beacuse it is implicit in the database.
					'case_context' : 'N-ILL',
					'vtype_context' : 'V-PRS',
					'pron_context' : 'P-PERS',
					'num_context' : 'NUM-ATTR',
					'num_level' : '1',
					'geography': 'world',
					'frequency' : [],
					'num_bare' : 'N-ILL',
					'adj_context' : 'ATTRPOS',
					'source' : 'all'}




class OahpaQuestion(forms.Form):
	"""
		Meta form for question/answer section.
	"""
	is_correct = is_correct
	set_correct = set_correct
	get_feedback = get_feedback
	
	# Set answer widget. Can this JS actually be moved to templates? 
	KEYDOWN = 'javascript:return process(this, event, document.gameform);'
	answer_attrs = {'size': 45} # , 'onkeydown': KEYDOWN}
	answer = forms.CharField(max_length=45, widget=forms.TextInput(attrs=answer_attrs))
	
	def log_response(self):
		import datetime

		today = datetime.date.today()
		# print ','.join(self.correct_anslist)

		log, c = Log.objects.get_or_create(userinput=self.answer,
											correct=','.join(self.correct_anslist),
											iscorrect=self.iscorrect,
											example=self.example,
											game=self.game,
											date=today)
	
	def __init__(self, *args, **kwargs):
		correct_val = False
		if 'correct_val' in kwargs:
			correct_val = kwargs.get('correct_val')
			kwargs.pop('correct_val')
		
		super(OahpaQuestion, self).__init__(*args, **kwargs)
		
		# set correct and error values
		if correct_val == "correct":
			self.error = "correct"
			
	def init_variables(self, possible, userans_val, accepted_answers, preferred=False):
		# Get lemma and feedback
		self.feedback = ""
		self.messages = []
		if preferred:
			self.correct_ans = preferred
		else:
			self.correct_ans = accepted_answers
		self.correct_answers = ""
		self.case = ""
		self.userans = userans_val
		self.correct_anslist = []
		self.error = "empty"
		self.problems = "error"
		self.pron = ""
		self.pron_imp = ""
		self.PronPNBase = PRONOUNS_LIST
		self.is_relaxed = ""
		self.is_tcomm = ""
		forms = []
		relaxings = []
		if hasattr(self, 'translang'):
			if self.translang == 'sme':
				# Relax spellings.
				accepted_answers = [force_unicode(item) for item in accepted_answers]
				forms = sum([relax(force_unicode(item)) for item in accepted_answers], [])
				# need to subtract legal answers and make an only relaxed list.
				relaxings = [item for item in forms if force_unicode(item) not in accepted_answers]
			else:

				# add infinitives as possible answers
				if self.word.pos == 'V':
					if self.translang in infinitives_sub and infinitives_add:
						infin_s = infinitives_sub[self.translang]
						infin_a = infinitives_add[self.translang]

						lemma = re.compile(infin_s)
						infins = [lemma.sub(infin_a, force_unicode(ax)) for ax in accepted_answers]
						accepted_answers = infins + accepted_answers

				forms = accepted_answers
		
		self.correct_anslist = [force_unicode(item) for item in accepted_answers] + \
							   [force_unicode(f) for f in forms]
		self.relaxings = relaxings

		#def generate_fields(self,answer_size, maxlength):
		#	self.fields['answer'] = forms.CharField(max_length = maxlength, \
         #                                       widget=forms.TextInput(\
          #  attrs={'size': answer_size, 'onkeydown':'javascript:return process(this, event,document.gameform);',}))  # copied from old-oahpa

# #
#
# Leksa Forms
#
# #

class LeksaSettings(OahpaSettings):
	semtype = forms.ChoiceField(initial='HUMAN', choices=SEMTYPE_CHOICES)
	transtype = forms.ChoiceField(choices=TRANS_CHOICES, widget=forms.Select)
	# For placename quizz
	geography = forms.ChoiceField(initial='world', choices=GEOGRAPHY_CHOICES)
	#frequency = forms.MultipleChoiceField(required=False, widget=CheckboxSelectMultiple, choices=FREQUENCY_CHOICES)  # added
	common = forms.BooleanField(required=False, initial='1')
	rare = forms.BooleanField(required=False,initial=0)
	# sapmi = forms.BooleanField(required=False, initial='1')
	# world = forms.BooleanField(required=False,initial=0)
	# suopma = forms.BooleanField(required=False,initial=0)
	source = forms.ChoiceField(initial='all', choices=BOOK_CHOICES)
	# level = forms.ChoiceField(initial='all', choices=LEVEL_CHOICES, widget=forms.Select(attrs={'onchange':'javascript:return SetIndex(document.gameform.semtype,this.value);',}))
	
	default_data = {'gametype' : 'bare', 'language' : 'sme', 'dialogue' : 'GG', 
			'syll' : [], 
			'bisyllabic': False,
			'trisyllabic': False,
			'bisyllabic': False,
			'contracted': False,
			'source': 'all',
			'semtype' : 'HUMAN',
			'geography' : 'world',
			'frequency' : ['common'] # added
			}

	
	# set default language pair from session language setting.
	def __init__(self, *args, **kwargs):
		if 'initial_transtype' in kwargs:
			initial_transtype = kwargs.pop('initial_transtype')
		else:
			initial_transtype = False

		self.set_settings()
		super(LeksaSettings, self).__init__(*args, **kwargs)

		if initial_transtype:
			self.fields['transtype'].initial = initial_transtype
			self.default_data['transtype'] = initial_transtype
	

class LeksaQuestion(OahpaQuestion):
	"""
	Questions for word quizz
	"""
	
	def __init__(self, tcomms, stat_pref, preferred, possible, transtype, word, correct, translations, question, userans_val, correct_val, *args, **kwargs):
		lemma_widget = forms.HiddenInput(attrs={'value' : word.id})
		self.translang = transtype[-3::]
		self.word = word
		kwargs['correct_val'] = correct_val
		super(LeksaQuestion, self).__init__(*args, **kwargs)
				
		self.tcomm = None
		if tcomms:
			if userans_val in tcomms:
				self.tcomm = True
			else:
				self.tcomm = None

		
		self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
		
		if type(word) == Word:
			self.lemma = word.lemma
		else:
			self.lemma = word.definition
		
		# TODO: insert infinitives with settings.INFINITIVES
		if word.pos.upper() == 'V':
			if word.language in infinitives_sub and infinitives_add:
				infin_s = infinitives_sub[word.language]
				infin_a = infinitives_add[word.language]

				lemma = re.compile(infin_s)
				lemmax = lemma.sub(infin_a, force_unicode(self.lemma))
				self.lemma = force_unicode(lemmax)

		self.init_variables(possible=translations, 
							userans_val=userans_val, 
							accepted_answers=possible, 
							preferred=preferred)
		
		self.is_correct("leksa", self.lemma)
		# set correct and error values
		if correct_val:
			if correct_val == "correct":
				self.error = "correct"
			# relax
			if userans_val in self.relaxings:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			else:
				self.is_relaxed = ""
		
		if stat_pref:
			self.correct_ans = stat_pref

		# Displayed answer also needs infinitive marking
		# Needs to happen last because of stat_pref
		if word.pos.upper() == 'V':
			if self.translang in infinitives_sub and infinitives_add:
				infin_s = infinitives_sub[self.translang]
				infin_a = infinitives_add[self.translang]
		
				lemma = re.compile(infin_s)
				
				self.correct_ans = [lemma.sub(infin_a, force_unicode(ax)) for ax in self.correct_ans]
				self.correct_ans = [force_unicode(ax) for ax in self.correct_ans]
		
	


# #
#
# Morfa Forms 
#
# #

class MorfaSettings(OahpaSettings):
	"""
		A form for the settings part of the game form, e.g., the form used to
		set case, stem and source books for quiz questions.
		
		This is a separate form from the one which validates questions and
		answers.
	"""
	case = forms.ChoiceField(initial='N-ILL', choices=CASE_CHOICES, widget=forms.Select)
	pron_type = forms.ChoiceField(initial='PERS', choices=PRONOUN_SUBCLASSES, widget=forms.Select)
	proncase = forms.ChoiceField(initial='N-ILL', choices=CASE_CHOICES_PRONOUN, widget=forms.Select)
	adjcase = forms.ChoiceField(initial='ATTR', choices=ADJCASE_CHOICES, widget=forms.Select)  # was ADJEX_CHOICES
	vtype = forms.ChoiceField(initial='PRS', choices=VTYPE_CHOICES, widget=forms.Select)
	num_bare = forms.ChoiceField(initial='N-ILL', choices=NUM_BARE_CHOICES, widget=forms.Select)
	num_level = forms.ChoiceField(initial='1', choices=NUM_LEVEL_CHOICES, widget=forms.Select)
	num_context = forms.ChoiceField(initial='NUM-ATTR', choices=NUM_CONTEXT_CHOICES, widget=forms.Select)
	case_context = forms.ChoiceField(initial='N-ILL', choices=CASE_CONTEXT_CHOICES, widget=forms.Select)
	adj_context = forms.ChoiceField(initial='ATTR', choices=ADJ_CONTEXT_CHOICES, widget=forms.Select)
	vtype_context = forms.ChoiceField(initial='V-PRS', choices=VTYPE_CONTEXT_CHOICES, widget=forms.Select)
	pron_context = forms.ChoiceField(initial='P-PERS', choices=PRON_CONTEXT_CHOICES, widget=forms.Select)
	book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select) 
	bisyllabic = forms.BooleanField(required=False, initial=True)
	trisyllabic = forms.BooleanField(required=False, initial=False)
	contracted = forms.BooleanField(required=False, initial=False)
	grade = forms.ChoiceField(initial='POS', choices=GRADE_CHOICES, widget=forms.Select) 
	
	def __init__(self, *args, **kwargs):
		self.set_settings()
		self.set_default_data()
		super(MorfaSettings, self).__init__(*args, **kwargs)

		# If this is set, then the form has been posted by the user otherwise
		# it hasn't
		try:
			post_data = args[0]
		except:
			post_data = False

		if post_data:
			# Use a restricted choice set for pronoun case for Refl and Recipr
			if 'pron_type' in post_data:
				if post_data['pron_type'].lower() in ['refl', 'recipr']:
					self.fields['proncase'].choices = RECIP_REFL_CHOICES




class MorfaQuestion(OahpaQuestion):
	"""
	Questions for morphology game. 
	"""
	
	def __init__(self, word, tag, baseform, correct, fullforms, present, translations, question, dialect, language, userans_val, correct_val, *args, **kwargs):
		
		lemma_widget = forms.HiddenInput(attrs={'value': word.id})
		tag_widget = forms.HiddenInput(attrs={'value': tag.id})
		self.translang = 'sme'  # was: sma
		kwargs['correct_val'] = correct_val
		super(MorfaQuestion, self).__init__(*args, **kwargs)
		
		# initialize variables
		self.init_variables(possible=[], userans_val=userans_val, accepted_answers=fullforms)
		# init_variables(self, possible, userans_val, accepted_answers, preferred=False):
		
		self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
		self.fields['tag_id'] = forms.CharField(widget=tag_widget, required=False)
		self.lemma = baseform.fullform
		self.wordclass = word.wordclass
		
		# print self.lemma, correct
		# print baseform.tag, correct.tag
		
		# Retrieve feedback information
		self.get_feedback(word=word, tag=tag, wordform=baseform.fullform,
							language=language, dialect=dialect.dialect)
		
		# Take only the first translation for the tooltip
		if len(translations) > 0:
			self.translations = translations[0]
			
		if tag.pos == "N":
			self.case = tag.case

		if tag.pos == 'Pron':
			self.case = tag.case
					
		self.tag = tag.string
		
		if tag.pos == "V": 
			if tag.string.find("ConNeg") > -1:
				pers = choice(self.PronPNBase.keys())
				pronoun = self.PronPNBase[pers]
				neg_verb = NEGATIVE_VERB_PRES[pers]

				self.pron = '%s %s' % (pronoun, neg_verb)
			elif tag.personnumber:
				pronbase = self.PronPNBase[tag.personnumber]
				pronoun = pronbase
				self.pron = pronoun
				
				if self.pron and tag.mood == "Imprt":
					self.pron_imp = "(" + self.pron + ")"
					self.pron = ""
				# TODO: conneg only in Prs

		if tag.pos == "Pron":
			# Various display alternations for pronouns.
			
			# Reciprocative:
			# 	guhtet guoibmámet
			# 	goabbat guoibmámet

			if tag.subclass == 'Recipr':
				if tag.possessive.find('PxDu'):
					px_no = 'Du'
				elif tag.possessive.find('PxPl'):
					px_no = 'Pl'
				pronoun = RECIPROCATIVE_PRESENTATION.get(px_no, False)
				if pronoun:
					self.pron = pronoun

			# Demonstrative:
			# 	dát okta
			# 	dát máŋga

			if tag.subclass == 'Dem':
				noun_pres = DEMONSTRATIVE_PRESENTATION.get(tag.number, False)

				if noun_pres:
					self.lemma += ' (%s)' % force_unicode(noun_pres).encode('utf-8')
		
		log_name = "morfa_%s" % tag.pos
		self.is_correct(log_name, self.lemma + "+" + self.tag)
		
		# set correct and error values
		if correct_val:
			if correct_val == "correct":
				self.error="correct"
			# relax
			if userans_val in self.relaxings:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			else:
				self.is_relaxed = ""
		
		self.correct_ans = present
# #
#
# Numra Forms
#
# #


class NumSettings(OahpaSettings):
	maxnum = forms.ChoiceField(initial='10', choices=NUM_CHOICES, widget=forms.RadioSelect)
	numgame = forms.ChoiceField(initial='string', choices=NUMGAME_CHOICES, widget=forms.RadioSelect)
	numlanguage = forms.ChoiceField(initial='sme', choices=NUMLANGUAGE_CHOICES, widget=forms.RadioSelect)
	# TODO: remove mandatory need to set default data, should be done through 'initial' field setting.
	default_data = {'language' : 'nob', 'numlanguage' : 'sme', 'dialogue' : 'GG', 'maxnum' : '10', 'numgame': 'string'}
					
	def __init__(self, *args, **kwargs):
		self.set_settings()
		super(NumSettings, self).__init__(*args, **kwargs)


class NumQuestion(OahpaQuestion):
	"""
	Questions for numeral quizz
	"""
	game_log_name = 'numra'

	def answer_relax(self, answer):
		""" Method for relaxing answers. Override if needed.
		"""

		return answer

	def is_correct(self, game, example=None):
		self.game = game
		self.example = example

		if not self.is_valid():
			return False

		self.userans = self.cleaned_data['answer']
		self.answer = self.userans.strip()

		self.error = "error"
		self.iscorrect = False

		correct_test = self.game_obj.check_answer(self.question_str, 
													self.userans, 
													self.correct_anslist)
		if correct_test:
			self.error = "correct"
			self.iscorrect = True

		self.correctlist = u",".join(list(set(self.correct_anslist)))
		
		self.log_response()

	
	def __init__(self, numeral, num_string, num_list, gametype, userans_val, correct_val, game, *args, **kwargs):
		numeral_widget = forms.HiddenInput(attrs={'value' : numeral})
		kwargs['correct_val'] = correct_val
		self.userans_val = self.userans = userans_val
		self.game_obj = game

		if 'no_eval_correct' in kwargs:
			no_eval_correct = kwargs.pop('no_eval_correct')
		else:
			no_eval_correct = False

		super(NumQuestion, self).__init__(*args, **kwargs)
		wforms = []
		self.relaxings = []
		
		# Initialize variables
		if gametype == "string":
			self.init_variables(force_unicode(numeral), userans_val, [ numeral ])
			example = num_string
			self.question_str = num_string
		else:
			self.init_variables(force_unicode(num_list[0]), userans_val, num_list)
			wforms = sum([relax(force_unicode(item)) for item in num_list], [])
			# need to subtract legal answers and make an only relaxed list.
			self.relaxings = [item for item in wforms if item not in num_list]
			example = numeral
			self.question_str = numeral
		
		self.correct_anslist = self.correct_anslist + [force_unicode(f) for f in wforms]
		
		self.fields['numeral_id'] = forms.CharField(widget=numeral_widget, required=False)
		
		if gametype == "string":
			self.numstring = num_string
		self.numeral = numeral
		
		# Correctness not evaluated here but in child class. Short fix 
		
		if not no_eval_correct:
			self.is_correct(self.game_log_name, example)
		
		if correct_val:
			if correct_val == "correct":
				self.error = "correct"
			# relax
			if userans_val in self.relaxings:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			else:
				self.is_relaxed = ""
		
		
# #
#
# Klokka Forms
#
# #


class KlokkaSettings(NumSettings):
	numgame = forms.ChoiceField(initial='string', choices=NUMGAME_CHOICES_PL, widget=forms.RadioSelect)
	gametype = forms.ChoiceField(initial='kl1', choices=KLOKKA_CHOICES, widget=forms.RadioSelect)
	default_data = {'language' : 'nob', 'numlanguage' : 'sme', 'dialogue' : 'GG', 'gametype' : 'kl1', 'numgame': 'string'}
					
	def __init__(self, *args, **kwargs):
		self.set_settings()
		super(KlokkaSettings, self).__init__(*args, **kwargs)


class KlokkaQuestion(NumQuestion):
	"""
	Questions for numeral quizz
	"""
	game_log_name = "klokka"

	def __init__(self, *args, **kwargs):
		present_list = kwargs.get('present_list')
		accept_list = kwargs.get('accept_list')
		kwargs.pop('present_list')
		kwargs.pop('accept_list')
		
		numeral = kwargs.get('numeral')
		num_string = kwargs.get('num_string')
		correct_val = kwargs.get('correct_val')
		userans_val = kwargs.get('userans_val')
		self.gametype = gametype = kwargs.get('gametype')
		prefix = kwargs.get('prefix')
		data = kwargs.get('data')


		numeral_widget = forms.HiddenInput(attrs={'value' : numeral})
		kwargs['correct_val'] = correct_val
		self.userans_val = self.userans = userans_val
		
		kwargs['num_list'] = present_list
		# Prevent double evaluation of correctness

		kwargs['no_eval_correct'] = True
		super(KlokkaQuestion, self).__init__(*args, **kwargs)

		wforms = []
		self.relaxings = []
		# Initialize variables
		if gametype == "string":
			self.init_variables(force_unicode(numeral), userans_val, [ numeral ])
			example = num_string
			
		else:
			self.init_variables(force_unicode(accept_list), userans_val, present_list)
			wforms = sum([relax(force_unicode(item)) for item in accept_list], [])
			# need to subtract legal answers and make an only relaxed list.
			self.relaxings = [item for item in wforms if item not in accept_list]
			example = numeral
		
		self.correct_anslist = self.correct_anslist + [force_unicode(f) for f in wforms]
		
		self.fields['numeral_id'] = forms.CharField(widget=numeral_widget, required=False)
		
		if gametype == "string":
			self.numstring = num_string
		self.numeral = numeral

		self.is_correct(self.game_log_name, example)
		
		if correct_val:
			if correct_val == "correct":
				self.error = "correct"
			# relax
			if userans_val in self.relaxings:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			elif userans_val in accept_list and userans_val not in present_list:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			else:
				self.is_relaxed = ""
	


# #
#
# Dato Forms
#
# #

class DatoSettings(KlokkaSettings):
	gametype = None # Disable gametype (easy, medium, hard)

	default_data = {'language' : 'nob', 'numlanguage' : 'sme', 'numgame': 'string'}

# TODO: Relax answer format if number? Accept other things than DD.MM.?
# DD.MM
# DD/MM


class DatoQuestion(KlokkaQuestion):
	
	game_log_name = "dato"

	def answer_relax(self, answer):
		""" TODO: any need to relax the date?
			
			TODO: perhaps relax MM.DD. to MM.D. if one digit
				  is a zero?
		"""

		return answer




# #
#
# MorfaC Forms
#
# #


class ContextMorfaQuestion(OahpaQuestion):
	"""
	Questions for contextual morfa
	"""

	select_words = select_words
	qtype_verbs = set(['V-PRS', 'V-PRT', 'V-COND','V-IMPRT', 'TEST'])

	def generate_fields(self,answer_size, maxlength):
		self.fields['answer'] = forms.CharField(max_length = maxlength, \
												widget=forms.TextInput(\
			attrs={'size': answer_size,}))
			
			# 'onkeydown':'javascript:return process(this, event,document.gameform);'
	
	def __init__(self, question, qanswer, \
				 qwords, awords, dialect, language, userans_val, correct_val, *args, **kwargs):
		self.init_variables("", userans_val, [])
		self.lemma = ""
		self.dialect = dialect

		qtype=question.qtype
		if qtype in self.qtype_verbs:
			qtype = 'PRS'

		question_widget = forms.HiddenInput(attrs={'value' : question.id})
		answer_widget = forms.HiddenInput(attrs={'value' : qanswer.id})
		atext = qanswer.string
		task = qanswer.task
		if not task:
			error_msg = u"not task: %s %s (%s)" % (atext, question.qid, question.qatype)

			raise Http404(error_msg)
		super(ContextMorfaQuestion, self).__init__(*args, **kwargs)

		answer_size = 20
		maxlength = 30

		self.generate_fields(20,30)

		self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)
		self.fields['answer_id'] = forms.CharField(widget=answer_widget, required=False)

		# Select words for the the answer
		selected_awords = self.select_words(qwords, awords)

		relaxed = []
		form_list=[]
		
		if not selected_awords.has_key(task):
			raise Http404(task + " " + atext + " " + str(qanswer.id))			
		if len(selected_awords[task]['fullform'])>0:
			for f in selected_awords[task]['fullform']:
				self.correct_anslist.append(force_unicode(f))
			
			accepted = sum([relax(force_unicode(item)) for item in self.correct_anslist], [])
			self.relaxings = [item for item in accepted if item not in self.correct_anslist]
			self.correct_anslist.extend(self.relaxings)
			log_w = Word.objects.get(id=selected_awords[task]['word'])
			w_str = log_w.lemma
			w_pos = log_w.pos
			t_str = Tag.objects.get(id=selected_awords[task]['tag']).string
			log_name = "contextual_morfa_" + w_pos
			log_value = '%s+%s' % (w_str, t_str)
			self.is_correct(log_name, log_value)
			self.correct_ans = self.correct_anslist[0]

		self.correct_anslist = [force_unicode(item) for item in accepted] 
				
		self.qattrs = {}
		self.aattrs = {}		
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
		for w in qtext.split():
			if not qwords.has_key(w):
				qstring = qstring + " " + force_unicode(w)
			else:
				if qwords[w].has_key('fullform'):
					qstring = qstring + " " + force_unicode(qwords[w]['fullform'][0])
				else:
					qstring = qstring + " " + force_unicode(w)
		qstring=qstring.replace(" -","-")
		qstring=qstring.replace(" .",".")
		
		
		try:
			answer_word = selected_awords[task]['word']
		except KeyError:
			answer_word = False
			# print 'fail: ', question.qid
			# print ' task: ', task
			self.error = 'error'
			self.lemma = 'error in answer words: ' + question.qid
			return
			# self.lemma = question.qid
		answer_tag = selected_awords[task]['tag']
		selected_awords[task]['fullform'][0] = 'Q'
		
		# Get lemma for contextual morfa
		answer_word_el = Word.objects.get(id=answer_word)
		answer_tag_el = Tag.objects.get(id=answer_tag)
		self.lemma = answer_word_el.lemma
		self.tooltip_question_id = question.qid

		# Set tooltip translations
		transl = answer_word_el.translations2(language)
		# if len(transl) == 0:
			# transl = answer_word_el.translations2('nob') # Norwegian as default
		if len(transl) > 0:
			xl = transl[0]
			self.translations = xl.definition
		
		if answer_word_el.pos == 'V':
			self.wordclass = answer_word_el.wordclass
	
		# If the asked word is in Pl, generate nominal form

		if answer_tag_el.pos == "N":
			if qtype == "COLL-NUM":
				self.lemma = answer_word_el.lemma
			else:
				if answer_tag_el.number=="Sg" or answer_tag_el.case=="Ess" or qtype=="N-NOM-PL":
					self.lemma = answer_word_el.lemma
				else:
					nplforms = Form.objects.filter(word__pk=answer_word, tag__string='N+Pl+Nom')
					if nplforms.count() > 0:
						self.lemma = nplforms[0].fullform
					else:
						self.lemma = answer_word_el.lemma + " (plural) fix this"
		
		if qtype == "ORD-NUM":
			self.lemma = answer_word_el.lemma

		# Retrieve feedback information
		self.get_feedback(answer_word_el,answer_tag_el,self.lemma,dialect,language)

		# Format answer string
		for w in atext.split():
			if w.count("(") > 0:
			  continue
			
			if not selected_awords.has_key(w) or not selected_awords[w].has_key('fullform'):
				astring = astring + " " + force_unicode(w)
			else:
				astring = astring + " " + force_unicode(selected_awords[w]['fullform'][0])
					
		# Remove leading whitespace and capitalize.
		astring = astring.lstrip()
		qstring = qstring.lstrip()
		astring = astring[0].capitalize() + astring[1:]
		qstring = qstring[0].capitalize() + qstring[1:]

		qstring = qstring + "?"
		# Add dot if the last word is not the open question.
		if astring.count("!")==0 and not astring[-1]=="Q":
			astring = astring + "."
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
		if correct_val:
			if correct_val == "correct":
				self.error="correct"
			# relax
			if userans_val in self.relaxings:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			else:
				self.is_relaxed = ""

		if answer_word == False:
			self.lemma = '%s - error: %s' % (answer_word_el.lemma, question.qid)

def vasta_is_correct(self,question,qwords,language,utterance_name=None):
    """
    Analyzes the answer and returns a message.
    """
    if not self.is_valid():
        return None, None, None

    noanalysis=False

    #fstdir = "/opt/smi/sme/bin"
    fstdir = settings.FST_DIRECTORY
    lookup2cg = " | lookup2cg"
    cg3 = "/usr/local/bin/vislcg3"
    preprocess = " | /usr/local/bin/preprocess "
    dis_bin = "/opt/smi/sme/bin/sme-ped.cg3" # on victorio
    # dis_bin = "../sme/src/sme-ped.cg3" # in Heli's machine
    
    #fstdir = "/Users/saara/gt/sme/bin"
    #lookup2cg = " | /Users/saara/gt/script/lookup2cg"
    #cg3 = "/Users/saara/bin/vislcg3"
    #preprocess = " | /Users/saara/gt/script/preprocess "
    #dis_bin = "/Users/saara/ped/sme/src/sme-ped.cg3"
    
    vislcg3 = " | " + cg3 + " --grammar " + dis_bin + " -C UTF-8"

    
    self.userans = self.cleaned_data['answer']
    answer = self.userans.rstrip()
    answer = answer.lstrip()
    answer = answer.rstrip('.!?,')

    self.error = "error"
                
    qtext = question
    qtext = qtext.rstrip('.!?,')
    
    host = 'localhost'
    port = 9000  # was: 9000
    size = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host,port))
        sys.stdout.write('%')

        analysis = ""
        data_lookup = "echo \"" + qtext + "\"" + preprocess
        words = os.popen(data_lookup).readlines()
        for w in words:
            cohort=""
            if qwords and qwords.has_key(w):
                qword = qwords[w]
                if qword.has_key('word'):
                    if qword.has_key('fullform') and qword['fullform']:
                        cohort = cohort + "\"<" + qword['fullform'][0].encode('utf-8') + ">\"\n"
                        lemma = Word.objects.filter(id=qword['word'])[0].lemma
                        cohort = cohort + "\t\"" + lemma + "\""
                    if qword.has_key('tag') and qword['tag']:
                        string = Tag.objects.filter(id=qword['tag'])[0].string
                        tag = string.replace("+"," ")
                        cohort = cohort + " " + tag + "\n"
                else:
                    w=w.lstrip().rstrip()
                    s.send(w)
                    cohort = s.recv(size)
            else:
                w=w.lstrip().rstrip()
                s.send(w)
                cohort = s.recv(size)

            if not cohort or cohort == w:
                cohort = w + "\n"
            if cohort=="error":
                raise Http500
                
            analysis = analysis + cohort

        if self.gametype=="sahka":
            analysis = analysis + "\"<^qdl_id>\"\n\t\"^sahka\" QDL " + utterance_name +"\n"
        else:
            analysis = analysis + "\"<^qst>\"\n\t\"^qst\" QDL\n"

        ans_cohort=""
        data_lookup = "echo \"" + answer.encode('utf-8') + "\"" + preprocess
        word = os.popen(data_lookup).readlines()
        analyzed=""
        for c in word:
            c=c.strip()
            s.send(c)
            analyzed = analyzed + s.recv(size)
            analysis3=c + analyzed + c

    except socket.timeout:
        raise Http404("Technical error, please try again later.")            

    s.send("q")
    s.close()

    analysis = analysis + analyzed
    analysis = analysis + "\"<.>\"\n\t\".\" CLB"
    analysis = analysis.rstrip()
    analysis = analysis.replace("\"","\\\"")

    ped_cg3 = "echo \"" + analysis + "\"" + vislcg3
    checked = os.popen(ped_cg3).readlines()

    wordformObj=re.compile(r'^\"<(?P<msgString>.*)>\".*$', re.U)
    messageObj=re.compile(r'^.*(?P<msgString>&(grm|err|sem)[\w-]*)\s*$', re.U)
    targetObj=re.compile(r'^.*\"(?P<targetString>[\wáÁæÆåÅáÁšŠŧŦŋŊøØđĐžZčČ-]*)\".*dia-.*$', re.U)
    # Extract the lemma    
    constantObj=re.compile(r'^.*\"\<(?P<targetString>[\wáÁæÆåÅáÁšŠŧŦŋŊøØđĐžZčČ-]*)\>\".*$', re.U)
    diaObj=re.compile(r'^.*(?P<targetString>&dia-[\w]*)\s*$', re.U)

    # Each wordform may have a set of tags.
    spelling = False
    msgstrings = {}
    diastring = "jee"
    lemma=""
    for line in checked:
        line = line.strip()

        #Find the lemma first
        matchObj=constantObj.search(line)
        if matchObj:
            lemma = matchObj.expand(r'\g<targetString>')

        #The wordform
        matchObj=wordformObj.search(line)
        if matchObj:
            wordform = matchObj.expand(r'\g<msgString>')
            msgstrings[wordform] = {}
            
        #grammatical/semantic/other error
        matchObj=messageObj.search(line)
        if matchObj:
            msgstring = matchObj.expand(r'\g<msgString>')
            if msgstring.count("spellingerror") > 0:
                spelling = True
            msgstrings[wordform][msgstring] = 1

        #Store the baseform if tehre is dia-whatever
        matchObj=targetObj.search(line)
        if matchObj:
            msgstring = matchObj.expand(r'\g<targetString>')
            msgstrings[wordform]['dia-target'] = msgstring
            msgstrings[wordform]['dia-lemma'] = lemma

        # What is the dia-tag?
        matchObj=diaObj.search(line)
        if matchObj:
            msgstring = matchObj.expand(r'\g<targetString>')
            msgstrings[wordform][msgstring] = 1
            diastring=msgstring            
            

    msg=[]
    dia_msg = []
    target = ""
    variable=""
    constant=""
    found=False
    #Interface language    
    if not language: language = "nob"
    if language == "no" : language = "nob"
    if language == "fi" : language = "fin"
    if language == "en" : language = "eng"
    if not language=="nob" and not language=="sme" and not language=="fin" and not language=="eng": language="nob"
    for w in msgstrings.keys():
        if found: break
        for m in msgstrings[w].keys():
            if spelling and m.count("spelling") == 0: continue
            m = m.replace("&","") 
            if Feedbackmsg.objects.filter(msgid=m).count() > 0:
                msg_el = Feedbackmsg.objects.filter(msgid=m)[0]
                message = Feedbacktext.objects.filter(feedbackmsg=msg_el,language=language)[0].message
                message = message.replace("WORDFORM","\"" + w + "\"") 
                msg.append(message)
                if not spelling:
                    found=True
                    break                
            else:
                if m.count("dia-") == 0:
                    msg.append(m)
                    if not spelling:
                        found=True
                        break
            if m.count("dia-") > 0:
                dia_msg.append(m)
        if msgstrings[w].has_key('dia-target'):
            constant = msgstrings[w]['dia-lemma']
            variable = msgstrings[w]['dia-target']
        if msgstrings[w].has_key('dia-unknown'):
            constant = msgstrings[w]['dia-lemma']
            variable = msgstrings[w]['dia-unknown']

    #iscorrect is used only in logging
    iscorrect=False
    if not msg:
        self.error = "correct"
        iscorrect=True

    feedbackmsg=' '.join(msg)
    today=datetime.date.today()
    log = Log.objects.create(userinput=self.userans,feedback=feedbackmsg,iscorrect=iscorrect,\
                                       example=question,game=self.gametype,date=today)
    log.save()           
        
    variables = []
    variables.append(variable)
    variables.append(constant)
    return msg, dia_msg, variables


class VastaSettings(OahpaSettings):

    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    level = forms.ChoiceField(initial='1', choices=VASTA_LEVELS, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        self.set_settings()
        self.set_default_data()
        self.default_data['gametype'] = 'qa',
        super(VastaSettings, self).__init__(*args, **kwargs)

class VastaQuestion(OahpaQuestion):
    """
    Questions for vasta
    """

    select_words = select_words
    vasta_is_correct = vasta_is_correct
        
    def __init__(self, question, qwords, language, userans_val, correct_val, *args, **kwargs):                 

        self.init_variables("", userans_val, [])
        
        question_widget = forms.HiddenInput(attrs={'value' : question.id})

        super(VastaQuestion, self).__init__(*args, **kwargs)

        maxlength=50
        answer_size=50
        self.fields['answer'] = forms.CharField(max_length = maxlength, \
                                                widget=forms.TextInput(\
            attrs={'size': answer_size, 'onkeydown':'javascript:return process(this, event, document.gameform);',}))

        self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)

        self.qattrs= {}
        for syntax in qwords.keys():
            qword = qwords[syntax]
            if qword.has_key('word'):
                self.qattrs['question_word_' + syntax] = qword['word']
            if qword.has_key('tag') and qword['tag']:
                self.qattrs['question_tag_' + syntax] = qword['tag']
            if qword.has_key('fullform') and qword['fullform']:
                self.qattrs['question_fullform_' + syntax] = qword['fullform'][0]

        # Forms question string and answer string out of grammatical elements and other strings.
        qstring = ""

        # Format question string
        qtext = question.string
        for w in qtext.split():
            if not qwords.has_key(w): qstring = qstring + " " + force_unicode(w)
            else:
                if qwords[w].has_key('fullform'):
                    qstring = qstring + " " + force_unicode(qwords[w]['fullform'][0])
                else:
                    qstring = qstring + " " + w
        # this is for -guovttos
        qstring=qstring.replace(" -","-");
        qstring=qstring.replace("- ","-");
                    
        # Remove leading whitespace and capitalize.
        qstring = qstring.lstrip()
        qstring = qstring[0].capitalize() + qstring[1:]

        qstring = qstring + "?"
        self.question=qstring

        # In qagame, all words are considered as answers.
        self.gametype="vasta"
        self.messages, jee, joo  = self.vasta_is_correct(qstring.encode('utf-8'), qwords, language)
        
        # set correct and error values
        if correct_val == "correct":
            self.error="correct"


def sahka_is_correct(self,utterance,targets,language):
    """
    Analyzes the answer and returns a message.
    """
    if not self.is_valid():
        return False

    if not self.cleaned_data.has_key('answer'):
        return
    qwords = {}
    # Split the question to words for analaysis.

    self.messages, self.dia_messages, self.variables = self.vasta_is_correct(utterance.utterance, None, language, utterance.name)
    #self.variables = [ "Kárášjohka" ]
    #self.dia_messages = [ "dia-unknown" ]

    if not self.messages:
        self.error = "correct"

    for answer in self.dia_messages:
        answer = answer.lstrip("dia-")
        if answer == "target":
            self.target = answer

    
class SahkaSettings(OahpaSettings):

    #dialogue = forms.ChoiceField(initial='firstmeeting', choices=DIALOGUE_CHOICES, widget=forms.Select)
    
    def __init__(self, *args, **kwargs):
        self.set_settings()
        self.set_default_data()
        self.default_data['gametype'] = 'sahka'
        self.default_data['dialogue_id'] = '1'
        self.default_data['dialogue'] = 'firstmeeting'
        self.default_data['topicnumber'] = '0'
        self.default_data['image'] = 'sahka.png'
        self.default_data['wordlist'] = ''
        super(SahkaSettings, self).__init__(*args, **kwargs)

        # Link to grammatical explanation for each page
        self.grammarlinkssme = Grammarlinks.objects.filter(language="sme")
        self.grammarlinksno = Grammarlinks.objects.filter(language="no")

    def init_hidden(self, topicnumber, num_fields, dialogue, image, wordlist):
        
        # Store topicnumber as hidden input to keep track of topics.
        #print "topicnumber", topicnumber
        #print "num_fields", num_fields
        topicnumber = topicnumber
        num_fields = num_fields
        dialogue = dialogue
        image = image
        wordlist = wordlist


class SahkaQuestion(OahpaQuestion):
    """
    Sahka: Dialogue game
    """

    select_words = select_words
    sahka_is_correct = sahka_is_correct
    vasta_is_correct = vasta_is_correct

    def __init__(self, utterance, qwords, targets, global_targets, language, userans_val, correct_val, *args, **kwargs):                 
        
        self.init_variables("", userans_val, [])

        utterance_widget = forms.HiddenInput(attrs={'value' : utterance.id})        
        
        super(SahkaQuestion, self).__init__(*args, **kwargs)

        if utterance.utttype == "question":
            maxlength=50
            answer_size=50
            self.fields['answer'] = forms.CharField(max_length = maxlength, \
                                                    widget=forms.TextInput(\
            attrs={'size': answer_size, 'onkeydown':'javascript:return process(this, event, document.gameform);',}))

        self.fields['utterance_id'] = forms.CharField(widget=utterance_widget, required=False)

        self.global_targets = global_targets
        #print self.global_targets
        self.utterance =""
        self.qattrs={}

        if utterance:
            self.utterance_id=utterance.id
            #self.utterance=utterance.utterance

            # Forms question string and answer string out of grammatical elements and other strings.
            qstring = ""
            
            # Format question string
            qtext = utterance.utterance
            for w in qtext.split():
                if not qwords.has_key(w):
                    qstring = qstring + " " + force_unicode(w)
                    self.qattrs['question_fullform_' + w] = force_unicode(w)
                else:
                    if qwords[w].has_key('fullform'):
                        qstring = qstring + " " + force_unicode(qwords[w]['fullform'][0])
                        self.qattrs['question_fullform_' + w] = qwords[w]['fullform'][0]
                    else:
                        qstring = qstring + " " + w
                        self.qattrs['question_fullform_' + w] = w

            # this is for -guovttos
            qstring=qstring.replace(" -","-");
            qstring=qstring.replace("- ","-");
                    
            # Remove leading whitespace and capitalize.
            qstring=qstring.replace(" .",".");
            qstring=qstring.replace(" ?","?");
            qstring=qstring.replace(" !","!");

            qstring = qstring.lstrip()
            if len(qstring)>0:
                qstring = qstring[0].capitalize() + qstring[1:]

            self.utterance=qstring

        self.target=""
        self.constant=""
        self.dia_messages = ""        
        self.gametype="sahka"
        self.variables = []
        self.variables.append("")
        self.variables.append("")
        self.sahka_is_correct(utterance,targets,language)
        if self.target:
            variable=""
            constant=""
            if utterance.links.filter(target=self.target).count()>0:
                variable = utterance.links.filter(target=self.target)[0].variable
                if variable:
                    self.qattrs['target_' + variable] = self.variables[0]
                    self.global_targets[variable] = { 'target' : self.variables[0] }
                constant = utterance.links.filter(target=self.target)[0].constant
                if constant:
                    self.qattrs['target_' + constant] = self.variables[1]
                    self.global_targets[constant] = { 'target' : self.variables[1] }
        for t in self.global_targets.keys():
            if not self.qattrs.has_key(t):
                self.qattrs['target_' + t] = self.global_targets[t]['target']

        #self.error="correct"
        self.errormsg = ""

        if correct_val == "correct":
            self.error="correct"

