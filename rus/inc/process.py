#!/usr/bin/python3
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, codecs, copy;

conversion_table = {
	'Прилагательное, тип склонения по классификации А. Зализняка — 1*a.':'1*a',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 1a.':'1a',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 5*b по классификации А. Зализняка); при склонении в основе происходит чередование гласной е с «нулём».':'5*b',
	'Прилагательное, тип склонения по классификации А. Зализняка — 3aX~.':'3aX~',
	'Прилагательное, относительное, тип склонения по классификации А. Зализняка — 3aX~.':'3aX~',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 2*a-. Краткая форма муж. р. предположительна.':'2*a-',
	'Местоимение (притяжательное), тип склонения по классификации А. Зализняка — 6b.':'6b',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 2a.':'2a',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 5b.':'5b',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 1a.':'1a',
	'Числительное (порядковое прилагательное),  тип склонения по классификации А. Зализняка — 1b.':'1b',
	'Числительное, порядковое, адъективное склонение; тип склонения по классификации А. Зализняка — 1b':'1b',
	'Числительное, порядковое, адъективное склонение; тип склонения по классификации А. Зализняка — 1a':'1a',
	'Числительное (местоименное прилагательное, местоимение), тип склонения 1*b по классификации А. Зализняка.':'1*b',
	'Указательное местоимение, тип склонения по классификации А. Зализняка — 3b. Корень: -так-; окончание: -ой.':'3b',
	'Указательное местоимение, тип склонения по классификации А. Зализняка — <1a>.':'1a',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения индивидуальное по классификации А. Зализняка); единственное число относится к типу склонения 3a по классификации А. Зализняка (2-ое склонение). Множественное, люди, образуется супплетивно, но после количественных числительных в ряде падежей используются формы слова человек.':'3a',
	'Существительное, одушевлённое, женский род, 3-е склонение (тип склонения 8e^)Возможно использование,как обращениие':'8e^',
	'Существительное, одушевлённое, женский род, 1-е склонение (тип склонения 1*d^) Во фразеологизме всем сестра́м по серьга́м используется вариант ударения по типу 1*f.':'1*d^',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 6*a- по классификации А. Зализняка); формы мн. ч. предположительны.':'6*a-',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 1c- по классификации А. Зализняка); формы мн. ч. предположительны.':'1c-',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 1*c^) Исчислимое и неисчислимое.':'1*c^',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 1b- по классификации А. Зализняка); множественное число предположительно или неупотребимо.':'1b-',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 5*b по классификации А. Зализняка); при склонении в основе происходит чередование гласной «е» с «нулём».':'5*b',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 2a)Контроль чего-то/кого-то, за кем-то/чем-то, над кем-то/чем-то.':'2a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1e)':'1e',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1c(1)) В словаре А. Зализняка слово отнесено к категории 1a — мн. ч.: се́веры, се́веров, се́верам и т. п., — но в современном употреблении ударение в этих формах ставится на окончание. Множественное число употребляется в основном в значении северные области.':'1c(1)',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1a- по классификации А. Зализняка); множественное число предположительно или неупотребимо.':'1a-',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1a по классификации А. Зализняка); множественное число морфологически возможно, но на практике неупотребимо или предположительно.':'1a',
	'Существительное, неодушевлённое, женский род, 3-е склонение (тип склонения 8e^)':'8e^',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 4d\')':'4d\'',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 3f\')':'4f\'',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 3*e по классификации А. Зализняка); формы ед. ч. не используются.':'3*e',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 3d\')':'3d\'',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 3a по классификации А. Зализняка); формы ед. ч. не используются.':'3a',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 1d- по классификации А. Зализняка); формы мн. ч. предположительны или неупотребимы.':'1d-',
	'Притяжательное местоимение, тип склонения по классификации А. Зализняка — 6b.':'6b',
	'Прилагательное, тип склонения по классификации А. Зализняка — 3b/c~.':'3b/c~',
	'Прилагательное, тип склонения по классификации А. Зализняка — 1*b~. Полной формы нет.':'1*b~',
	'Прилагательное, тип склонения по классификации А. Зализняка — 1a.':'1a',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 4a.':'4a',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 3bX~.':'3bX~',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 1*a.':'1*a',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 3a^.':'3a^',
	'Прилагательное (качественное),  тип склонения по классификации А. Зализняка — 1bX. Корень: -род-; суффикс: -н-; окончание: -ой.':'1bX',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 1a.':'1a',
	'Определительное местоимение (местоименное прилагательное), тип склонения по классификации А. Зализняка — 3b.':'3b',
	'Определительное местоимение (местоименное прилагательное), тип склонения по классификации А. Зализняка — 1a.':'1a',
	'Местоименное прилагательное, тип склонения по классификации А. Зализняка — 1a.':'1a',
	'Местоименное прилагательное, союзное или вопросительное слово, тип склонения по классификации А. Зализняка — 3b.':'3b',
	'Местоимение, указательное, тип склонения по классификации А. Зализняка — <1a>.':'1a',
	'Местоимение, также вопросительное слово, также союз, адъективное склонение, тип склонения по классификации А. Зализняка — <1a>.':'1a',
	'Местоимение (определительное), тип склонения по классификации А. Зализняка — <1f>.':'1f',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 1a.':'1a',
	'Глагол, совершенный вид, переходный, изолированное спряжение, тип спряжения по классификации А. Зализняка — ^b/b(9).':'^b/b(9)',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 7b/b.':'7b/b',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 6°b/c.':'6°b/c',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 5c.':'5c',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 5a.':'5a',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 4c.':'4c',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 4b.':'4b',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 4a.':'4a',
	'Глагол, несовершенный вид, переходный, возвратный, тип спряжения по классификации А. Зализняка — 12b.':'12b',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 5b^.':'5b^',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 4c.':'4c',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 4b.':'4b',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 16b/c.':'16b/c',
	'Глагол, несовершенный вид, непереходный, изолированное спряжение, тип спряжения по классификации А. Зализняка — ^b/b(9). См. также ходить.':'^b/b(9)',
	'Глагол, несовершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 4a.':'4a',
	'Глагол, двувидовой (может образовывать формы совершенного и несовершенного вида), непереходный, возвратный, тип спряжения по классификации А. Зализняка — 4c. В соверш. в. форма дееприч. — жени́вшись. Участники ситуации, описываемой с помощью жениться  в знач. вступать в брак c женщиной:  субъект (им. п.),  супруга (на + предл. п.).':'4c',
