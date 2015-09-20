# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.db.models import Q, Count
from random import randint

from models import *
from forms import *
from game import Game

import crk_oahpa.settings as settings

try:
	DEFAULT_DIALECT = settings.DEFAULT_DIALECT
except:
	DEFAULT_DIALECT = None
class CealkkaGame(Game):

	test = 0
	
	def __init__(self, *args, **kwargs):
		super(CealkkaGame, self).__init__(*args, **kwargs)
		self.init_tags()
	
	def init_tags(self):
		"""
		Initialize the grammatical information.
		This information should be moved to parameters
		"""
		self.num_fields = 3
		self.syntax =('MAINV','SUBJ','HAB')
		self.qtype_verbs = set(['V-COND','V-IMPRT','V-POT', 'PRS','PRT', 'V-PRS', 'V-PRT', 'V-GER', 'V-PRF'])

		# Default tense and mood for testing
		self.tense = "Prs"
		self.mood = "Ind"
		self.gametype = "cealkka" 
				
		# TODO: check this in smeoahpa, possible source of error.
		# Values for pairs QPN-APN
		
		# spørsmål:   svar:
		# mun         don
		# don         mun
		# son         son
        # 
		# moai 		  doai
		# doai        moai
		# soai        soai
        # 
		# mii         dii
		# dii         mii
		# sii		  sii
        # 
		# Noun Sg 	son
		# Noun Pl   sii
		
		self.QAPN={	'Sg':'Sg',			#  
					'Pl':'Pl',			#  
					
					'Sg1':'Sg2',		# Mun? Don.
					'Sg2':'Sg1',		# Don? Mun.
					'Sg3':'Sg3',		# Son? Son.
					
					'Du1':'Du2',		# Moai? Doai.
					'Du2':'Du1',		# Doai? Moai.
					'Du3':'Du3',		# Soai? Soai.
					
					'Pl1':'Pl2',		# Mii? Dii.
					'Pl2':'Pl1',		# Dii? Mii.
					'Pl3':'Pl3'}		# Sii? Sii.
					
					

		# Values for subject-verb agreement:
		# e.g. Subject with N+Sg+Nom requires verb with Sg3.
		self.SVPN={'Sg1':'Sg1','Sg2':'Sg2','Sg3':'Sg3','Sg':'Sg3',\
				   'Pl1':'Pl1','Pl2':'Pl2','Pl3':'Pl3','Pl':'Pl3',\
				   'Du1':'Du1','Du2':'Du2','Du3':'Du3'}

		# Available values for Number
		self.PronPN=['Sg1','Sg2','Sg3','Pl1','Pl2','Pl3','Du1','Du2','Du3']
		self.PronPNBase={'Sg1':'mun','Sg2':'don','Sg3':u'son',\
						 'Pl1':'mii','Pl2':'dii','Pl3':'sii',\
						 'Du1':'moai','Du2':'doai','Du3':'soai'}
		self.NounPN=['Sg','Pl']
		self.NountoPronPN={'Sg':'Sg3','Pl':'Pl3'}

	def get_qword(self, qelement, tag_el):
		"""
			Note: attempting to reduce amount of queries run here, there are still some that are repeated,
				  but these should reduced once we come along to testing numbers.
		"""
		if self.settings.has_key('dialect'):
			dialect = self.settings['dialect']
		else:
			dialect = DEFAULT_DIALECT

		word=None
		if tag_el.pos=="Num" and self.settings.has_key('num_level') and str(self.settings['num_level'])=="1":
			smallnum = ["1","2","3","4","5","6","7","8","9","10"]
		word = Word.objects.filter(wordqelement__qelement=qelement,
									 form__tag=tag_el.id)
		if word.count() > 0:
			word = word.order_by('?')[0]
		else:
			# Dialect is commented out still because we're only getting
			# dialectical form variants, not word variants.
			possible_words = Word.objects.filter(wordqelement__qelement=qelement,
												# dialects__dialect=dialect,
												form__tag=tag_el.id)
			if possible_words.count() > 0:
				word = possible_words.order_by('?')[0]

		form_set_filter = word.form_set.filter(tag=tag_el.id)

		# filter forms by dialect
		form_set_filter_dial = form_set_filter\
									.exclude(dialects__dialect='NG')\
									.filter(dialects__dialect=dialect)

		if form_set_filter_dial.count() > 0:
			form_set_filter = form_set_filter_dial

		if word and form_set_filter.count()>0:
			form = form_set_filter[0] 
		else: raise Form.DoesNotExist("No words found.")
		# return None
		# TODO: better error handling here-- this needs to point out
		# that the DB is not installing properly, but I need to check
		# first that the code doesn't depend on returning None
		# sometimes.
		# Test by raising Form.DoesNotExist? 
		word_id = word.id
		fullform = form.fullform
			
		info = { 'word' : word_id, 'tag' : tag_el.id, 'fullform' : [ fullform ], 'qelement' : qelement }
		return info
	
	# Select a word matching semtype and return full form.
	def get_words(self, qelement, tag_el=None, lemma=None, word_id=None):
		"""
		Select word from possible options in the element.
		"""
		words = []

		if self.settings.has_key('dialect'):
			dialect = self.settings['dialect']
		else:
			dialect = DEFAULT_DIALECT
		
		# If there are no information available for these elements, try to use other info.
		word = None
		form = None
				
		if lemma and tag_el:
			form_set = tag_el.form_set.exclude(dialects__dialect='NG')
			dialect_forms = form_set.filter(dialects__dialect=dialect)
			if dialect_forms.count() > 0:
				form_set = dialect_forms

			if qelement:
				if qelement.semtype:
					form_set = form_set.filter(word__semtype=qelement.semtype)
			form = form_set[0]
		else:
			if word_id and tag_el:
				###		word_set = Word.objects.filter(id=word_id)
				###		if qelement:
				###			if qelement.semtype:
				###				word_set.filter(semtype=qelement.semtype)
				###		word = word_set[0]

				word = Word.objects.get(id=word_id)
				# if qelement:
					# if qelement.semtype:
						# word_set.filter(semtype=qelement.semtype)

				# word = word_set[0]

				form_set = word.form_set.filter(tag=tag_el)

				excl = form_set.exclude(dialects__dialect='NG')

				if excl.count() > 0:
					form_set = excl

				dialect_forms = form_set.filter(dialects__dialect=dialect)

				if dialect_forms.count() > 0:
					form_set = dialect_forms

				form = form_set[0]

		
		if form:
			fullform = form.fullform
			info = {'word': form.word.id, 'tag': tag_el.id, 'fullform': [ fullform ]}
			words.append(info)
		elif word:
			form_list = word.form_set.exclude(dialects__dialect='NG')

			filtered = form_list.filter(dialects__dialect=dialect)
			
			if filtered.count() > 0:
				form_list = filtered

			if tag_el:
				form_list = form_list.filter(tag=tag_el)
			# We do not want to filter by dialect here, because we want
			# all forms to be accepted regardless of dialect
			if not form_list:
				if self.test: raise Http404(qelement.id + " " + tag_el.id + " " + word.id)
				return []

			fullform = form_list[0].fullform

			info = {'word': word.id, 'tag' : tag_el.id, 'fullform' : [ fullform ] }
			words.append(info)					
		else:
			if self.test: raise Http404("not word " + str(qelement.id))			
			return []
		
		return words

	def get_elements(self, question_element, identifier):
		elements = QElement.objects.filter(question=question_element, 
											identifier=identifier)
		if elements.count() > 0:
			return elements
		else:
			return None
		

	def generate_question(self, question, qtype):
		"""
		Generate question for the form.
		Only one question is generated.
		"""
		qtext=question.string
		#print "QUESTION " + str(question.id) + " " + qtext
		qwords = {}
	
		# Find out syntax elements
		qwords_list=[]
		for w in qtext.split():
			if w== "": continue
			qwords_list.append(w)

		# Handle all grammatical elements one at the time
		# 1. SUBJ-MAINV argreement
		#if self.test: raise Http404(question.id,qwords_list)
		# print qwords_list
		if 'SUBJ' in set(qwords_list):
			qwords['SUBJ'] = {}
			
			# Select randomly an element, if there are more than one available.
			# This way there is only one subject and tag for each question.
			subj_elements=self.get_elements(question, 'SUBJ')
			
			if not subj_elements:
				return None
			subj_el = subj_elements[randint(0, len(subj_elements)-1)]
			tag_el_count = subj_el.tags.count()
			
			# If there was no tag elements, there is nothing to do.
			# Subject tag is needed for everything else. 
			if tag_el_count == 0:
				if self.test: raise Http404("0 tag count" + " " + qwords_list)
				return None
			
			tag_el = subj_el.tags.all()[randint(0, tag_el_count-1)]
			# Get number information for subject
			subjword = {}
			if tag_el.pos == "Pron":
				subjnumber = tag_el.personnumber
				if not subjnumber:
					raise Http404("Tag Element missing personnumber. Database may be improperly installed for tags.")
				pronbase = self.PronPNBase[subjnumber]
				word_el = Word.objects.filter(lemma=pronbase)[0]
				words_ = self.get_words(None, tag_el, None, word_el.id)
				try:
					info = words_[0]
				except IndexError:
					info = False
				# print subjnumber
				# print pronbase
				# print word_el
				# print info
				# print '--'
			else:
				subjnumber = tag_el.number
				info = self.get_qword(subj_el, tag_el)

			if not info:
				if self.test: raise Http404("not info " + " ".join(qwords_list))
				return None
			
			subjword = info
			subjword['number'] = subjnumber
			qwords['SUBJ'] = subjword
			# print qwords['SUBJ']

		if 'HAB' in set(qwords_list):
			
			qwords['HAB'] = {}
			
			# Select randomly an element, if there are more than one available.
			# This way there is only one habect and tag for each question.
			hab_elements = self.get_elements(question, 'HAB')
			
			if not hab_elements:
				return None
			hab_el = hab_elements[randint(0, len(hab_elements)-1)]
			tag_el_count = hab_el.tags.count()
			
			# If there was no tag elements, there is nothing to do.
			# Subject tag is needed for everything else. 
			if tag_el_count == 0:
				if self.test: raise Http404("0 tag count" + " " + qwords_list)
				return None
			
			tag_el = hab_el.tags.all()[randint(0, tag_el_count-1)]
			
			# Get number information for habect
			habword = {}
			if tag_el.pos == "Pron":
				habnumber = tag_el.personnumber
				pronbase = self.PronPNBase[habnumber]
				word_el = Word.objects.filter(lemma=pronbase)[0]
				words_ = self.get_words(None, tag_el, None, word_el.id)
				try:
					info = words_[0]
				except IndexError:
					info = False
				# print habnumber
				# print pronbase
				# print word_el
				# print info
				# print '--'
			else:
				habnumber = tag_el.number
				info = self.get_qword(hab_el, tag_el)

			if not info:
				if self.test: raise Http404("not info " + " ".join(qwords_list))
				return None
			habword = info
			habword['number'] = habnumber
			qwords['HAB'] = habword
			# print qwords['SUBJ']

		if 'MAINV' in set(qwords_list):

			qwords['MAINV'] = {}
			mainv_word = None
			
			# Select one mainverb element for question.
			mainv_elements = self.get_elements(question,'MAINV')
			if mainv_elements:
				mainv_el = mainv_elements[randint(0, len(mainv_elements)-1)]
				
				# If there is only on tag element, then there are no choices for agreement.
				tag_el_count = mainv_el.tags.count()
				if tag_el_count == 1:
					tag_el=mainv_el.tags.all()[0]
				else:
					# Subject-verb agreement
					if qwords.has_key('SUBJ') and qwords['SUBJ'].has_key('number'):
						subjnumber=qwords['SUBJ']['number']
						v_number = self.SVPN[subjnumber]

						if qtype in self.qtype_verbs or self.gametype=="qa":
							mainv_tags = mainv_el.tags.filter(Q(personnumber=v_number))
						else:
							mainv_tags = mainv_el.tags.filter(Q(personnumber=v_number) & \
															Q(tense=self.tense) & \
															Q(mood=self.mood))
					# If there is no subject element
					# then select random tag from all tags.
					else:
						mainv_tag_count = mainv_el.tags.count()
						mainv_tags = mainv_el.tags.all()
					if not mainv_tags:
						if self.test: raise Http404("not mainv_tags " + " ".join(qwords_list) + " " + question.qid)
						return None
					tag_el = mainv_tags[randint(0, mainv_tags.count()-1)]

				# Select random mainverb
				info = self.get_qword(mainv_el, tag_el)
				mainv_word = info

				if not mainv_word:
					if self.test: raise Http404("not mainv_word " + " ".join(qwords_list) + " " + question.qid)
					return None
				else:
					mainv_word['number'] = tag_el.personnumber
					qwords['MAINV'] = mainv_word

			if not mainv_word:
				if self.test: raise Http404("not mainv" + " " + " ".join(qwords_list))
				return None
				
		# 2. Other grammatical elements
		# At the moment, agreement is not taken into account
		for s in qwords_list:
			if s in set(self.syntax): continue

			tag_el=None
			word = {}
			anumber = ""			
			elements = self.get_elements(question,s)
			if elements:
				element = elements[randint(0, len(elements)-1)]
				copy_id=element.copy_id
				if copy_id:
					copy = QElement.objects.filter(id=copy_id)[0]
					copy_syntax = copy.syntax
					
					if qwords.has_key(copy_syntax):
						word = qwords[copy_syntax]

				if element.agreement:
					agr_id = element.agreement_id
					agr_el = QElement.objects.get(id=agr_id)
					agr_syntax = agr_el.identifier
					if qwords.has_key(agr_syntax):
						qword = qwords[agr_syntax]
						if qword.has_key('tag'):
							agr_tag_id = qword['tag']
							agr_tag = Tag.objects.get(id=agr_tag_id)
							if agr_tag.personnumber:
								anumber = agr_tag.personnumber
							else:
								anumber = agr_tag.number
							tag_count = element.tags.filter(Q(personnumber=anumber) | Q(number=anumber)).count()
							if tag_count>0:
								tag_el = element.tags.filter(Q(personnumber=anumber) | Q(number=anumber))[randint(0, tag_count-1)]
				if not tag_el: 
					tag_el_count = element.tags.count()
					if tag_el_count > 0:
						tag_el = element.tags.order_by('?')[0]

				if tag_el:
					# Select random word
					info = self.get_qword(element, tag_el)
					word = info					
			else:
				word = {}
				info = {'fullform' : [ s ] }
				word = info

			if not word:
				if self.test: raise Http404("not word " + "".join(qwords_list))
				return None
			qwords[s] = word

		# Return the ready qwords list.			
		return qwords

	def generate_answers_subject(self, answer, question, awords, qwords, element="SUBJ"):
		""" Can be used to generate answers for habitive, just supply element="HAB"
		"""
		words=[]
		word_id=""
		a_number=""
		subj_el = None
		subjword = None

		copy_syntax = ""
		# If there is subject in the question, there is generally agreement.
		subj_elements = self.get_elements(answer,element)
		if subj_elements:
			subj_el = subj_elements[0]
		
		copy_id = subj_el.copy_id
		
		if subj_el.copy:
			subj_copy = subj_el.copy
			copy_syntax = subj_copy.syntax
			if qwords.has_key(copy_syntax):
				qword = qwords[copy_syntax]

				subjtag_id = qword['tag']
				subjtag = Tag.objects.get(id=subjtag_id)
				subjword_id = qword['word']

				if subjtag.pos == "Pron":
					subjnumber = subjtag.personnumber
				else:
					subjnumber = subjtag.number
				
				# this should only happen if there's subj person
				a_number = self.QAPN[subjnumber]
				asubjtag = subjtag.string.replace(subjnumber, a_number)
				asubjtag_el = Tag.objects.get(string=asubjtag)
				
				# If pronoun, get the correct form
				if self.PronPNBase.has_key(a_number):
					pronbase = self.PronPNBase[a_number]
					words = self.get_words(None, asubjtag_el, pronbase)
					for word in words:
						word['number'] = a_number
					
				if not words and not len(words)>0:
					words = self.get_words(subj_copy, asubjtag_el, None, subjword_id)
					words[0]['number'] = a_number

		# Check if there are elements specified for the answer subject.
		else:
			if subj_el:
				tag_el_count = subj_el.tags.count()
				word_el_count = subj_el.wordqelement_set.count()
				
				if tag_el_count > 0:
					tag_el = subj_el.tags.all().order_by('?')[0]

				if tag_el.pos=="Pron":
					a_number = tag_el.personnumber
				else:
					a_number = tag_el.number
				
				if not subjword:
					subjword = subj_el.wordqelement_set\
									.filter(word__form__tag=tag_el)\
									.order_by('?')[0].word.id

				info = { 'qelement': subj_el.id, 'word' : subjword, 'tag' : tag_el.id, 'number' : a_number }
				words.append(info)

				for word in words:
					word['number'] = a_number
		
		awords[element] = words[:]
		
		# If SUBJ is appearing in the output, this means subjword is set to none for some reason.
		# subjword is set to none because subj_el.copy_id is none
		return awords

	
	def generate_answers_mainv(self, answer, question, awords, qwords):

		mainv_elements = self.get_elements(answer,"MAINV")
		# print '--'
		# print question.qid
		# print mainv_elements
		mainv_word=None
		mainv_words = []
		mainv_tag = None
		mainv_tags = []
		va_number = None

		copy_syntax = ""
		# Find content elements.
		if mainv_elements:
			mainv_el = mainv_elements[0]
			if mainv_el.copy_id:
				copy_id = mainv_el.copy_id
				copy_element = QElement.objects.get(id=copy_id)
				copy_syntax = copy_element.identifier
		# It is assumed that all subjects cause the same inflection
		# for verb, so it does not matter which subject is selected.
		if awords.has_key('SUBJ') and len(awords['SUBJ'])>0:
			# mainverb number depends on the number of the subject.
			asubj = awords['SUBJ'][0]
			a_number=asubj['number']
			# print 'asubj number: ', a_number
			va_number=self.SVPN[a_number]
			# print 'va_number: ', va_number
		else:
            # No SUBJ defined, MAINV is a copy of the question MAINV
            # and needs to have Question-Answer subject change
			if qwords.has_key(copy_syntax):
				qmainv = qwords[copy_syntax]
				q_number = qmainv['number']
				if q_number:
					va_number = self.QAPN[q_number]
			else:
				# No SUBJ defined, and MAINV is defined (and not a copy from Q)
                # but MAINV still needs to have Question-Answer subject change
				if qwords.has_key('MAINV'):
					qmainv = qwords['MAINV']
					q_number = qmainv['number']
					if q_number:
						va_number = self.QAPN[q_number]
					
		# If there is no subject, then the number of the question
		# mainverb determines the number.
		mainv_fullform = False
		mainv_form = False
		mainv_word_obj = None
		if qwords.has_key(copy_syntax):

			qmainv = qwords[copy_syntax]
			mainv_word = qwords[copy_syntax]['word']

			qmainvtag_id = qmainv['tag']
			qmainvtag = Tag.objects.get(id=qmainvtag_id)
			qmainvtag_string = qmainvtag.string
			v_number = qmainvtag.personnumber
			if va_number:
				amainvtag_string = qmainvtag_string.replace(v_number,va_number)
			else:
				amainvtag_string = qmainvtag_string
				
			mainv_tag = Tag.objects.get(string=amainvtag_string)
			mainv_tags.append(mainv_tag)
			
			mainv_word_obj = Word.objects.get(id=mainv_word)
			try:
				mainv_form = mainv_word_obj.form_set.filter(tag__string=mainv_tag).order_by('?')[0]
			except IndexError:
				error_vars = ('generate_answers_mainv', 
								mainv_word_obj,
								mainv_word_obj.pk,
								mainv_tag.string,
								mainv_word_obj.form_set.all().count())
				error = "%s: Word <%s, id: %d> missing form for Tag <%s> (%d total form(s) available). \r\n" % error_vars
				# error += '\r\n'.join([form.tag.string for form in mainv_word_obj.form_set.all()])
				raise Http404(error)

			mainv_fullform = mainv_form.fullform

		# If the main verb is under question, then generate full list.
		if answer.task == "MAINV":
			mainv_words = []
			if mainv_elements:
				for mainv_el in mainv_elements:
					if mainv_el.tags.count()>0:
						if va_number:
							# print va_number
							mainv_tags = mainv_el.tags.filter(Q(personnumber=va_number))
						else:
							mainv_tags = mainv_el.tags.all()
						for t in mainv_tags:
							info = {'qelement': mainv_el.id, 
									'tag': t.id}
							if mainv_fullform and mainv_word and mainv_tag:
								info['fullform'] = [mainv_fullform]
								info['word'] = mainv_word
								info['number'] = mainv_tag.personnumber
							mainv_words.append(info)
					else:
						info = { 'qelement' : mainv_el.id, 'tag' : mainv_tag.id }
						mainv_words.append(info)

			else:
				if mainv_word:
					mainv_words.extend(self.get_words(mainv_el, mainv_tag, None, mainv_word))
					
		# Otherwise take only one element
		else:
			if mainv_elements:
				mainv_element = mainv_elements[0]
				tag_el_count = mainv_element.tags.count()
				if tag_el_count > 0:
					mainv_tags = mainv_el.tags.filter(Q(personnumber=va_number))
				for tag in mainv_tags:
					info = { 'qelement' : mainv_element.id, 'word' : mainv_word, 'tag' : tag.id }
					mainv_words.append(info)

			else:
				for tag in mainv_tags:
					info = { 'tag' : mainv_tag.id, 'word' : mainv_word }
					mainv_words.append(info)
					
		if not mainv_words and qwords.has_key("MAINV"):
			mainv_words.append(qwords["MAINV"])
		
		awords["MAINV"] = mainv_words
		
		return awords

	def generate_syntax(self, answer, question, awords, qwords, s):

		
		if s in ["SUBJ", "MAINV", "HAB"]: return awords
		
		if not awords.has_key(s):
			awords[s] = []

		word_id=None
		
		tag_elements = []
		swords = []
		elements = self.get_elements(answer,s)

		if not elements:
			info = { 'fullform' : [ s ] }
			swords.append(info)
			awords[s] = swords
			return awords

		element = elements[0]
		if element.copy_id:
			copy_id = element.copy_id
			copy_element = QElement.objects.get(id=copy_id)
			copy_syntax = copy_element.identifier
			if qwords.has_key(copy_syntax):
				qword = qwords[copy_syntax]
				if qword.has_key('word'):
					word_id=qword['word']
				if qword.has_key('tag'):
					tag = Tag.objects.get(id=qword['tag'])
					tag_elements.append(tag)

		if element.agreement:
			agr_id = element.agreement_id
			agr_el = QElement.objects.get(id=agr_id)
			agr_syntax = agr_el.identifier
			if qwords.has_key(agr_syntax):
				qword = qwords[agr_syntax]
				if qword.has_key('tag'):
					agr_tag_id = qword['tag']
					agr_tag = Tag.objects.get(id=agr_tag_id)
					if agr_tag.personnumber:
						anumber = agr_tag.personnumber
					else:
						anumber = agr_tag.number
					tag_count = element.tags.filter(Q(personnumber=anumber) | Q(number=anumber)).count()
					if tag_count>0:
						tag_elements = element.tags.filter(Q(personnumber=anumber) | Q(number=anumber))

		# if no agreement, take all tags.
		else:
			tag_count = element.tags.count()
			if tag_count > 0:
				tag_elements = element.tags.all()
		
		# Take word forms for all tags
		info=None
		for tag_el in tag_elements:
			if not word_id:
				info = self.get_qword(element, tag_el)
			else:
				form_list = Form.objects.filter(Q(tag=tag_el.id) & Q(word=word_id))
				if form_list:
					info = { 'qelement' : element.id, 'word' : word_id, 'tag' : tag_el.id  }
			if not info:
				if self.test: raise Http404("not info " + question.id)
				return None
			swords.append(info)

		if not swords:
			if self.test: raise Http404("not swords " + str(question.id) + " " + s + str(element.id))
			return None
		awords[s] = swords

		return awords

	######### Cealkka questions
	def get_question_cealkka(self,db_info,qtype):

		qwords = {}
                if self.settings.has_key('level') and self.settings['level'] not in ['All','all']: 
                    level=int(self.settings['level'])
                else: # default level was set to 'all', but I could not find where
                    level=1
                #if self.settings.has_key('lemmacount'):  # added by Heli
                 #   lemmacount=int(self.settings['lemmacount'])
                #else:
                 #   lemmacount=2		
		q_count = Question.objects.filter(gametype="cealkka", level__lte=level).count()
		question = Question.objects.filter(gametype="cealkka", level__lte=level)[randint(0,q_count-1)]  # removed lemmacount filter lemmacount=lemmacount
		#print level
		#print lemmacount 
		#question = Question.objects.get(id="107")
	   
		qtype = question.qtype
		qwords = None
		qwords= self.generate_question(question, qtype)
		db_info['qwords'] = qwords

		db_info['question_id'] = question.id
		return db_info,question

	########### Cealkka answers (like morfa)
	def get_answer_morfa(self,db_info,question):
		
		# Select answer that is related to the question.
		awords = {}
		if db_info.has_key('answer_id'):
			answer=Question.objects.get(id=db_info['answer_id'])
		else:
			answer=question.answer_set.all().order_by('?')[0]

		# Generate the set of possible answers if they are not coming from the interface
		# Or if the gametype is qa.
		if db_info.has_key('answer_id') and self.settings['gametype'] == 'cealkka':
			awords=db_info['awords']
			print awords
		else:
			# Generate the set of possible answers
			# Here only the text of the first answer is considered!!
			atext=answer.string
			words_strings = set(atext.split())
			#Initialize each element identifier
			for w in atext.split():
				if w== "": continue
				info = {}
				awords[w] = info
			# Subject and main verb are special cases:
			# There is subject-verb agreement and correspondence with question elements.
			if 'SUBJ' in words_strings:
				awords = self.generate_answers_subject(answer, question, awords, db_info['qwords'])
				
			if 'HAB' in words_strings:
				awords = self.generate_answers_subject(answer, question, awords, db_info['qwords'], element="HAB")

			if 'MAINV' in words_strings:
				try:
					awords = self.generate_answers_mainv(answer, question, awords, db_info['qwords'])
				except AttributeError:
					if self.test: raise Http404("problem")
					return "error"

			# Rest of the syntax
			#if self.test: raise Http404(words_strings)
			for s in words_strings:
				awords = self.generate_syntax(answer, question, awords, db_info['qwords'], s)
				if not awords:
					if self.test: raise Http404("problem" + s)
					return "error"
				if not awords.has_key(s):
					if self.test: raise Http404("problem2" + s)
					return "error"

		db_info['answer_id'] = answer.id
		db_info['awords'] = awords
		# print db_info
