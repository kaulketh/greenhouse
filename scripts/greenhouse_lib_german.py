#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Thomas Kaulke, kaulketh@gmail.com

empty = ' '

# commands and descriptions
panic = 'Panik'
cancel = 'Abbrechen'
all = 'Alles'
stopBot = 'Beenden'
group1 = ('Ventile 1 bis 3', 'Ventil 1', 'Ventil 2', 'Ventil 3')
group2 = ('Ventile 6 bis 8', 'Ventil 6', 'Ventil 7', 'Ventil 8')
group3 = ('Ventil 4 und 5', 'Ventil 4', 'Ventil 5')

# keybord configs
kb1 = [[group1[1], group1[2], group1[3]],
       [group3[1], group3[2]],
       [group2[1], group2[2], group2[3]],
       [group1[0], group3[0], group2[0]],
       [all, stopBot]
       ]
kb2 = [[cancel, stopBot]]

# messages
msg_welcome = '`Willkommen {}, lass uns Ventile öffnen!\n`'
msg_stop = '`Na dann, tschüss {}!`'
msg_duration = '`Öffnungszeit für \'{}\' in Sekunden angeben:`'
water_on = '`\'{}\' wird jetzt für {}s geöffnet.`'
water_on_group = '`Die {} werden jetzt für {}s geöffnet.`'
water_on_all = '`\'{}\' wird jetzt für {}s geöffnet.`'
water_off = '`\'{}\' nach {}s wieder geschlossen.\n\n`'
water_off_group = '`\'{}\' wurden nach {}s geschlossen.\n\n`'
water_off_all = '`Alles wurde nach {}s geschlossen.`\n\n'
msg_choice = '`Bitte auswählen:`'
msg_new_choice = '`Neue Auswahl oder Beenden?`'
msg_panic = '*Panik-Modus! \nVersuch was Spezielles!*'
private_warning = '`Hallo {}, dies ist ein privater Bot!\nDeine ChatID: {} ist geblockt worden.`'
