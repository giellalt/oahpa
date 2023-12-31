﻿# Current development:

Moving stuff to trello

# Added installation notes:

    Context processors:
        "sme_oahpa.courses.context_processors.courses_user",
        "django.core.context_processors.csrf",

    Middleware:
        'django.middleware.csrf.CsrfViewMiddleware',
        'courses.middleware.GradingMiddleware',

    installed apps:
        'django.contrib.staticfiles',

        'sme_oahpa.courses',
        'rest_framework',
        # ... 
        'notifications',
        'django_messages',
        'django_forms_bootstrap',

    TEMPLATE_LOADERS:
        'django.template.loaders.app_directories.Loader',

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    COOKIE_NAME_STARTSWITH = 'wordpress_logged_in_'

## New packages in use

- django-notifications-hq: https://github.com/brantyoung/django-notifications
- django-messages: https://github.com/arneb/django-messages

# Oppsummering fra prosjektbeskrivelsen:

## Status quo:

* Innloggingssystem basert på Open-ID: brukar får ein konto i kursa, og
  cookie frå kursa/kuvsje gjeld alle subdomainar i `*.oahpa.no`. Oahpa
  ser på cookie:n, og loggar brukaren inn, og registrerar ein ny konto
  viss det trengst.

* Bruk av ulike modular i Oahpa vert logga, og brukaren får oversikt
  over aktivitet, med nokre korte / enkle statistikk

* Admin brukarar for logga inn på ein administrative grensesnitt for å
  leggja til nye lærarar i systemet

* Admin brukarar kan setja brukarar som ansvarleg som lærar i fleire kurs.

* Lærararfår oversikt over elevane deira: kan sjå på datoen av siste
  innlogging, statistikk, osv. Dette er generert av Django sitt
  admingrensesnittrammeverk.

### Neste stigar

Nye innloggings-/registrasjons- eigenskapar:

 * Studentar får registrera seg i kurs dei fylgjar, og vert knytta opp
   mot ein lærar.

 * Lærar får rettleda studentar om oppgåvor dei bur gjera på ulike trinn
   i kurset.

 * Lærar får oversikt på progresjon i læringsmåla til kvar student,
   resymé

Nye moglegheitar for tilbakemelding til studentar om statistikk / progresjon:

 * Oahpa og View vert logga.

 * Studentane får tilbakemelding på typar grammatiske feil dei gjer

 * Studentar får fylgja med på progresjon i forhold til læringsmål frå
   kurs dei er registrert i:

   - studenten får fargekode for nivå dei hev nådd i forhold til
     læringsmål

   - studenten får ogso prosent av arbeidsbyrden som er definert

Nye moglegheitar for inndeling av oppgåvor:

 * Kurs-spesifiske læringsmål for grammatikk og ordforråd

Nye moglegheitar for grammatiske feedback:

* I forhold til studentane sine nivåklassifisering, får student ulike
  form for tilbakemelding: meir eller mindre faglig grammatisk
  terminologi

* Unngå lange forklaringar: sporing av feedback studentar hev sedd på

# Programmering

## Nye models

 * event / notification
   - student adds to course, need way of tracking new events to show to
     instructor when they log in
   - django rest framework for events shown to instructor, so they can
     dismiss easily each notification

 * Goal
   - related course
   - goal name
   - expected accuracy rate / condition for success
   - goal definitions:
     - exercise module (MORFA S, MORFA C, LEKSA, NUMRA)
     - exercise settings:
        - semantic sets, or case and number, and so forth
     - correct on first try vs. correct eventually
   - goal deep-links

## Endringar på eksisterande model

 * User profile model needs changes for level/statistics
   - related course
   - goals completed
   - grammatical feedback type

 * User log - UI events ulik frå correct/incorrect svar: brukar klikkar
   på feedback, opnar grammatikken, osv.

    - `process_template_response` middleware?

    - maybe this should be a different model: user feedback events

    - this also needs to reference user objects if they're avialable,
      instead of username. could be an irritating process to upgrade.
        - can also use signals to generate different types of log
          events: user enters answers partially vs. user enters all
          things

    - alternate option: store logs in courses module only for when a
      student is working toward a goal. 

 * Morphological feedback models:
   - will need a means for specifying the "level" of the feedback.

### Moglege endringar

 * User log - course goal vs. general activity - viss studenten vel å
 trena på eit kursmål, vis i loggen

## Nye frontend endringar

 * Systemet må lagra ei loggmelding når studentar klikkar på morfologisk
   feedback, dvs.: JSON API for logg-eventar

     - systemet kan då velja kva slags feedback det burde visa neste
       gongen, når alt vert logga

     - django rest framework and angular.js for these things:
       http://www.django-rest-framework.org/

 * Når studenten trenar på ulike oppgåvor som dei hev vald sjølv (f.eks., dei
   berre går gjennom Morfa-S), det kan henda dei vil framleis sjå ei
   lista over ting dei kan gjera i forhold til eit kurs:

     - ? spursmål: burde alle aktivitet i ei oppgåva gå til kursmål, eller
         berre når folk vel å trena på målet? f.eks., eksame-basert
         læring, eller statistikk/progresjon basert?

## Source data updates

 * Feedback xml files (`feedback_nouns.xml`, `messages.lang.xml`) need
   attributes for specifying message level. We can assume that there may
   be however many levels as the instructor is willing to define, but,
   message id needs to continue to be unique. Following is a maybe
   unrealistic example, but should illustrate the point:

   This should be an optional update, which doesn't cause problems if
   not present.

e.g.:

    <l stem="2syll">
      <msg>bisyllabic_stem</msg>
    </l>

    -->

    <l stem="2syll">
      <msg user_level="1">bisyllabic_stem_I</msg>
      <msg user_level="2">bisyllabic_stem_II</msg>
      <msg user_level="3">bisyllabic_stem_III</msg>
    </l>

    <messages xml:lang="sme">
        <message order="A" id="Bis_NomPl" user_level="1">
            WORDFORM gets -t plural, and has two syllables.
        </message>
        <message order="A" id="Bis_NomPl" user_level="2">
            WORDFORM inflects as a bisyllabic noun in the nominative plural.
        </message>
    </messages>

 * Need to determine what the behavior will be if there is not a message
   defined for the particular level, probably just take the highest
   level available?

## User flows

Student sjølvregistrasjon:

 1.) studenten vel eit kurs

 2.) får tilgang til alle ulike måla på kurset

 3.) burde lærar godkjenna, eller får studenten plutseleg tilgang til alle
     resurss?

Mål-basert oppgåvor:

 1.) studenten vel eit mål frå lista si

 2.) når dei arbeider, alt arbeid går i måla

   - må ha ein måte at dei kan slå det av. Kanskje berre når dei
     navigerar bort frå sida, eller kvar spursmål-svar sett send ein
     variabel med kvar form submit

## New views

 * Student's courses
 * Student assignment/goals list
 * Instructor feedback

# Questions

## Course goals:

What sort of criteria do we expect the instructors to specify? I have a
few ideas (i.e., 80% accuracy on Illative Pl), but also:

A student needs to select that they will work on this goal, or can any
work be counted? Must students choose to "test" themselves when they are
ready?

## Course registration

Students can register, maybe just by typing in a course name or
following a link, instructors can always remove them.

