﻿import settings
from settings import OLD_NEW_ISO_CODES as ISO

def switch_language_code(CODE):
	"""
		Switches language codes from ISO 639-1 to ISO 639-2.
		
		>>> switch_language_code("no")
		"nob"
		
	"""
	try:
		return ISO[CODE]
	except:
		# logger.warning("*** Unidentified language code %s." % CODE)
		# print >> sys.stdout, "*** Unidentified language code %s." % CODE
		return settings.LANGUAGE_CODE
	

