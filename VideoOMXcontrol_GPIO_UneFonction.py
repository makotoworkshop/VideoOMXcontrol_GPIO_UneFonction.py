#!usr/bin env python3
# Ressources
# https://github.com/Douglas6/omxcontrol
# https://forums.framboise314.fr/viewtopic.php?t=3548
#
# Programme qui joue une playliste de vidéo
# La première vidéo est jouée en boucle
# Si on sélectionne la vidéo suivante ou précédente, elle est à son tour jouée en boucle
# Une seule fonction par boutons

from omxcontrol import *
import subprocess, time
import RPi.GPIO as GPIO
import os

#############
# Init GPIO #
#############
PIN_PLAY = 31           # GPIO06, Play/Pause/Stop
PIN_VOLMOINS = 35       # GPIO19, Volume -
PIN_VOLPLUS = 37        # GPIO26, Volume +
PIN_PRECEDENT = 38      # GPIO20, Précédent
PIN_SUIVANT = 36        # GPIO16, Suivant

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(PIN_PLAY, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_VOLMOINS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_VOLPLUS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_PRECEDENT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_SUIVANT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

####################
# Ressources Vidéo #
####################
#video1 = '/home/pi/deathsml_15-07-2015_1cc_h264-21.mp4'
#video2 = '/home/pi/dodonpachi_23-02-2014_montage.avi'
#video3 = '/home/pi/deathsml_15-07-2015_1cc_h264-21.mp4'
#video4 = '/home/pi/dodonpachi_23-02-2014_montage.avi'
def Selection(i):
    switcher={
        0:'/home/pi/deathsml_15-07-2015_1cc_h264-21.mp4',
        1:'/home/pi/dodonpachi_23-02-2014_montage.avi',
        2:'/home/pi/deathsml_15-07-2015_1cc_h264-21.mp4',
        3:'/home/pi/dodonpachi_23-02-2014_montage.avi',
        }
    return switcher.get(i,"Séléction Invalide")

vid = 0

os.system('sudo pkill omxplayer')       # S'assure qu'aucune instance omxplayer ne tourne encore, en cas de plantage
# omxplayer /home/pi/deathsml_15-07-2015_1cc_h264-21.mp4 --aspect-mode stretch -o local
subprocess.Popen(['omxplayer','--aspect-mode', 'stretch', '-o', 'local', Selection(vid)], stdin=subprocess.PIPE)
time.sleep(3)

#####################
# Boucle Principale #
#####################
while True:
    try:
        omx = OmxControl()      # appel librairie OmxControl

        if GPIO.input(PIN_PLAY) == 0: # Button pressed
            print("Button Play/Pause/Stop pressé")      # un appuie long pour STOP
            omx.action(OmxControl.ACTION_PAUSE)

        if GPIO.input(PIN_VOLMOINS) == 0: # Button pressed
            print("Button Volume - pressé")
            omx.action(OmxControl.ACTION_DECREASE_VOLUME)

        if GPIO.input(PIN_VOLPLUS) == 0: # Button pressed
            print("Button Volume + pressé")
            omx.action(OmxControl.ACTION_INCREASE_VOLUME)

        if GPIO.input(PIN_PRECEDENT) == 0: # Button pressed
            print("Button Précédent pressé")            # un appuis long pour Vidéo précédente
#            omx.action(OmxControl.ACTION_SEEK_BACK_SMALL)
            omx.action(OmxControl.ACTION_EXIT)          # Stopper la lecture et tombe donc en erreur via Try > Except
            vid = vid - 1       # pour lire la vidéo précédente
            if vid == -1:
                vid = 3
            print('vid : ',vid)

        if GPIO.input(PIN_SUIVANT) == 0: # Button pressed
            print("Button Suivant pressé")              # un appuie long pour Vidéo suivante
         #   omx.action(OmxControl.ACTION_SEEK_FORWARD_SMALL)
            omx.action(OmxControl.ACTION_EXIT)          # Stopper la lecture et tombe donc en erreur via Try > Except
            vid = vid + 1       # pour lire la vidéo suivante
            if vid == 4:
                vid = 0
            print('vid : ',vid)

    except OmxControlError as ex:       # si le controle ne voit plus D-Bus, relance la vidéo
        print("ERROR contrôle D-Bus")
        print('Selection : ',Selection(vid))
        subprocess.Popen(['omxplayer','--aspect-mode', 'stretch', '-o', 'local', Selection(vid)], stdin=subprocess.PIPE)
        time.sleep(3)   # tempo pour laisser le temps au player vidéo de démarrer

    time.sleep(0.1)     # délay de répétition de pression sur le bouton si on le maintient enfoncé

#####################################################
# Fonctions disponible dans la librairie OmxControl #
#####################################################
#ACTION_DECREASE_SPEED
#ACTION_INCREASE_SPEED
#ACTION_REWIND
#ACTION_FAST_FORWARD
#ACTION_SHOW_INFO
#ACTION_PREVIOUS_AUDIO
#ACTION_NEXT_AUDIO
#ACTION_PREVIOUS_CHAPTER
#ACTION_NEXT_CHAPTER
#ACTION_PREVIOUS_SUBTITLE
#ACTION_NEXT_SUBTITLE
#ACTION_TOGGLE_SUBTITLE
#ACTION_DECREASE_SUBTITLE_DELAY
#ACTION_INCREASE_SUBTITLE_DELAY
#ACTION_EXIT
#ACTION_PAUSE
#ACTION_DECREASE_VOLUME
#ACTION_INCREASE_VOLUME
#ACTION_SEEK_BACK_SMALL
#ACTION_SEEK_FORWARD_SMALL
#ACTION_SEEK_BACK_LARGE
#ACTION_SEEK_FORWARD_LARGE
#ACTION_SEEK_RELATIVE
#ACTION_SEEK_ABSOLUTE
#ACTION_STEP
#ACTION_BLANK
#ACTION_MOVE_VIDEO
#ACTION_HIDE_VIDEO
#ACTION_UNHIDE_VIDEO
#ACTION_HIDE_SUBTITLES

