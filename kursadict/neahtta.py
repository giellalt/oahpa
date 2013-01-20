#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
A service that provides JSON and RESTful lookups to webdict xml trie files.

## Configuration

Configuration settings for paths to FSTs, utility programs and
dictionary files must be set in `app.config.yaml`. A sample file is
checked in as `app.config.yaml.in`, so copy this file, edit the settings
and then launch the service.

## Testing via cURL

### Submit post data with JSON

    curl -X POST -H "Content-type: application/json" \
         -d ' {"lookup": "fest" } ' \
         http://localhost:5000/lookup/nob/sme/

### Submit GET data with parameters, and JSON response

    curl -X GET -H "Content-type: application/json" \
           http://localhost:5000/detail/sme/nob/geađgi/

## Installing

See requirements.txt. Ideally, use virtualenv to create a new Python
virtual environment, and use requirements.txt to automatically install
all of the required packages.

You can test that it's worked by running this file with python-- if you
see no errors, and dictionaries are parsed, and autocomplete tries are
prepared, things are working. Finally, the app will state which host and
port it is running on. For developing locally, this is all you need.

### Production environments

There is a separate fcgi script (neahttadigisanit.fcgi) which is meant
to be used with nginx for production environments.

## Todos

TODO: autocomplete from all left language lemmas, build cache and save
      to pickle on each run, then use pickle

## Compiling XML

    java -Xmx2048m -Dfile.encoding=UTF8 net.sf.saxon.Transform \
        -it:main /path/to/gtsvn/words/scripts/collect-dict-parts.xsl \
        inDir=/path/to/gtsvn/words/dicts/smenob/src/ > OUTFILE.xml

    may need to also include -cp ~/lib/saxon9.jar

### Note about macs with saxon

Can be installed by brew

    brew install saxon