###
	'Притяжательное местоимение (местоименное прилагательное), тип склонения по классификации А. Зализняка — <4a>.':'4a',
	'Прилагательное, относительное, тип склонения по классификации А. Зализняка — 1a.':'1a',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 3aX~.':'3aX~',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 1a.':'1a',
	'Глагол, совершенный вид, непереходный, изолированное спряжение, тип спряжения по классификации А. Зализняка — ^a':'^a',
	'Числительное (порядковое прилагательное),  тип склонения по классификации А. Зализняка — 1b':'1b',
	'Числительное, порядковое, адъективное склонение; тип склонения по классификации А. Зализняка — 1b. Соответствующее количественное числительное — семь':'1b',
	'Числительное, порядковое, адъективное склонение; тип склонения по классификации А. Зализняка — 1a. Соответствующее количественное числительное — один':'1a',
	'Числительное (местоименное прилагательное, местоимение), тип склонения 1*b по классификации А. Зализняка':'1*b',
	'Указательное местоимение, тип склонения по классификации А. Зализняка — 3b. Корень: -так-; окончание: -ой':'3b',
	'Указательное местоимение, тип склонения по классификации А. Зализняка — <1a>':'1a',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 6*a- по классификации А. Зализняка); формы мн. ч. предположительны':'6*a',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 1c- по классификации А. Зализняка); формы мн. ч. предположительны':'1c-',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 1*c^) Исчислимое и неисчислимое':'1*c^',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 1b- по классификации А. Зализняка); множественное число предположительно или неупотребимо':'1b-',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 5*b по классификации А. Зализняка); при склонении в основе происходит чередование гласной «е» с «нулём»':'5*b',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 2a)Контроль чего-то/кого-то, за кем-то/чем-то, над кем-то/чем-то':'2a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1a- по классификации А. Зализняка); множественное число предположительно или неупотребимо':'1a-',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1a по классификации А. Зализняка); множественное число морфологически возможно, но на практике неупотребимо или предположительно':'1a',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 3*e по классификации А. Зализняка); формы ед. ч. не используются':'3*e',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 3a по классификации А. Зализняка); формы ед. ч. не используются':'3a',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 1d- по классификации А. Зализняка); формы мн. ч. предположительны или неупотребимы':'1d-',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 1b* по классификации А. Зализняка); образование род. п. мн. ч. затруднительно':'1b*',
	'Притяжательное местоимение, тип склонения по классификации А. Зализняка — 6b':'6b',
	'Притяжательное местоимение (местоименное прилагательное), тип склонения по классификации А. Зализняка — <4a>':'4a',
	'Определительное местоимение (местоименное прилагательное), тип склонения по классификации А. Зализняка — 3b':'3b',
	'Определительное местоимение (местоименное прилагательное), тип склонения по классификации А. Зализняка — 1a':'1a',
	'Местоименное прилагательное, тип склонения по классификации А. Зализняка — 1a':'1a',
	'Местоименное прилагательное, союзное или вопросительное слово, тип склонения по классификации А. Зализняка — 3b':'3b',
	'Местоимение, указательное, тип склонения по классификации А. Зализняка — <1a>':'1a',
	'Местоимение, также вопросительное слово, также союз, адъективное склонение, тип склонения по классификации А. Зализняка — <1a>':'1a',
	'Местоимение (определительное), тип склонения по классификации А. Зализняка — <1f>':'1f',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 7bX':'7bX',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 4a. Готовить к + дат. п. или для + род. п':'4a',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 1*a':'1*a',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 1*a/b':'1*a/b',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 1*a/c\'':'1*a/c\'',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 1a':'1a',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 3b/c\'':'3b/c\'',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 1a/c"':'1a/c"',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 1a/c\'':'1a/c\'',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 1*a/c\'^':'1*a/c\'^',
	'Прилагательное, качественное, тип склонения по классификации А. Зализняка — 1*a':'1*a',
	'Прилагательное, тип склонения по классификации А. Зализняка — 3b/c~':'3b/c~',
	'Прилагательное, тип склонения по классификации А. Зализняка — 1*b~. Полной формы нет':'1*b~',
	'Прилагательное,  тип склонения по классификации А. Зализняка — 1b/c\'':'1b/c\'',
	'Прилагательное, тип склонения по классификации А. Зализняка — 1a/c\'':'1a/c\'',
	'Прилагательное, тип склонения по классификации А. Зализняка — 1a':'1a',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 4a/c':'4a/c',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 3bX~':'3bX~',
	'Прилагательное, относительное, тип склонения по классификации А. Зализняка — 1a':'1a',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 1*a':'1*a',
	'Прилагательное (относительное и качественное), тип склонения по классификации А. Зализняка — 1*a':'1*a',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 4b':'4b',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 4a/b':'4a/b',
	'Прилагательное, качественное, тип склонения по классификации А. Зализняка — 3b/c':'3b/c',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 3a/c"':'3a/c"',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 3a^':'3a^',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 2a/c':'2a/c',
	'Прилагательное (качественное),  тип склонения по классификации А. Зализняка — 1bX. Корень: -род-; суффикс: -н-; окончание: -ой':'1bX',
	'Прилагательное (качественное),  тип склонения по классификации А. Зализняка — 1b/c':'1b/c',
	'Прилагательное, качественное, тип склонения по классификации А. Зализняка — 1a/c\'':'1a/c\'',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 1*a/c"':'1*a/c"',
	'Прилагательное (качественное), тип склонения по классификации А. Зализняка — 1a/b':'1a/b',
	'Прилагательное (качественное),  тип склонения по классификации А. Зализняка — 1a':'1a',
	'Прилагательное (качественное и относительное), тип склонения по классификации А. Зализняка — 1*a':'1*a',
	'Глагол, несовершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 1a':'1a',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 4c':'4c',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 1a':'1a',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 4a':'4a',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 4c':'4c',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 13b':'13b',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 6c':'6c',
	'Глагол, совершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 4a':'4a',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 4b':'4b',
	'Глагол, совершенный вид, переходный, изолированное спряжение, тип спряжения по классификации А. Зализняка — ^b/b(9)':'^b/b(9)',
	'Глагол, совершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 5b':'5b',
	'Глагол, совершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 1a':'1a',
	'Глагол, совершенный вид, непереходный, изолированное спряжение, тип спряжения по классификации А. Зализняка — ^b/b(9)':'^b/b(9)',
	'Глагол, совершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 2a':'2a',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 4a':'4a',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 4c':'4c',
	'Глагол, несовершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 2a':'2a',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — ^b/c[(1)]':'^b/c[(1)]',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 7b/b':'7b/b',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 6°b/c':'6°b/c',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 5a':'5a',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 2a':'2a',
	'Глагол, совершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 4a':'4a',
	'Глагол, совершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 15a':'15a',
	'Глагол, совершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 5a':'5a',
	'Глагол, совершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 3b':'3b',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 5c':'5c',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 5a':'5a',
	'Глагол, несовершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 4a':'4a',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — ^b/c':'^b/c',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — ^b':'^b',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 5c':'5c',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 4c. Спросить что-то кого-то либо у кого-то; спросить о чём-то кого-то либо у кого-то; спросить с кого-то':'4c',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 3bX':'3bX',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 1aX. В знач. захотеть — пожелать + вин. п., инфинитив или придаточное с союзом чтобы; в знач. высказать пожелание — пожелать + дат. п., пожелать + род. п':'1aX',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 16b/c':'16b/c',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 15a':'15a',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 14b/c(1)':'14b/c(1)',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 14b/c\'':'14b/c\'',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 14b/c':'14b/c',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 12a':'12a',
	'Глагол, совершенный вид, переходный, тип спряжения по классификации А. Зализняка — 11a':'11a',
	'Глагол, совершенный вид, переходный, изолированное спряжение, тип спряжения по классификации А. Зализняка — ^a':'^a',
	'Глагол, совершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 9*b/c(1)':'9*b/c(1)',
	'Глагол, совершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 8c/b':'8c/b',
	'Глагол, совершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 7a':'7a',
	'Глагол, совершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 4b':'4b',
	'Глагол, совершенный вид, непереходный, изолированное спряжение, тип спряжения по классификации А. Зализняка — ^a(9)':'^a(9)',
	'Глагол, совершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 6c':'6c',
	'Глагол, совершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 4b':'4b',
	'Глагол, совершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 12a':'12a',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 6°b/cX':'6°b/cX',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 6°b/cX^':'6°b/cX^',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 6°b/c':'6°b/c',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 5c\'^':'5c\'^',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 5b':'5b',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 4b':'4b',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 11b/c':'11b/c',
	'Глагол, несовершенный вид, переходный, возвратный, тип спряжения по классификации А. Зализняка — 4c':'4c',
	'Глагол, несовершенный вид, переходный, возвратный, тип спряжения по классификации А. Зализняка — 12b':'12b',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 5b/c':'5b/c',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 5b^':'5b^',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 4b':'4b',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 4a':'4a',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 16b/c':'16b/c',
	'Глагол, несовершенный вид, непереходный, изолированное спряжение, тип спряжения по классификации А. Зализняка — ^b/b(9). См. также ходить':'^b/b(9)',
	'Глагол, несовершенный вид, непереходный, изолированное спряжение, тип спряжения по классификации А. Зализняка — ^a':'^a',
	'Глагол, несовершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 6c':'6c',
	'Глагол, несовершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 6b':'6b',
	'Глагол, несовершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 6a':'6a',
	'Глагол, несовершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 4b':'4b',
	'Глагол, несовершенный вид, непереходный, возвратный, тип спряжения по классификации А. Зализняка — 4a. Знакомиться + с + тв. п':'4a',
	'Существительное, одушевлённое, мужской род (тип склонения 4c^)':'4c^',
	'Существительное, одушевлённое, мужской род (тип склонения ??)':'??',
	'Существительное, одушевлённое, мужской род, несклоняемое (тип склонения 0)':'0',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 5*a)':'5*a',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 4b)':'4b',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 3e)':'3e',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 3c^)':'3c^',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 3b)':'3b',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 3°a^)':'3°a^',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 2e)':'2e',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 2b)':'2b',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 1c(1))':'1c(1)',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 1°a)':'1°a',
	'Существительное, одушевлённое, мужской род, 1-е склонение (тип склонения 3*a)':'3*a',
	'Существительное, одушевлённое, мужской род, 1-е склонение (тип склонения 2a(2))':'2a(2)',
	'Существительное, одушевлённое, мужской род, 1-е склонение (тип склонения 1a)':'1a',
	'Существительное, одушевлённое, женский род (тип склонения ??)':'??',
	'Существительное, одушевлённое, женский род, 3-е склонение (тип склонения 8e^)':'8e^',
	'Существительное, одушевлённое, женский род, 3-е склонение (тип склонения 8a)':'8a',
	'Существительное, одушевлённое, женский род, 1-е склонение (тип склонения 2a)':'2a',
	'Существительное, одушевлённое, женский род, 1-е склонение (тип склонения 1d)':'1d',
	'Существительное, неодушевлённое, средний род, адъективное склонение (тип склонения <п 3a>)':'3a',
	'Существительное, неодушевлённое, средний род, адъективное склонение (тип склонения <п 1b>)':'1b',
	'Существительное, неодушевлённое, средний род, адъективное склонение (тип склонения <п 1a>)':'1a',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 8°c)':'8°c',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 5a)':'5a',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 3d(1)-)':'3d(1)-',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 3*a(1))':'3*a(1)',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 1d)':'1d',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 6c)':'6c',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 6a)':'6a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 4e)':'4e',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 4a)':'4a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 3*b)':'3*b',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 2*b)':'2*b',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1c(2))':'1c(2)',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1c(1)(2))':'1c(1)(2)',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения (1b))':'1b',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1a((2)))':'1a((2))',
	'Существительное, неодушевлённое, женский род, 3-е склонение (тип склонения 8*b\')':'8*b\'',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 6*d^)':'6*d^',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 3*f\')':'3*f\'',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 2*a^)':'2*a^',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 1*d)':'1*d',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 1*a)':'1*a',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 5*b по классификации А. Зализняка); при склонении в основе происходит чередование гласной е с «нулём»':'5*b',
	'Существительное, неодушевлённое, женский род, адъективное склонение (тип склонения 1a)':'1a',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 2a)':'2a',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 1d\')':'1d\'',
	'Прилагательное, относительное, тип склонения по классификации А. Зализняка — 3aX~':'3aX~',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 2*a-. Краткая форма муж. р. предположительна':'2*a-',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 1a':'1a',
	'Местоимение (притяжательное), тип склонения по классификации А. Зализняка — 6b':'6b',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 5b':'5b',
	'Глагол, несовершенный вид, непереходный, тип спряжения по классификации А. Зализняка — 1a':'1a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 3c(1))':'3c(1)',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 4a':'4a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 3a)':'3a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1a)':'1a',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 1a^)':'1a^',
	'Существительное, одушевлённое, женский род, 1-е склонение (тип склонения 3a)':'3a',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 1*d)':'1*d',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 1c)':'1c',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 1a^)':'1a^',
	'Существительное, неодушевлённое, мужской род, несклоняемое (тип склонения 0)':'0',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1*b)':'1*b',
	'Существительное, неодушевлённое, женский род (тип склонения ??)':'??',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 2a)':'2a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 3*a)':'3*a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1b)':'1b',
	'Существительное, неодушевлённое, женский род, 3-е склонение (тип склонения 8e)':'8e',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 1d)':'1d',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 5a)':'5a',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 1a)':'1a',
	'Существительное, неодушевлённое, женский род, 3-е склонение (тип склонения 8a)':'8a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1c(1))':'1c(1)',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 2b)':'2b',
	'Существительное, неодушевлённое, мужской род (тип склонения ??)':'??',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 7a)':'7a',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 1a':'1a',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 7a)':'7a',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 4a)':'4a',
	'Существительное, одушевлённое, женский род, 1-е склонение (тип склонения 1a)':'1a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1c)':'1c',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 3a)':'3a',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 3a)':'3a',
	'Существительное, одушевлённое, женский род, 1-е склонение (тип склонения 3*a)':'3*a',
	'Прилагательное, тип склонения по классификации А. Зализняка — 1*a':'1*a',
	'Прилагательное (относительное), тип склонения по классификации А. Зализняка — 3aX~':'3aX~',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 1a)':'1a',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 3*a)':'3*a',
	'Существительное, неодушевлённое, средний род, несклоняемое (тип склонения 0)':'0',
	'Существительное, одушевлённое, женский род, 1-е склонение (тип склонения 5a)':'5a',
	'Существительное, одушевлённое, мужской род, 2-е склонение (тип склонения 1a)':'1a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 4b)':'4b',
	'Прилагательное, тип склонения по классификации А. Зализняка — 3aX~':'3aX~',
	'Существительное, неодушевлённое, женский род, 1-е склонение (тип склонения 2*a)':'2*a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 2a)':'2a',
	'Существительное, неодушевлённое, средний род, 2-е склонение (тип склонения 6*a)':'6*a',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 2a':'2a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 1a по классификации А. Зализняка); множественное число морфологически возможно, но на практике неупотребимо или предположительн':'1a',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 3b)':'3b',
	'Существительное, неодушевлённое, мужской род, 2-е склонение (тип склонения 3a)':'3a',
	'Глагол, несовершенный вид, переходный, тип спряжения по классификации А. Зализняка — 7b/b':'7b/b'
};

