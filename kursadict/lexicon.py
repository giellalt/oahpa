﻿from lxml import etree

##
##  Lexicon
##
##

class XMLDict(object):
    """ XML dictionary class. Initiate with a file path or an already parsed
    tree, exposes methods for searching in XML.

    Entries are only cleaned resulting in lg/l/text(), lg/l@pos, and
    mg/tg/t/text() with self.cleanEntry. Probably easier to make mixins
    that add to this functionality?

    This is mostly used in lookups for the JSON api, but also for the
    main search view. Thus, editing requires care to not disturb the
    JSON API functionality.

    # TODO: write some tests to ensure that breakage can be found
    # quickly.

    """
    def __init__(self, filename=False, tree=False):
        if not tree:
            print "parsing %s" % filename
            self.tree = etree.parse(filename)
        else:
            self.tree = tree
        self.xpath_evaluator = etree.XPathDocumentEvaluator(self.tree)

        # Initialize XPath queries
        regexpNS = "http://exslt.org/regular-expressions"
        self.lemmaStartsWith = etree.XPath('.//e[starts-with(lg/l/text(), $lemma)]')
        self.lemma = etree.XPath('.//e[lg/l/text() = $lemma]')
        self.lemmaPOS = etree.XPath(
            ".//e[lg/l/text() = $lemma and re:match(lg/l/@pos, $pos, 'i')]",
            namespaces={'re':regexpNS})
        self.lemmaPOSAndType = etree.XPath(
            ".//e[lg/l/text() = $lemma and re:match(lg/l/@pos, $pos, 'i') and lg/l/@type = $_type]",
            namespaces={'re':regexpNS})

    def cleanEntry(self, e):
        l = e.find('lg/l')
        left_text = l.text
        left_pos = l.get('pos')
        ts = e.findall('mg/tg/t')
        right_text = [t.text for t in ts]
        _right_langs = [t.getparent().xpath('@xml:lang') for t in ts]
        if _right_langs:
            right_langs = []
            for _rl in _right_langs:
                if len(_rl) > 0:
                    right_langs.append(_rl[0])
                else:
                    right_langs.append(False)
        else:
            right_langs = []

        return { 'left': left_text
               , 'pos': left_pos
               , 'right': right_text
               , 'lang': right_langs
               }

    def XPath(self, xpathobj, *args, **kwargs):
        # print "Querying: %s" % xpathobj.path
        # print "With: %s, %s" % (repr(args), repr(kwargs))
        return map(self.cleanEntry, xpathobj(self.tree, *args, **kwargs)) or False

    def lookupLemmaStartsWith(self, lemma):
        return self.XPath(self.lemmaStartsWith, lemma=lemma)

    def lookupLemma(self, lemma):
        return self.XPath(self.lemma, lemma=lemma)

    def lookupLemmaPOS(self, lemma, pos):
        return self.XPath(self.lemmaPOS, lemma=lemma, pos=pos)

    def lookupLemmaPOSAndType(self, lemma, pos, _type):
        return self.XPath(self.lemmaPOSAndType, lemma=lemma, pos=pos, _type=_type)

class FrontPageFormat(XMLDict):

    def cleanEntry(self, e):
        l = e.find('lg/l')
        left_text = l.text
        left_pos = l.get('pos')
        tgs = e.findall('mg/tg')

        right_nodes = []
        for tg in tgs:
            re = tg.find('re')
            te = tg.find('te')
            _ex = [ (xg.find('x').text, xg.find('xt').text)
                    for xg in tg.findall('xg') ]
            if len(_ex) == 0:
                _ex = False

            if te is not None:      te = te.text
            else:                   te = ''

            if re is not None:      re = re.text
            else:                   re = ''

            tx = tg.find('t')
            link = True
            if (tx is None) and (te is not None):
                text = te
                te = ''
                link = False
            else:
                text = tx.text

            right_nodes.append({ 'tx': text
                               , 're': ', '.join([a for a in [re, te] if a])
                               , 'link': link
                               , 'examples': _ex
                               })

        _right_langs = [t.xpath('@xml:lang') for t in tgs]
        if _right_langs:
            right_langs = []
            for _rl in _right_langs:
                if len(_rl) > 0:
                    right_langs.append(_rl[0])
                else:
                    right_langs.append(False)
        else:
            right_langs = []

        return { 'left': left_text
               , 'pos': left_pos
               , 'right': right_nodes
               , 'lang': right_langs
               }

class DetailedEntries(XMLDict):
    def cleanEntry(self, e):
        l = e.find('lg/l')
        mg = e.findall('mg')

        def orFalse(l):
            if len(l) > 0:
                return l[0]
            else:
                return False

        # TODO: <re> nodes
        meaningGroups = []
        for tg in e.findall('mg/tg'):
            _ex = [(xg.find('x').text, xg.find('xt').text) for xg in tg.findall('xg')]
            _tg = {
                'translations': [t.text for t in tg.findall('t')],
                'examples': _ex,
                'language': orFalse(tg.xpath('@xml:lang'))
            }
            meaningGroups.append(_tg)

        return {
            'lemma': l.text,
            'pos': l.get('pos'),
            'context': l.get('context'),
            'meaningGroups': meaningGroups,
            'type': l.get('type')
        }