"""

import sys
import logging
import urllib
from   flask                          import ( Flask
                                             , request
                                             , json
                                             , render_template
                                             , Markup
                                             , Response
                                             , abort
                                             )

from   werkzeug.contrib.cache         import SimpleCache
from   config                         import *
from   utils                          import *
from   logging                        import getLogger

cache = SimpleCache()
app = Flask(__name__,
    static_url_path='/static',)


app.config = Config('.', defaults=app.config)
app.config.from_yamlfile('app.config.yaml')

# Configure user_log
user_log = getLogger("user_log")
useLogFile = logging.FileHandler('user_log.txt')
user_log.addHandler(useLogFile)
user_log.setLevel("INFO")



##
##  Endpoints
##
##


# language_pairs = app.config.lexicon.language_pairs
# autocomplete_tries = app.config.lexicon.autocomplete_tries

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# TODO: Keeping the old endpoints until all dependent apps are migrated
#       to the new ones.
@app.route('/autocomplete/<from_language>/<to_language>/',
           methods=['GET'], endpoint="autocomplete")
def autocomplete(from_language, to_language):

    autocomplete_tries = app.config.lexicon.autocomplete_tries
    # URL parameters
    lookup_key = user_input = request.args.get('lookup', False)
    lemmatize               = request.args.get('lemmatize', False)
    has_callback            = request.args.get('callback', False)

    autocompleter = autocomplete_tries.get((from_language, to_language), False)

    if not autocompleter:
        return fmtForCallback(
                json.dumps(" * No autocomplete for this language pair."),
                has_callback)

    autos = autocompleter.autocomplete(lookup_key)

    # Only lemmatize if nothing returned from autocompleter?

    return Response(response=fmtForCallback(json.dumps(autos), has_callback),
                    status=200,
                    mimetype="application/json")

# TODO: Keeping the old endpoints until all dependent apps are migrated
#       to the new ones.
@app.route('/lookup/<from_language>/<to_language>/',
           methods=['GET'], endpoint="lookup")
def lookupWord(from_language, to_language):
    """
    Returns a simplified set of JSON for dictionary, with 'success' to mark
    whether there were no errors. Additional URL parameters are available to
    control the lookup type or whether the lookup is lemmatized before being
    run through the lexicon.

    Path parameters:

        /lookup/<from_language>/<to_language>/

        Follow the ISO code.

        TODO: 404 error for missing languages

    URL parameters:

        lookup - the string to search for
        lemmatize - true/false
        type - none, or 'startswith'

    Output:

        {
            "result": [
                {
                    "input": "viidni",
                    "lookups": [
                        {
                            "right": [
                                "vin"
                            ],
                            "pos": "n",
                            "left": "viidni"
                        }
                    ]
                }
            ],
            "success": true
        }

    If there are multiple results from lemmatizing, they are included in the
    "results" list.

    """

    if (from_language, to_language) not in app.config.dictionaries:
        abort(404)

    success = False
    results = False

    # URL parameters
    lookup_key = user_input = request.args.get('lookup', False)
    lookup_type             = request.args.get('type', False)
    lemmatize               = request.args.get('lemmatize', False)
    has_callback            = request.args.get('callback', False)

    if lookup_key == False:
        return json.dumps(" * lookup undefined")

    # Is there a lemmatizer?
    lemm_ = app.config.morphologies.get(from_language, False)
    if lemm_:
        lemmatizer = lemm_.lemmatize

    if lemmatize and lemmatizer and not lookup_type:
        lookup_keys = lemmatizer(lookup_key, split_compounds=True)
    else:
        lookup_keys = [lookup_key]

    results, success = app.config.lexicon.lookups( from_language
                                                 , to_language
                                                 , lookup_keys
                                                 , lookup_type
                                                 )

    results = sorted( results
                    , key=lambda x: len(x['input'])
                    , reverse=True
                    )

    logSimpleLookups( user_input
                    , results
                    , from_language
                    , to_language
                    )

    data = json.dumps({ 'result': results
                      , 'success': success })

    if has_callback:
        data = '%s(%s)' % (has_callback, data)

    return Response( response=data
                   , status=200
                   , mimetype="application/json"
                   )


# TODO: Keeping the old endpoints until all dependent apps are migrated
#       to the new ones.
@app.route('/detail/<from_language>/<to_language>/<wordform>.<format>',
           methods=['GET'], endpoint="detail")
def wordDetail(from_language, to_language, wordform, format):
    """
    Returns a detailed set of information, in JSON or HTML, given a specific
    wordform.

    Path parameters:

        /detail/<from_language>/<to_language>/<wordform>.<format>
    
    TODO: See /languages for an overview of supported language pairs, and
    supply the ISO code for <from_language> and <to_language>. <wordform> may
    be any word form in the source language, as the form will be passed through
    a morphological analyzer.

    <format> must be either json, or html.
    
      Ex.) /detail/sme/nob/orrut.html
           /detail/sme/nob/orrut.json

    <wordform> is generally expected to be UTF-8, and most web browsers
    automatically encode unicode in URLs to UTF-8, however it may be that
    services using this endpoint will need to make sure to do the conversion.

    """
    import hashlib

    user_input = wordform
    if not format in ['json', 'html']:
        return "Invalid format. Only json and html allowed."

    wordform = wordform.encode('utf-8')

    # NOTE: these options are mostly for detail views that are linked to
    # from the initial page's search. Everything should work without
    # them, and with all or some of them.

    # Do we filter analyzed forms and lookups by pos? 
    pos_filter = request.args.get('pos_filter', False)
    # Do we want to analyze compounds?
    no_compounds = request.args.get('no_compounds', False)
    # Should we match the input lemma with the analyzed lemma?
    lemma_match = request.args.get('lemma_match', False)

    _pattern = u'/detail/%s/%s/%s.%s?pos_filter=%r&no_compounds=%r&lemma_match=%r'
    cache_key =  _pattern % \
                ( from_language
                , to_language
                , wordform.decode('utf-8')
                , format
                , pos_filter
                , no_compounds
                , lemma_match
                )

    if no_compounds or lemma_match:
        want_more_detail = True
    else:
        want_more_detail = False

    def unsupportedLang(more='.'):
        if format == 'json':
            _err = " * Detailed view not supported for this language pair" + more
            return json.dumps(_err)
        elif format == 'html':
            abort(404)

    if (from_language, to_language) in app.config.lexicon.reverse_language_pairs:
        return unsupportedLang()

    if app.caching_enabled:
        cached_result = cache.get(cache_key)
    else:
        cached_result = None

    if cached_result is None:

        lang_paradigms = app.config.paradigms.get(from_language)
        if not lang_paradigms:
            return unsupportedLang(', no paradigm defined.')
        lang_baseforms = app.config.baseforms.get(from_language)
        if not lang_baseforms:
            return unsupportedLang(', no baseforms defined.')
        # All lookups in XML must go through analyzer, because we need
        # POS info for a good lookup.
        morph = app.config.morphologies.get(from_language, False)
        if no_compounds:
            analyzed = morph.analyze(wordform)
        else:
            analyzed = morph.analyze(wordform, split_compounds=True)
        # NOTE: #formanalysis

        # Collect lemmas and tags
        _result_formOf = []
        if analyzed:
            for form, lemma, tag in sorted(analyzed, reverse=True):

                # TODO: try with OBT
                if lemma == '?' or tag == '?':
                    continue
                pos, _tag = tag[0], tag[1::]
                _ft = morph.tool.formatTag(tag)
                _result_formOf.append((lemma, pos, _ft))

        # Now collect XML lookups
        _result_lookups = []
        _lemma_pos_exists = []

        if lemma_match:
            _result_formOf = [ (lem, pos, tag)
                               for lem, pos, tag in _result_formOf
                               if lem == wordform.decode('utf-8') ]

        if pos_filter:
            _result_formOf = [ (lem, pos, tag)
                               for lem, pos, tag in _result_formOf
                               if pos.upper() == pos_filter.upper() ]


        for lemma, pos, tag in _result_formOf:

            # TODO: generalize for other languages, use tagsets
            _sp = morph.tool.splitAnalysis(tag)
            if len(_sp) >= 2:
                _type = _sp[1]
                if _type not in [u'NomAg', 'G3']:
                    _type = False
            else:
                _type = False

            if (lemma, pos) in _lemma_pos_exists:
                continue
            # Only look up word when there is a baseform
            paradigm = lang_paradigms.get(pos, False)
            baseforms = lang_baseforms.get(pos, False)
            if baseforms:
                xml_result = app.config.lexicon.detailedLookup( from_language
                                                              , to_language
                                                              , lemma
                                                              , pos
                                                              , _type=_type
                                                              )

                if xml_result:
                    res = {'lookups': xml_result}
                else:
                    res = False

                _result_lookups.append({
                    'entries': res,
                    'input': (lemma, pos, tag, _type)
                })
                _lemma_pos_exists.append((lemma, pos))
            else:
                continue

        detailed_result = {
            "analyses": _result_formOf,
            "lexicon": _result_lookups,
            "input": wordform.decode('utf-8'),
        }

        # TODO: ideally the things here need to be going to an external
        # socket server thing analogous to lookupserv for Oahpa/Sahka.
        # also, for ease of use it needs to be something that the
        # Morphology or XFST or OBT classes spawn and keeps track of
        # For now, just caching things on the hope that this begins to
        # save time.

        def cacheKey(lang, lemma, generation_tags):
            """ key is something like generation-LANG-LEMMA-TAG|TAG|TAG
            """
            _cache_tags = '|'.join(['+'.join(a) for a in generation_tags])

            _cache_key = hashlib.md5()
            _cache_key.update('generation-%s-' % from_language)
            _cache_key.update(lemma.encode('utf-8'))
            _cache_key.update(_cache_tags.encode('utf-8'))
            return _cache_key.hexdigest()


        # TODO: either clean this up or comment.
        for _r in _result_lookups:
            lemma, pos, tag, _type = _r.get('input')
            paradigm = lang_paradigms.get(pos)
            if tag in lang_baseforms.get(pos):
                if paradigm:
                    _pos_type = [pos]
                    if _type:
                        _pos_type.append(_type)
                    form_tags = [_pos_type + _t.split('+') for _t in paradigm]

                    morphology_cache_key = cacheKey(from_language,
                                                    lemma,
                                                    form_tags)

                    _is_cached = cache.get(morphology_cache_key)
                    if _is_cached:
                        _r['paradigms'] = _is_cached
                    else:
                        _generate = morph.generate(lemma, form_tags)
                        cache.set(morphology_cache_key, _generate)
                        _r['paradigms'] = _generate
                else:
                    _r['paradigms'] = False
            else:
                _r['paradigms'] = False

        cache.set(cache_key, detailed_result)
    else:
        detailed_result = cached_result

    _lookup = detailed_result.get('lexicon')

    if len(_lookup) > 0:
        success = True
        result_lemmas = list(set([
            entry['input'][0] for entry in detailed_result['lexicon']
        ]))
        _meanings = []
        for lexeme in detailed_result['lexicon']:
            if lexeme['entries']:
                for entry in lexeme['entries']['lookups']:
                    _entry_tx = []
                    for mg in entry['meaningGroups']:
                        _entry_tx.append(mg['translations'])
                    _meanings.append(list(sum(_entry_tx, [])))
        tx_set = '; '.join([', '.join(a) for a in _meanings])
    else:
        success = False
        result_lemmas = ['-']
        tx_set = '-'

    user_log.info('%s\t%s\t%s\t%s\t%s\t%s' % ( user_input
                                               , str(success)
                                               , ', '.join(result_lemmas)
                                               , tx_set
                                               , from_language
                                               , to_language)
                                               )

    if format == 'json':
        result = json.dumps({
            "success": True,
            "result": detailed_result
        })
        return result
    elif format == 'html':
        return render_template( 'word_detail.html'
                              , language_pairs=app.config.pair_definitions
                              , result=detailed_result
                              , user_input=user_input
                              , _from=from_language
                              , _to=to_language
                              , more_detail_link=want_more_detail
                              , zip=zipNoTruncate
                              )

# TODO: Keeping the old endpoints until all dependent apps are migrated
#       to the new ones.
@app.route('/notify/<from_language>/<to_language>/<wordform>.html',
           methods=['GET'], endpoint="notify")
def wordNotification(from_language, to_language, wordform):
    """
    Returns a simplified set of JSON for dictionary, with 'success' to mark
    whether there were no errors. Additional URL parameters are available to
    control the lookup type or whether the lookup is lemmatized before being
    run through the lexicon.

    Path parameters:

        /lookup/<from_language>/<to_language>/

        Follow the ISO code.

        TODO: 404 error for missing languages

    URL parameters:

        lookup - the string to search for
        lemmatize - true/false
        type - none, or 'startswith'

    Output:

        {
            "result": [
                {
                    "input": "viidni",
                    "lookups": [
                        {
                            "right": [
                                "vin"
                            ],
                            "pos": "n",
                            "left": "viidni"
                        }
                    ]
                }
            ],
            "success": true
        }

    If there are multiple results from lemmatizing, they are included in the
    "results" list.

    """

    success = False
    results = False

    # URL parameters
    lookup_key = user_input = wordform
    lookup_type = False
    lemmatize = True

    if (from_language, to_language) not in app.config.dictionaries:
        abort(404)

    if lemmatize and not lookup_type:
        lemm_ = app.config.morphologies.get(from_language, False)
        if lemm_:
            lemmatizer = lemm_.lemmatize
        lemmatized_lookup_key = lemmatizer(lookup_key)
    else:
        lemmatized_lookup_key = False

    if lemmatized_lookup_key:
        if not isinstance(lemmatized_lookup_key, list):
            lemmatized_lookup_key = [lemmatized_lookup_key]

        results = []
        for _key in lemmatized_lookup_key:
            result = lookupXML(from_language, to_language,
                               _key, lookup_type)
            result['input'] = _key
            if len(result['lookups']) == 0:
                result['lookups'] = False
            results.append(result)

        results = sorted(results, key=lambda x: len(x['input']), reverse=True)

        if 'error' in result:
            success = False
        else:
            success = True

        if 'lookups' in result:
            if not result['lookups']:
                success = False
    else:

        result = lookupXML(from_language, to_language,
                           lookup_key, lookup_type)
        result['input'] = lookup_key
        if len(result['lookups']) == 0:
            result['lookups'] = False
        results = [result]

        results = sorted(results, key=lambda x: len(x['input']), reverse=True)

        if 'error' in result:
            success = False
        else:
            success = True

        if 'lookups' in result:
            if not result['lookups']:
                success = False

    result_lemmas = set()
    tx_set = set()
    if success:
        for result in results:
            result_lookups = result.get('lookups')
            if result_lookups:
                for lookup in result_lookups:
                    l_left = lookup.get('left')
                    l_right = ', '.join(lookup.get('right'))
                    tx_set.add(l_right)
                    # Reversed lookups return list
                    if isinstance(l_left, list):
                        for _l in l_left:
                            result_lemmas.add(_l)
                    else:
                        result_lemmas.add(lookup.get('left'))

    result_lemmas = ', '.join(list(result_lemmas))
    meanings = '; '.join(list(tx_set))

    user_log.info('%s\t%s\t%s\t%s\t%s\t%s' % ( user_input
                                               , str(success)
                                               , result_lemmas
                                               , meanings
                                               , from_language
                                               , to_language
                                               ,
                                               ))

    return render_template( 'word_notify.html'
                          , result=results
                          , success=success
                          , input=user_input
                          )

proxy_shim = """
<script
    src="//ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js">
