#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

panic = 'Panik'
cancel = 'Abbrechen'
all = 'Alles'
stop = 'Beenden'
group1 = ('Tomaten', 'Tomaten 1', 'Tomaten 2', 'Tomaten 3')
group2 = ('Chilis', 'Chili 1', 'Chili 2', 'Chili 3')
group3 = ('Reserve', 'Reserve 1', 'Reserve 2')

# messages
msg_welcome = '`Willkommen {}, lass uns Pflanzen bewässern!\n`'
msg_stop = '`Na dann, tschüss {}!\nZum nächsten Wässern geht\'s mit /start`'
msg_duration = '`Bewässerungsdauer für \'{}\' in Sekunden angeben:`'
water_on = '`\'{}\' wird jetzt für {}s gewässert.`'
water_on_group = '`Alle {} werden jetzt für {}s gewässert.`'
water_on_all='`{} wird jetzt für {}s gewässert.`'
water_off = '`Bewässerung von \'{}\' nach {}s beendet.\n\n`'
water_off_group = '`Bewässerung von allen {} wurde nach {}s beendet.\n\n`'
water_off_all='`Komplettbewässerung wurde nach {}s beendet.`\n\n'
msg_choice = '`Bitte auswählen:`'
msg_new_choice = '`Neue Auswahl oder Beenden?`'
msg_panic='*Panik-Modus! \nVersuch was Spezielles!*'
private_warning = '`Hallo {}, dies ist ein privater Bot!\nDeine ChatID: {} ist geblockt.`'