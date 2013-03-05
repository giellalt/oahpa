###
A jQuery plugin for enabling the Kursadict functionality


## TODOs / Bugs

TODO: prevent window url from updating with form submit params

###

# Wrap jQuery and add plugin functionality
jQuery(document).ready ($) ->

  fakeGetText = (string) ->
    ### Want to mark strings as requiring gettext somehow, so that
        a babel or other extractor can find them.
    ###
    return string

  _ = fakeGetText

  # API_HOST = "http://sanit.oahpa.no/"
  API_HOST = "http://localhost:5000/"

  Templates =
    OptionsMenu: (opts) ->
      # TODO: navmenu fixed at bottom containing language option, and 
      #       lookup button
      return "omg"
    
    OptionsTab: (opts) ->
      makeLanguageOption = (options) ->
        options_block = []
        for data, i in options
          if i+1 == 1
            checked = "checked"
          else
            checked = ""

          options_block.push """
            <option value="#{data.from.iso}-#{data.to.iso}">
            #{data.from.name} → #{data.to.name}
            </option>
          """
        return options_block.join('\n')
    
      el = $("""
      <div id="webdict_options">
        <div class="well">
        <a class="close" href="#" style="display: none;">&times;</a>
        <div class="trigger">
          <h1><a href="#" class="open">#{_("Á")}</a></h1>
        </div>

        <div class="option_panel" style="display: none;">
          <ul class="nav nav-pills">
            <li class="active">
              <a href="#" data-target="#options">#{ _("Options") }</a>
            </li>
            <li><a href="#" data-target="#about">#{ _("About") }</a></li>
          </ul>
          <div id="options" class="minipanel">
            <form class="">
              <label class="control-label" for="inputEmail">#{ _("Dictionary") }</label>
              <select type="radio" 
                     name="language_pair">
              #{makeLanguageOption(opts.dictionaries)}
              </select>
              <br />
              <button type="submit" class="btn" id="save">#{_('Save')}</button>
            </form>
          </div>
          <div id="about" style="display: none;" class="minipanel">
          <p>#{ _("In order to look up a word, hold down the <em>Alt</em> or <em>Option</em> (⌥) key, and doubleclick on a word. The service will contact the dictionary, and return a word after a short pause.") }</p>
          <p> </p>
          <p>#{ _('If you find a bug, or if the bookmark does not work on a specific page <a href="mailto:giellatekno@hum.uit.no">please contact us</a>. Tell us what page didn\'t work, or what you did when you discovered the problem.') }
          </p>
          </div>
        </div>
      </div>
      """)

      el.find('ul.nav-pills a').click (evt) ->
        target_element = $(evt.target).attr('data-target')
        el.find('ul.nav-pills a').parent('li').removeClass('active')
        $(evt.target).parent('li').addClass('active')
        el.find('div.minipanel').hide()
        el.find(target_element).show()
        return false

      el.find('.trigger').click () ->
        optsp = el.find('div.option_panel')
        optsp.toggle()
        el.find('a.close').toggle()
        return false

      el.find('a.close').click () ->
        optsp = el.find('div.option_panel')
        optsp.toggle()
        el.find('a.close').toggle()
        return false

      el.find('select[name="language_pair"]').change (e) ->
        store_val = $(e.target).val()
        DSt.set('digisanit-select-langpair', store_val)
        return true

      el.find('form').submit () ->
        optsp = el.find('div.option_panel')
        optsp.toggle()
        el.find('a.close').toggle()
        return false
      
      return el

    ErrorBar: (args) ->
      host = args.host
      el = $("""
       <div id="nds_errors" class="errornav navbar-inverse navbar-fixed-bottom">
         <div class="navbar-inner">
           <div class="container">
             <p><strong>#{_("Error!")}</strong> #{_("Could not connect to dictionary server")} (host: #{host}).
                <a href="#" class="dismiss">#{_("Close")}</a>.</p>
           </div>
         </div>
       </div>
       """)
      el.find('a.dismiss').click () ->
        $('body .errornav').remove()
        return false
      return el

  initSpinner = (imgPath) ->
    ###
        spinner popup in right corner; `spinner = initSpinner()` to
        create or find, then usual `spinner.show()` or `.hide()` as
        needed.
    ###
    spinnerExists = $(document).find('.spinner')
    if spinnerExists.length == 0
      spinner = $("""<img src="#{imgPath}" class="spinner" />""")
      $(document).find('body').append(spinner)
      return spinner
    return spinnerExists


  ## Some global ajax stuff
  ##
  ## 

  $.ajaxSetup
    type: "GET"
    timeout: 10 * 1000
    beforeSend: (args) ->
      spinner = initSpinner()
      spinner.show()
    complete: (args) ->
      spinner = initSpinner()
      spinner.hide()
    dataType: "json"
    cache: true
    error: () =>
      $(document).find('body').find('.errornav').remove()
      $(document).find('body').append Templates.ErrorBar {
        host: window.NDS_API_HOST || API_HOST
      }

  ##
  ## Some rangy helper functions 
  ## 

  getFirstRange = ->
    sel = rangy.getSelection()
    (if sel.rangeCount then sel.getRangeAt(0) else null)
  
  cloneContents = (range) ->
    range.cloneContents().textContent
  
  surroundRange = (range, surrounder) ->
    if range
      if not range.canSurroundContents()
        # TODO: should be possible to recover from this sometimes, as
        # non-FF browsers do not have this issue
        return false
      try
        range.surroundContents surrounder
      catch ex
        if (ex instanceof rangy.RangeException \
            or Object::toString.call(ex) is "[object RangeException]") \
            and ex.code is 1
          alert """Unable to surround range because range partially selects a
                   non-text node. See DOM Level 2 Range spec for more
                   information.\n\n""" + ex
        else
          alert "Unexpected errror: " + ex

   
  cleanTooltipResponse = (selection, response, opts) ->
    ###
        Clean response from tooltip $.getJSON query, and display results
    ###

    string   = selection.string
    element  = selection.element
    range    = selection.range

    if opts.tooltip
      _wrapElement = $("""
      <a style="font-style: italic; border: 1px solid #CEE; padding: 0 2px" 
         class="tooltip_target">#{string}</a>
      """)[0]
      surroundRange(range, _wrapElement)

    # Compile result strings
    result_strings = []
    for result in response.result
      for lookup in result.lookups
        if lookup.right.length > 1
          clean_right = []
          for r, i in lookup.right
            clean_right.push "#{i+1}. #{r}"
          right = clean_right.join(', ')
        else
          right = lookup.right[0]

        result_string = "<em>#{lookup.left}</em> (#{lookup.pos}) &mdash; #{right}"
        result_strings.push(result_string)

    
    langpair = DSt.get('digisanit-select-langpair')
    [_f_from, _t_to] = langpair.split('-')
    current_pair = $.fn.selectToLookup.options.dictionaries.filter (e) =>
      if e.from.iso == _f_from and e.to.iso == _t_to
        return true
      else
        return false
    if current_pair.length > 0
      _cp = current_pair[0]
      current_pair_names = "#{_cp.from.name} → #{_cp.to.name}"
    else
      current_pair_names = ""

    if result_strings.length == 0 or response.success == false
      if opts.tooltip
        _tooltipTitle = _('Ukjent ord')
        result_strings.push("<span class='tags'><em>#{_('You are using')} #{current_pair_names}</em></span>")
        if response.tags.length > 0
          _tooltipTitle = _('Betydning ikke funnet')
        ##  tags = ("<li><em>#{t[1]}</em></li>" for t in response.tags).join(', ')
        ##  result_strings.push("<span class='tags'><ul>#{tags}</ul></span>")

    if opts.tooltip
      if !_tooltipTitle
        _tooltipTitle = string
      
      _tooltipTarget = $(element).find('a.tooltip_target')

      _tooltipTarget.popover
        title: _tooltipTitle
        content: $("<p />").html(result_strings.join('<br />')).html()
        html: true
        placement: () =>
          if _tooltipTarget[0].offsetLeft < 125
            'right'
          else
            'bottom'
        trigger: 'hover'
      
      # Remove selection
      if window.getSelection
        # Chrome
        if window.getSelection().empty
          window.getSelection().empty()
        # Firefox
        else if window.getSelection().removeAllRanges
          window.getSelection().removeAllRanges()
      # IE
      else if document.selection
        document.selection.empty()
      # Done
      _tooltipTarget.popover('show')

  
  lookupSelectEvent = (evt, string, element, range, opts) ->
    result_elem = $(document).find(opts.formResults)

    # Remove punctuation, some browsers select it by default with double
    # click
    string = $.trim(string).replace(/\b[-.,()&$#!\[\]{}"]+\B|\B[-.,()&$#!\[\]{}"]+\b/g, "")

    if (string.length > 60) or (string.search(' ') > -1)
      return false

    langpair = $(opts.langPairSelect).val()
    # "aaabbb"
    [source_lang, target_lang] = langpair.split('-')
    lookup_string = string

    post_data =
      lookup: lookup_string
      lemmatize: true

    url = "#{opts.api_host}/lookup/#{source_lang}/#{target_lang}/"
    $.getJSON(
      url + '?callback=?'
      post_data
      (response) =>
        selection = {
          string: string
          element: element
          range: range
        }
        cleanTooltipResponse(selection, response, opts)
    )
    return false

  ##
   # $(document).selectToLookup();
   #
   #
   ## 

  $.fn.selectToLookup = (opts) ->
    opts = $.extend {}, $.fn.selectToLookup.options, opts
    spinner = initSpinner(opts.spinnerImg)

    # TODO: find a way to mark strings as gettextable, maybe use cake
    #       build process to extract them to something simple.

    # TODO: check localstorage, fetch language JSON from /read/config/
    #       extend options
    #       also check browser language and make sure this is included
    #       in request somehow.
    
    # TODO: device / OptionsMenu
    if opts.displayOptions
      $(document).find('body').append Templates.OptionsTab(opts)
      window.optTab = $(document).find('#webdict_options')
      ### Over 9000?!! ###
      window.optTab.css('z-index', 9000)

    # Recall stored language pair from session
    previous_langpair = DSt.get('digisanit-select-langpair')
    if previous_langpair
      _select = "select[name='language_pair']"
      _opt = window.optTab.find(_select).val(previous_langpair)
    else
      _select = "select[name='language_pair']"
      _opt = window.optTab.find(_select).val()
      previous_langpair = DSt.set('digisanit-select-langpair', _opt)
    
    holdingOption = (evt) =>
      clean(evt)

      if evt.altKey
        element = evt.target
        range = getFirstRange()
        string = cloneContents(range)
        if range and string
          lookupSelectEvent(evt, string, element, range, opts)
        return false
      return false

      # TODO: one idea for how to handle lookups wtihout alt/option key
      #
      # else
      #   if string != ''
      #     window.optTab.find('.well').addClass('highlight')
      #     window.optTab.find('.well a.open').click (o) =>
      #       lookupSelectEvent(evt, string, element, index, opts)
      #       return false
      #   else
      #     window.optTab.find('.well').removeClass('highlight')
    
    clean = (event) ->
      parents = []
      $(document).find('a.tooltip_target').each () ->
        parents.push $(this).parent()
        $(this).popover('destroy')
        $(this).replaceWith(this.childNodes)

      $(document).find('a.tooltip_target').contents().unwrap()

    window.cleanTooltips = clean
    $(document).bind('click', holdingOption)
   
  $.fn.selectToLookup.options =
    api_host: API_HOST
    formResults: "#results"
    spinnerImg: "dev/img/spinner.gif"
    sourceLanguage: "sme"
    langPairSelect: "#webdict_options *[name='language_pair']"
    tooltip: true
    displayOptions: true
    dictionaries: [
      {
        from:
          iso: 'sme'
          name: 'nordsamisk'
        to:
          iso: 'nob'
          name: 'norsk'
      }
    ]


  ##
   # $('#divname').digisanit();
   #
   #
   ## 
    
  $.fn.digiSanit = (opts) ->
    opts = $.extend {}, $.fn.digiSanit.options, opts

    this.each ->
      
      elem = $(this)
      result_elem = $(this).find('#results')

      # set up dropdown events for selecting language pair
      # Also store the default value in localStorage using DSt.js
      #
      # $(this).find('#langpairs li a').click (obj) =>
      #   new_val = $(obj.target).attr('data-value')
      #   elem.find('button span.val_name').html(
      #     "#{new_val.slice(0,3)}->#{new_val.slice(3,6)}"
      #   )
      #   elem.find('select[name="target_lang"]').val new_val
      #   DSt.set('digisanit-form-langpair', new_val)
      
      # Recall previous value if stored in session.
      # previous_setting = DSt.get('digisanit-form-langpair')
      # if previous_setting
      #   elem.find('select[name="target_lang"]').val previous_setting

      elem.find('input[name="lookup"]').keydown (event) ->
        if event.keyCode == 13
          elem.submit()
          return false
        return true

      elem.submit () =>
        lookup_value = elem.find('input[name="lookup"]').val()

        lang_pair = $(this).find('input[name="target_lang"]').val()
        source_lang = lang_pair.slice(0,3)
        target_lang = lang_pair.slice(3,6)

        post_data =
          lookup: lookup_value

        if lookup_value.slice(-1) == '*'
          post_data.type = 'startswith'
          post_data.lookup = post_data.lookup.replace('*', '')

        unknownWord = (response) ->
          $(result_elem).append $("""
            <p xml:lang="no" class="alert">Ukjent ord.</p>
          """)
          return false

        cleanResponse = (response) =>
          $(result_elem).html ""

          if (response.success == false)
            unknownWord()
          else if (response.result.length == 1) and not response.result[0].lookups
            unknownWord()

          for result in response.result
            for lookup in result.lookups
              result_list = lookup.right.join(', ')
              
              $(result_elem).append $("""
                <p>#{lookup.left} (#{lookup.pos}) &mdash; #{result_list}</p>
              """)
        
        url = "#{opts.api_host}/lookup/#{source_lang}/#{target_lang}/"
        $.getJSON(
          url + '?callback=?'
          post_data
          cleanResponse
        )

        return false

  $.fn.digiSanit.options =
    api_host: API_HOST
    formIDName: "#digisanit"
    formResults: "#results"

  $.fn.digiSanitTest = (opts) ->
    opts = $.extend {}, $.fn.digiSanit.options, opts
    cleanResp = (response) ->
      console.log "Can connect."
      console.log response
    data = {
      lookup: "mannat"
    }
    $.getJSON(
      "#{opts.api_host}/lookup/sme/nob/?callback=?",
      data,
      cleanResp
    )

  $.fn.digiSanitTest.options =
    api_host: API_HOST
    formIDName: "#digisanit"
    formResults: "#results"

# End jQuery wrap