</script>

<link
    href="http://%(host)s/static/css/jquery.neahttadigisanit.css"
    rel="stylesheet">
</link>

<script
    type="text/javascript"
    src="http://%(host)s/static/js/jquery.neahttadigisanit.min.js">
</script>

<script type='text/javascript'>
    $(document).ready(function (){
        $(document).selectToLookup({
            tooltip: true,
            displayOptions: true,
            spinnerImg: 'http://%(host)s/static/img/spinner.gif'
        });
    });
</script>""" % { 'host': 'localhost:5000' # TODO: live host
               }

# TODO:
# TODO: minify and url-encode javascript:blah
# TODO: http://jsbeautifier.org/
bookmarklet = """
(function () {
    var script  = document.createElement('script');
    script.type = 'text/javascript';
    script.src  = 'https://secure.branch.com/assets/bookmarklet/bookmarklet.m.js';
    document.body.appendChild(script);
})();

"""


@app.route('/read/', methods=['GET', 'POST'])
def embed():
    from lxml            import sax
    from flask           import render_template_string
    from xml.dom.minidom import parse

    # Allow submission via bookmarklet, e.g., "Read this page!"
    target = request.form.get('target_url', False)
    # TODO: validate url

    if request.method == 'GET':
        return render_template('proxy_reader.html')

    def proxy_error(msg):
        return render_template('proxy_error.html', error=msg)
    
    # TODO: store client IPs in cache, if number of requests exceeds a given
    # limit within a certain time frame, prevent the user from performing
    # additional requests, inform them.
    # proxy_error(msg="Disallowed content type <%s>" % content_type)
    # rate_limited = """ You have performed too many requests in a short
    # time. If you believe you have received this message in error, please
    # contact us. Or consider installing the bookmarklet.
    # """

    def tmpFileName(url, session_id):
        """ key is something like reader-url-session-date
        """
        from datetime import datetime
        _now = datetime.now().strftime('%Y-%m-%d-%H-%M')
        _cache_key = hashlib.md5()
        _cache_key.update('reader-%s-' % url)
        _cache_key.update(session_id)
        _cache_key.update(datetime)
        return _cache_key.hexdigest()
    
    client_ip = request.remote_addr
    temp_filename = tmpFileName(target, client_ip)


    # Supply some custom headers
    headers = {
        # Since we function as a proxy service, we want to tell the client we 
        # connect to who is requesting the information. In the event that someone
        # discovers our service and begins abusing it, we want to be able to help
        # investigate.
        'X-Forwarded-For': "%s, %s" % (client_ip, host),
        # Who we are
        'User-Agent': 'Neahttadigisánit (Linux x86_64; Python Requests; giellatekno.uit.no)',
    }

    # Check that header is actually a page, not something sketchy.
    h = requests.head(target, headers=headers)
    content_type = h.headers.get('content-type', '')
    if not content_type.find('text/html') > -1:
        proxy_error(msg="Disallowed content type <%s>" % content_type)

    # Do the actual request
    r = requests.get(target, headers=headers)
    if r == 200:
        text = r.text
        head, split, rest = text.partition('</head>')
        script = proxy_shim
        combined = head + script + split + rest

        # TODO: delete periodically
        cache_path = 'prox/' + temp_filename
        with open('static/' + cache_path, 'w') as X:
            X.write(combined)

    # TODO: what options need to be outside of the iframe?
    return render_template('proxy_iframe.html',
                           iframe_path=cache_path,)

