# -*- encoding: utf-8 -*-
# This is a temporary solution until I figure out the right way of
# getting Babel to compile strings out of app.config.yaml

# Here are all the names of the languages used in dictionaries, for
# internationalization.
from flaskext.babel import lazy_gettext as _
NAMES = dict([
    # sanit
    ('sme', _(u"North Sámi")),
    ('SoMe', _(u"North Sámi (#SoMe)")),

    # baakoeh
    ('sma', _(u"South Sámi")),

    # kyv
    ('kpv', _(u"Komi")),

    # sanat
    ('fkv', _(u"Kven")),
    ('liv', _(u"Livonian")),
    ('olo', _(u"Olonetsian")),
    ('izh', _(u"Izhorian")),

    # valks
    ('myv', _(u"Erzya Mordvin")),

    # target languages
    ('fin', _(u"Finnish")),
    ('nob', _(u"Norwegian")),

    ('ru', _(u"Russian")),
    ('rus', _(u"Russian")),

    ('fi', _(u"Finnish")),
    ('no', _(u"Norwegian")),
    ('nob', _(u"Norwegian")),
    ('lv', _(u"Latvian")),
    ('eng', _(u"English")),
])

LOCALISATION_NAMES_BY_LANGUAGE = dict([
    ('sme', u"Davvisámegiella"),
    ('sma', u"Åarjelsaemien"),
    ('ru', u"Руский"),
    ('olo', u"olo"),
    ('no', u"Norsk"),
    ('myv', u"myv"),
    ('lv', u"lv"),
    ('liv', u"liv"),
    ('kpv', u"kpv"),
    ('izh', u"izh"),
    ('fkv', u"fkv"),
    ('fi', u"Suomi"),
    ('eng', u"English"),
])

# Only put the exceptional ISOs here
ISO_TRANSFORMS = dict([
    ('se', 'sme'),
    ('no', 'nob'),
    ('fi', 'fin'),
    ('en', 'eng'),
])