class AutocompleteTrie(XMLDict):

    @property
    def allLemmas(self):
        """ Returns iterator for all lemmas.
        """
        return (e.text for e in self.tree.findall('e/lg/l') if e.text)

    def autocomplete(self, query):
        if not self.trie:
            return []
        else:
            return sorted(list(self.trie.autocomplete(query)))

    def __init__(self, *args, **kwargs):
        super(AutocompleteTrie, self).__init__(*args, **kwargs)

        print "* Preparing autocomplete trie..."
        from trie import Trie
        self.trie = Trie()
        try:
            self.trie.update(self.allLemmas)
        except:
            print "Trie processing error"
            print list(self.allLemmas)
            self.trie = False


class ReverseLookups(XMLDict):
    """

    1. use only entries that have the attribute usage="vd" at entry
    level

    2. don't use entries with reverse="no" at entry level

    3. search by e/mg/tg/t/text() instead of /e/lg/l/text()

    """

    def cleanEntry(self, e):
        ts = e.findall('mg/tg/t')
        ts_text = [t.text for t in ts]
        ts_pos = [t.get('pos') for t in ts]

        l = e.find('lg/l')
        right_text = [l.text]

        return {'left': ts_text, 'pos': ts_pos, 'right': right_text}

    def lookupLemmaStartsWith(self, lemma):
        _xpath = './/e[mg/tg/t/starts-with(text(), "%s")]' % lemma
        return self.XPath(_xpath)

    def lookupLemma(self, lemma):
        _xpath = './/e[mg/tg/t/text() = "%s" and @usage = "vd" and not(@reverse)]'
        return self.XPath(_xpath % lemma)

    def lookupLemmaPOS(self, lemma, pos):
        _xpath = ' and '.join(
            [ './/e[mg/tg/t/text() = "%s"' % lemma
            , '@usage = "vd"'
            , 'not(@reverse)'
            , 'mg/tg/t/@pos = "%s"]' % pos.lower()
            ]
        )
        return self.XPath(_xpath)


# TODO: settings.lexicon?
class Lexicon(object):

    def __init__(self, settings):

        language_pairs = dict(
            [ (k, XMLDict(filename=v))
              for k, v in settings.dictionaries.iteritems() ]
        )

        reverse_language_pairs = {}

        for k, v in settings.reversable_dictionaries.iteritems():
            _key =      (k[0], k[1])
            _reverse  = (k[1], k[0])

            has_root = language_pairs.get(_key)

            if has_root:
                reverse_language_pairs[_reverse] = ReverseLookups(tree=has_root.tree)
            else:
                reverse_language_pairs[_reverse] = ReverseLookups(filename=v)

        language_pairs.update(reverse_language_pairs)

        self.language_pairs = language_pairs
        self.reverse_language_pairs = reverse_language_pairs

        autocomplete_tries = {}
        for k, v in language_pairs.iteritems():
            has_root = language_pairs.get(k)
            if has_root:
                autocomplete_tries[k] = AutocompleteTrie(tree=has_root.tree)

        self.autocomplete_tries = autocomplete_tries


    def detailedLookup(self, _from, _to, lookup, pos, _type=False):
        lexicon = self.language_pairs.get((_from, _to), False)
        if not lexicon:
            raise Exception("Undefined language pair %s %s" % (_from, _to))

        detailed_tree = DetailedEntries(tree=lexicon.tree)

        args = [lookup, pos]
        if _type:
            if _type.strip():
                args.append(_type)
                lookupfunc = detailed_tree.lookupLemmaPOSAndType
        else:
            lookupfunc = detailed_tree.lookupLemmaPOS

        return lookupfunc(*args)



    def lookup(self, _from, _to, lookup, lookup_type=False):
        _dict = self.language_pairs.get((_from, _to), False)

        if not _dict:
            return {'error': "Unknown language pair"}

        if lookup_type:
            if lookup_type == 'startswith':
                result = _dict.lookupLemmaStartsWith(lookup)
        else:
            result = _dict.lookupLemma(lookup)

        return {'lookups': result,
                'input': lookup,
                }

    # TODO: rename
    def lookups(self, _from, _to, lookups, lookup_type=False):
        from functools import partial

        _look = partial(self.lookup,
                        _from=_from,
                        _to=_to,
                        lookup_type=lookup_type)

        results = map(lambda x: _look(lookup=x), lookups)
        success = any([(not ('error' in r) and bool(r.get('lookups', False)))
                       for r in results])

        return results, success

    def frontPageLookup(self, _from, _to, lookup, lookup_type=False):
        lexicon = self.language_pairs.get((_from, _to), False)
        if not lexicon:
            raise Exception("Undefined language pair %s %s" % (_from, _to))

        frontpageformat = FrontPageFormat(tree=lexicon.tree)

        args = [lookup]
        if lookup_type:
            if lookup_type.strip():
                args.append(lookup_type)
                lookupfunc = frontpageformat.lookupLemma
        else:
            lookupfunc = frontpageformat.lookupLemma

        result = lookupfunc(*args)
        return { 'lookups': result
               , 'input': lookup
               }

    def frontPageLookups(self, _from, _to, lookups, lookup_type=False):
        from functools import partial

        _look = partial(self.frontPageLookup,
                        _from=_from,
                        _to=_to,
                        lookup_type=lookup_type)

        results = map(lambda x: _look(lookup=x), lookups)
        success = any([(not ('error' in r) and bool(r.get('lookups', False)))
                       for r in results])

        return results, success