##
## Public Docs
##

# TODO: Keeping the old endpoints until all dependent apps are migrated
#       to the new ones.
@app.route('/lookup/', methods=['GET'], endpoint="lookup-doc")
def wordLookupDocs():
    from cgi import escape
    _lookup_doc = escape(lookupWord.__doc__)
    return '<html><body><pre>%s</pre></body></html>' % _lookup_doc

# TODO: Keeping the old endpoints until all dependent apps are migrated
#       to the new ones.
# @app.route('/detail/', methods=['GET'], endpoint="detail-doc")
# def wordDetailDocs():
#     from cgi import escape
#     _lookup_doc = escape(wordDetail.__doc__)
#     return '<html><body><pre>%s</pre></body></html>' % _lookup_doc

##
## Public pages
##

# For direct links, form submission.
@app.route('/<_from>/<_to>/', methods=['GET', 'POST'])
def indexWithLangs(_from, _to):
    user_input = lookup_val = request.form.get('lookup', False)

    if (_from, _to) not in app.config.dictionaries:
        abort(404)

    errors = []
    if request.method == 'POST' and lookup_val:
        morph = app.config.morphologies.get(_from, False)

        if morph:
            # lookup_keys = lemmatizer(lookup_val, split_compounds=True)
            analyzed = morph.analyze(lookup_val, split_compounds=True)
            # Collect lemmas and tags
            _result_formOf = []
            lookup_keys = [lemma for f, lemma, tag in analyzed
                           if lemma != '?' or tag != '?']
            if lookup_keys:
                lookup_keys.append(lookup_val)
            else:
                lookup_keys = [lookup_val]
        else:
            lookup_keys = [lookup_val]
            analyzed = False

        _lookups = list(set(lookup_keys))
        results, success = app.config.lexicon.lookups(_from, _to, _lookups)

        # TODO: ukjent ord `gollet` -> gollehit, gollet, gollat
        # sort so that recognized word is at top, rest are shown as a
        # possible form of _
        # Maybe this logic should be done in template instead, 
        # print results
        def hasLookups(l):
            if l.get('lookups', False) == False:
                return False
            return True


        logSimpleLookups(user_input, results, _from, _to)

        results = sorted(filter(hasLookups, results),
                         key=lambda x: len(x['input']),
                         reverse=True)

        if not results:
            results = False
            analyzed = False

        show_info = False
    else:
        results = False
        user_input = ''
        show_info = True
        analyzed = False

    if len(errors) == 0:
        errors = False

    # TODO: include form analysis of user input #formanalysis
    return render_template( 'index.html'
                          , language_pairs=app.config.pair_definitions
                          , _from=_from
                          , _to=_to
                          , user_input=lookup_val
                          , word_searches=results
                          , analyses=analyzed
                          , errors=errors
                          , show_info=show_info
                          , zip=zipNoTruncate
                          )

@app.route('/about/', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/plugins/', methods=['GET'])
def plugins():
    return render_template('plugins.html')

@app.route('/', methods=['GET'], endpoint="canonical-root")
def index():
    return render_template( 'index.html'
                          , language_pairs=app.config.pair_definitions
                          , _from='sme'
                          , _to='nob'
                          , show_info=True
                          )


##
## Template filters
##

@app.template_filter('tagfilter')
def urlencode_filter(s, lang_iso):
    filters = app.config.tag_filters.get(lang_iso, False)
    if filters:
        filtered = []
        for part in s.split(' '):
            filtered.append(filters.get(part, part))
        return ' '.join(filtered)
    else:
        return s

@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)

if __name__ == "__main__":
    app.caching_enabled = True
    app.run(debug=True, use_reloader=False)

# vim: set ts=4 sw=4 tw=72 syntax=python expandtab :