def strip_html(s): #{
	o = '';
	inTag = False;
	for c in s: #{
		if c == '<': #{
			inTag = True;
			continue;
		#}
		if c == '>': #{
			inTag = False;
			continue;
		#}
		if not inTag: #{
			o = o + c;
		#}
	#}
	return o.replace('&#160;', ' ').replace('&lt;', '<').replace('&gt;', '>');
#}

def clean_decl(s): #{
	o = s;
	o = o.replace(' по классификации А. Зализняка).', ')');
	return o.strip(' .');
#}

russian = False;
printing = False;
decl_list = [];
for line in sys.stdin.readlines(): #{
	line = line.strip(' .');
	if line.count('<h1>Русский</h1>') > 0: #{
		russian = True;
	#}
	if line.count('<h1>Русский</h1>') < 1 and line.count('<h1>') > 0: #{
		russian = False;
	#}
	if line.count('Морфологические и синтаксические свойства') > 0: #{
		printing = True;
	#}
	if line.count('Произношение') > 0: #{
		printing = False;
	#}

	if printing and russian: #{
		if line.count('Зализняка') > 0: #{
			sline = strip_html(line);
			decl_list.append(clean_decl(sline).strip());
		#}
	#}
#}
decl_list = list(set(decl_list));

output = '';
if len(decl_list) == 1: #{
	for item in decl_list: #{
		if item.count('Соответствующий глагол') > 0: #{
			item = item.split('Соответствующий глагол')[0].strip(' .');
		#} 
		if item.count('Соответствующие глаголы') > 0: #{
			item = item.split('Соответствующие глаголы')[0].strip(' .');
		#}
		if item.count('Соответствующего глагола') > 0: #{
			item = item.split('Соответствующего глагола')[0].strip(' .');
		#}
		if item.count('Сравнительная степень') > 0: #{
			item = item.split('Сравнительная степень')[0].strip(' .');
		#}
		if item.count('В качестве') > 0: #{
			item = item.split('В качестве')[0].strip(' .');
		#}
		if item.count('Форма прич.') > 0: #{
			item = item.split('Форма прич.')[0].strip(' .');
		#}
		if item.count('Прич. страд.') > 0: #{
			item = item.split('Прич. страд.')[0].strip(' .');
		#}
		if item.count('Соответствующее количественное') > 0: #{
			item = item.split('Соответствующее количественное')[0].strip(' .');
		#}
		if item.count('В сочетаниях') > 0: #{
			item = item.split('В сочетаниях')[0].strip(' .');
		#}
		if item in conversion_table: #{
			output = output + ' | ' + conversion_table[item];
		elif item+'.' in conversion_table: #{
			output = output + ' | ' + conversion_table[item+'.'];
		else: #{
			output = output + ' | ' + item ;
		#}
	#}
#}
print(output);