#		 raise Exception(db_info)
		# print db_info['awords']
		# print question.string
		return db_info

	def get_db_info(self, db_info,qtype=None,default_qid=None):
		anslist=[]

		# If the question id is received from the interface, use that question info
		# Otherwise select random question
		if db_info.has_key('question_id'):
			question = Question.objects.get(id=db_info['question_id'])
			qwords=db_info['qwords']
		else:
			if default_qid:
				question = Question.objects.get(qid=default_qid)	  
				qwords = None
				qwords= self.generate_question(question, qtype)
				db_info['qwords'] = qwords

			# If no default information select question
			else:
				db_info,question = self.get_question_cealkka(db_info,qtype)
				
		db_info = self.get_answer_morfa(db_info,question)

		return db_info

	def create_form(self, db_info, n, data=None):

		question = Question.objects.get(Q(id=db_info['question_id']))
		# print question.string
		answer = None
		if self.settings.has_key('dialect'):
			dialect = self.settings['dialect']
		else:
			dialect = DEFAULT_DIALECT
		# TODO: language setting
		language = "eng"
		if self.settings.has_key('language'):
			language = self.settings['language']

		answer = Question.objects.get(Q(id=db_info['answer_id']))
		#print answer.string

		form = (CealkkaQuestion(question, answer, db_info['qwords'], db_info['awords'], dialect, language, db_info['userans'], db_info['correct'], data, prefix=n))  # added the answer part
			
		print "awords:", db_info['awords']
		#print "awords ...................."
		#print "qwords:", db_info['qwords']
		#print "qwords ...................."

		return form, None

