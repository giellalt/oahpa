from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import sys

# # # 
# 
#  Command class
#
# # #

word_attrs = [
	"id",
	"lemma",
	"pos",
	"language",
	"presentationform",
	"stem",
	"wordclass",
	"valency",
	"hid",
	"diphthong",
	"gradation",
	"rime",
	"attrsuffix",
	"compsuffix",
	"soggi",
	"compare",
	"frequency",
	"geography",
	"tcomm",
]

###	"semtype",
###	"dialects",
###	"source",


def printword(word_key):
	from univ_drill.models import Word
	ws = Word.objects.filter(lemma=word_key)

	for w in ws:
		forms = w.form_set.all()

		for attr in word_attrs:
			v = w.__getattribute__(attr)
			if v:
				print "%s:\t%s" % (attr, v)

		print 'Wordforms: %d forms generated\n' % forms.count()
		for form in w.form_set.all():
			dialects = form.dialects.all().values_list('dialect', flat=True)
			if len(dialects) > 0:
				dialects = ', '.join(dialects)
			else:
				dialects = ""
			print "\t%s\t\t%s\t\t%s" % (form.tag.string, form.fullform, dialects)

		print '\nQuestion membership:'
		question_memberships = w.wordqelement_set.all().values_list(
			'qelement__question__qid',
			'qelement__question__question__qid', 
			'qelement__question__qatype')

		for q_m in question_memberships:
			q_ms = ' - '.join([q for q in q_m[::-1] if q])
			print '\t' + q_ms

		print "--"


class Command(BaseCommand):
	args = '--tagelement'
	help = """
	Search for word forms with missing feedback messages
	"""
	option_list = BaseCommand.option_list + (
		make_option("-w", "--word", dest="word_key", default=False,
						  help="Tag element to search for"),
	)

	def handle(self, *args, **options):
		import sys, os

		printword(options['word_key'])


