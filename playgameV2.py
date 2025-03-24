# An updated version to a game I made for a final project in highschool.
# Written in Python using pygame
# Made by Michael Onate
# March 21, 2025


# -- OLD NOTES -- 
# I used a tutorial to help make this game. 
# The link to the playlist is below:
# https://www.youtube.com/playlist?list=PLjcN1EyupaQnHM1I9SmiXfbT6aG4ezUvu      


import os
import pygame
import random
from pygame import mixer
from pygame.locals import *
import sys, os
from os import path
import time
import subprocess

#Initializations
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
mixer.init()


WIDTH = 800
HEIGHT = 800
FPS = 60


#Hex codes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
GREY = (50,50,50)

#Create Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Sussy Boy Part II (Enhanced Edition)")
icon = pygame.image.load('textures/icon.png')
pygame.display.set_icon(icon)
background1 = pygame.image.load('textures/bg_1.jpg')

#UI Elements
restart_img = pygame.image.load('ui/restart.png')
start_btn = pygame.image.load('ui/start.png')
exit_btn = pygame.image.load('ui/exit.png')
closet_btn = pygame.image.load('ui/closet.png')
clear_btn = pygame.image.load('ui/clear.png')
level_edit_img = pygame.image.load('ui/leveledit.png')
playcustom_btn = pygame.image.load('ui/playcustom.png')

        #Shop UI
shopbg = pygame.image.load('ui/shopbg.png')
equippedico = pygame.image.load('ui/selected.png')
lockedico = pygame.image.load('ui/locked.png')


buyico = pygame.image.load('ui/buy.png')
price500ico = pygame.image.load('ui/500.png')
price1500ico = pygame.image.load('ui/1500.png')
price3000ico = pygame.image.load('ui/3000.png')
price10000ico = pygame.image.load('ui/10000.png')
icon60s = pygame.image.load('ui/60s.png')

cyanPrev = pygame.image.load('skins/cyan/prev.png')
purplePrev = pygame.image.load('skins/purple/prev.png')
greenPrev = pygame.image.load('skins/green/prev.png')
redPrev = pygame.image.load('skins/red/prev.png')
blackPrev = pygame.image.load('skins/black/prev.png')
pinkPrev = pygame.image.load('skins/pink/prev.png')
bluePrev = pygame.image.load('skins/blue/prev.png')
copPrev = pygame.image.load('skins/cop/prev.png')
goldPrev = pygame.image.load('skins/gold/prev.png')




#Gameplay Variables
tile_size = 50
game_over = 0
title_screen = True
closet_open = False
playing_custom = False


#INT STOPWATCH
clock = pygame.time.Clock()
minutes = 0
seconds = 0
milliseconds = 0
realmins = 0
timeInSeconds = 0

current_time = 0     # Counting the time since start of pygame & resets to 0 when game starts.
fire_time = 0

deathCountReal = 0

finalMilliseconds = 0
finalSeconds = 0
finalMinutes = 0
finalRealMins = 0
finalTimeInSeconds = 0 


    #Fonts
font_level = pygame.font.SysFont('Calibri', 30)
font_title = pygame.font.SysFont('Engravers MT', 50)
font_small = pygame.font.SysFont("Calibri", 20)
font_win = pygame.font.SysFont('Engravers MT', 50)
font_win_big = pygame.font.SysFont('Engravers MT', 53)
font_hint = pygame.font.SysFont('Calibri', 18)
font_timer = pygame.font.SysFont('Calibri', 18)
font_titleinfo = pygame.font.SysFont('Engravers MT', 30)


#SFX                                                                                                                                            --Sound Effects
pygame.mixer.music.load('sfx/music.wav')
pygame.mixer.music.play(-1, 0.0, 6000)
pygame.mixer.music.set_volume(0.8)

jump_sfx = pygame.mixer.Sound('sfx/jump.wav')
jump_sfx.set_volume(0.5)

star_sfx = pygame.mixer.Sound('sfx/wow.wav')
star_sfx.set_volume(1.5)


dead_sfx = pygame.mixer.Sound('sfx/boom.wav')
dead_sfx.set_volume(0.5)

dead_slice_sfx = pygame.mixer.Sound('sfx/dead.wav')

dead_wasted_sfx = pygame.mixer.Sound('sfx/wasted.wav')
dead_wasted_sfx.set_volume(1.5)

dead_lego_sfx = pygame.mixer.Sound('sfx/lego.wav')
dead_lego_sfx.set_volume(1)

dead_bonk_sfx = pygame.mixer.Sound('sfx/bonk.wav')
dead_bonk_sfx.set_volume(1)

click_sfx = pygame.mixer.Sound('sfx/msclick.wav')
click_sfx.set_volume(1.0)

chaching_sfx = pygame.mixer.Sound('sfx/chaching.wav')
chaching_sfx.set_volume(1.0)

err_sfx = pygame.mixer.Sound('sfx/error.wav')
err_sfx.set_volume(1.0)

tada_sfx = pygame.mixer.Sound('sfx/tada.wav')



#Load custom level file
customExists = False
# if os.path.exists('customPreview.txt'):
#     customExists = True
#     with open('customPreview.txt', 'r') as file:
#         custom_level_data = file.readlines()

#     def load_custom_level(data):
#         custom_world = []
#         for line in data:
#             row = list(map(int, line.split()))
#             custom_world.append(row)
#         return custom_world

#     world_0 = load_custom_level(custom_level_data)
#     print("Custom level loaded successfully:")
#     for row in world_0:
#         print(row)
# else:
#     print("Custom level file not found. Using placeholder for world_0.")

def load_custom_level_from_file():
    """
    Replaces the placeholder world_0 with the custom level data from customPreview.txt.
    """
    global world_0, customExists
    if os.path.exists('customPreview.txt'):
        with open('customPreview.txt', 'r') as file:
            custom_level_data = file.readlines()

        def parse_custom_level(data):
            custom_world = []
            for line in data:
                row = list(map(int, line.split()))
                custom_world.append(row)
            return custom_world

        world_0 = parse_custom_level(custom_level_data)
        customExists = True
        print("Custom level loaded successfully:")
        for row in world_0:
            print(row)
    else:
        customExists = False
        # print("Custom level file not found. Using placeholder for world_0.")




#Load Player Stats File
with open('playerstats.txt','r') as file:
    lineData = file.readlines()
#Int values to hold unlock values
pointsSave = str(lineData[0])[0:len(str(lineData[0])) -1]
pointsSave = int(pointsSave)


blackSave = str(lineData[1])[0:1]
blackSave = int(blackSave)


cyanSave = str(lineData[2])[0:1]
cyanSave = int(cyanSave)

greenSave = str(lineData[3])[0:1]
greenSave = int(greenSave)

pinkSave = str(lineData[4])[0:1]
pinkSave = int(pinkSave)

purpleSave = str(lineData[5])[0:1]
purpleSave = int(purpleSave)

redSave = str(lineData[6])[0:1]
redSave = int(redSave)

blueSave = str(lineData[9][0:1])
blueSave = int(blueSave)

copSave = str(lineData[10][0:1])
copSave = int(blueSave)

goldSave = str(lineData[11][0:1])
goldSave = int(goldSave)

bestRealMinsStr = str(lineData[13])
bestRealMinsLength = int(len(bestRealMinsStr) - 1)
bestRealMins = str(lineData[13][0:bestRealMinsLength])
bestRealMins = int(bestRealMins)

bestMinsStr = str(lineData[14])
bestMinsLength = int(len(bestMinsStr) - 1)
bestMins = str(lineData[14][0:bestMinsLength])
bestMins = int(bestMins)

bestSecStr = str(lineData[15])
bestSecLength = int(len(bestSecStr) - 1)
bestSec = str(lineData[15][0:bestSecLength])
bestSec = int(bestSec)

timeStr = str(lineData[16])
timeStrLength = int(len(timeStr) - 1)    
bestTime = str(lineData[16][0:timeStrLength])
bestTime = int(bestTime)

bestDeathsStr = str(lineData[17])
bestDeathsLength = int(len(bestDeathsStr) - 1)    
bestDeaths = str(lineData[17][0:bestDeathsLength])
bestDeaths = int(bestDeaths)

shouldDrawGrid = False

print("")
print("Loading...")
time.sleep(.5)
print("")
print("Save Data Loaded")

if customExists == True:
      print("Custom Level = True")
      print("Custom level grid data:")
      for row in world_0:
        print(row)
      print("")
else:
        print("Custom Level = False")
        print("")

#print("Dough: " + str(pointsSave))
#print("hasBlack: " + str(blackSave))
#print("hasCyan: " + str(cyanSave))
#print("hasGreen: " + str(greenSave))
#print("hasPink: " + str(pinkSave))
#print("hasPurple: " + str(purpleSave))
#print("hasRed: " + str(redSave))
#print("hasBlue: " + str(blueSave))
#print("hasCop: " + str(copSave))
#print("hasGold: " + str(goldSave))


activeskin = str(lineData[7])[0:len(str(lineData[7])) -1]

activedeath = str(lineData[8])[0:1]
activedeath = int(activedeath)

deathMessage = ""
randomNumber = 1
randomNumber2 = 0

def playDeath():
    global randomNumber2
    randomNumber2 = random.randint(0,4)
    if randomNumber2 == 0:
        #print("played default death")
        dead_sfx.play()
    elif randomNumber2 == 1:
        #print("played wasted death")
        dead_wasted_sfx.play()
    elif randomNumber2 == 2:
        #print("played lego death")
        dead_lego_sfx.play()
    elif randomNumber2 == 3:
        dead_bonk_sfx.play()
    elif randomNumber2 == 4:
        dead_slice_sfx.play()

def setDeathMessage():
    global deathMessage
    if randomNumber == 1:
        deathMessage = "bro."
    elif randomNumber == 2:  # Fixed assignment
        deathMessage = "cmon now."
    elif randomNumber == 3:
        deathMessage = "LOCK IN"
    elif randomNumber == 4:
        deathMessage = "it's not even that hard"
    elif randomNumber == 5:
        deathMessage = "What a save!"
    elif randomNumber == 6:
        deathMessage = "Wow!"
    elif randomNumber > 4 and randomNumber2 == 1:
        deathMessage = "Nice one!"
    elif randomNumber > 6 and deathCountReal > 20:
        deathMessage = "you've died " + str(deathCountReal) + " times now."
    elif randomNumber == 7:
        deathMessage = "red vented."
    elif randomNumber == 8:
        deathMessage = "how."
    elif randomNumber == 9:
        deathMessage = "folded."
    elif randomNumber == 10:
        deathMessage = "get up"
    elif randomNumber > 7 and deathCountReal > 30:
        deathMessage = "just uninstall at this point"

##########################################################################----------WORLDS----------################################################################
world_0 = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,15,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]




world_1=[
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,15,0,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

world_2= [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,15,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,7,8,9,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,7,8,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,8,0,0,0,0,0,1],
[1,2,2,2,2,2,12,12,12,12,12,12,12,12,12,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

world_3= [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,15,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,2,1,0,0,0,0,0,1],
[1,0,0,0,0,0,0,2,1,1,0,0,0,0,0,1],
[1,0,0,0,0,0,2,1,1,1,0,0,0,0,0,1],
[1,0,0,0,0,2,1,1,1,1,0,0,0,0,0,1],
[1,0,0,0,2,1,1,1,1,1,0,11,0,11,0,1],
[1,2,2,2,1,1,1,1,1,1,2,2,2,2,2,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

world_4= [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,15,0,0,0,0,0,0,0,0,0,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

world_5= [
[13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13],
[13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13],
[13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13],
[13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13],
[13,0,0,13,0,0,0,0,0,0,0,0,0,0,0,13],
[13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13],
[13,0,0,0,0,0,0,0,0,0,0,13,0,13,13,13],
[13,0,0,0,0,0,13,0,0,0,0,13,0,0,0,13],
[13,0,0,0,0,0,0,0,0,0,0,0,13,0,0,13],
[13,0,0,0,0,0,0,0,0,13,13,13,0,0,0,13],
[13,0,0,0,13,13,0,0,13,0,0,0,0,0,0,13],
[13,0,0,0,0,0,0,0,0,13,0,0,0,15,0,13],
[13,0,0,0,0,0,0,0,0,13,0,0,0,0,0,13],
[13,13,0,13,0,0,0,0,13,0,0,0,0,0,0,13],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

world_6= [
[4,4,4,4,4,14,14,14,14,14,14,14,14,14,14,14],
[14, 0,0,0,0,0,0,15,0,0,0,0,0,11,0,14],
[14, 0,0,0,0,0,11,0,0,0,0,0,0,0,0,14],
[14, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
[14, 0,0,11,0,0,0,0,0,0,0,0,0,5,0,14],
[14, 0,0,0,5,0,0,0,0,0,0,0,0,0,0,14],
[14, 11,0,0,0,0,0,0,0,0,0,5,0,0,0,14],
[14, 0,5,0,0,0,0,0,0,0,0,0,0,0,0,14],
[14, 0,0,0,0,0,0,0,0,5,0,0,0,0,0,14],
[14, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
[14, 0,0,0,0,0,0,0,0,0,0,0,0,5,0,14],
[14, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
[14, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,14],
[14, 0,5,0,0,0,0,0,0,0,5,0,0,0,0,14],
[14,14,5,14,14,14,14,14,14,14,14,14,14,14,14,14],
]

world_7= [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,15,0,12,0,12,0,12,0,12,0,0,0,0,0,1],
[1,9,0,7,8,8,8,8,8,8,8,9,0,0,5,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,5,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,5,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,5,1],
[1,0,0,0,0,0,11,0,0,2,12,12,12,12,12,1],
[1,2,2,2,2,2,2,2,2,1,14,14,14,14,14,1],
]

world_8= [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,14],
[1,0,0,0,1,0,0,0,0,0,12,0,0,0,0,14],
[1,0,2,0,0,0,0,2,14,8,8,8,9,0,0,14],
[1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,14],
[1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,14],
[1,0,1,0,2,0,0,1,0,0,0,11,0,0,0,14],
[1,0,1,0,1,0,0,1,0,7,8,8,8,8,8,14],
[1,0,1,0,1,0,0,14,0,0,0,0,0,0,0,14],
[1,0,1,0,1,0,0,0,0,0,0,11,0,0,15,14],
[1,0,1,0,1,0,0,0,0,0,0,0,0,0,7,1],
[1,0,1,0,1,0,0,14,0,0,0,0,0,0,0,1],
[1,0,1,0,1,0,0,1,0,2,0,0,0,0,0,1],
[1,12,1,12,1,12,12,1,12,1,12,12,12,12,12,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

world_9= [
[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
[4,15,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,12,12,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,5,5,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,4,4,4,4,4,0,0,11,0,4,4,4,4,4,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,12,0,0,0,0,0,0,0,0,0,0,4],
[4,0,4,4,14,4,0,0,0,11,4,4,4,4,4,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,4,4,4,4,4,13,11,0,0,4,14,4,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
]

world_10= [
[15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15],
[15,13,13,13,13,13,13,13,13,13,13,13,13,13,13,15],
[15,13,0,0,0,0,0,0,0,0,0,0,0,0,13,15],
[15,13,0,0,0,0,0,0,0,0,0,0,0,0,0,15],
[15,13,0,0,0,0,0,0,0,0,0,0,0,5,13,15],
[15,13,0,0,7,8,9,0,7,8,9,0,0,0,13,15],
[15,13,0,0,0,0,0,0,0,0,0,0,0,0,13,15],
[15,13,0,0,0,0,0,0,0,0,0,0,0,5,13,15],
[15,13,7,8,9,0,0,0,0,0,0,0,0,0,13,15],
[15,13,0,0,0,0,0,0,0,0,0,0,0,0,13,15],
[15,13,0,0,0,0,0,7,8,9,0,0,0,5,13,15],
[15,13,0,0,0,0,0,0,0,0,0,0,0,0,13,15],
[15,13,0,0,0,0,0,0,0,0,0,7,8,9,13,15],
[15,13,13,13,13,13,13,13,13,13,13,13,13,13,13,15],
[15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15],
]

world_11=[
[1,1,1,1,0,15,0,1,1,1,1,1,1,1,1,1],
[13,11,11,11,0,0,11,11,11,11,11,11,11,11,11,13],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,8,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,9,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,7,0,0,8,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,9,0,1],
[1,0,0,0,0,0,0,0,0,0,0,8,0,0,0,1],
[1,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
[1,0,0,0,0,7,9,0,0,0,0,0,0,0,0,1],
[1,0,0,0,11,11,11,11,11,11,11,11,11,11,11,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

world_12=[
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,2,2,2,2,2,2,0,0,2,2,2,2,2,2,1],
[1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,0,0,1,0,0,0,0,1,1],
[1,1,1,1,1,1,1,0,0,1,0,0,0,0,1,1],
[1,1,1,1,1,1,1,0,0,1,0,0,0,0,1,1],
[1,1,1,1,1,1,1,0,0,1,15,0,0,0,1,1],
[1,1,1,1,1,1,1,0,0,1,5,0,0,0,1,1],
[1,1,1,1,1,1,1,0,0,1,1,1,0,0,1,1],
[1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

world_13=[
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,2,2,2,2,2,2,0,15,11,15,0,0,2,2,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

world_14=[
[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
[5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5],
[5,0,15,0,0,0,0,0,0,0,0,0,0,0,0,5],
[5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,5],
[5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,5],
[5,0,4,0,4,4,0,0,4,0,0,4,0,0,0,5],
[5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,5],
[5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,5],
[5,0,0,0,0,0,0,0,0,0,0,0,4,0,0,5],
[5,0,0,0,0,0,0,0,0,0,0,0,4,0,0,5],
[5,0,0,0,0,0,0,0,4,0,0,0,4,0,0,5],
[5,0,0,0,0,0,0,0,4,0,0,0,4,0,0,5],
[5,0,0,0,4,0,0,0,4,0,0,0,4,0,0,5],
[5,12,4,12,4,12,12,12,4,12,12,12,4,12,12,5],
[5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
]

world_15=[
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,15,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

##########################################################################--------/\-WORLDS-/\-------################################################################



level = 1
max_levels = 15


#Custom Functions

def draw_text(text, font, text_col, x ,y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x,y))


def reset_level(level):
        player.reset(100, HEIGHT - 130)
        leaf_group.empty()
        lava_group.empty()
        exit_group.empty()
        lavabig_group.empty()
        world = World(world_data)

        return world
        
        


def draw_grid():
	for line in range(0, 16):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (WIDTH, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, HEIGHT))

class UI():
    action = False
    
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
      

    def draw(self):
        action = False
        
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action


class Player():
        def __init__(self, x, y):
               self.reset(x, y)

        def update(self, game_over):
                global deathCountReal
                dx = 0
                dy = 0
                walk_cooldown = 1
                can_jump = False
                

                if game_over == 0:
                #movement
                        global randomNumber
                        global musicIsMuted
                        key = pygame.key.get_pressed()
                        if key[pygame.K_SPACE] and self.jumped == False and self.jumpcount <= 1:
                                #set jump height
                                jump_sfx.play()
                                self.vel_y = -10
                                self.jumped = True
                                self.jumpcount += 1



                        # if key[pygame.K_m]:
                        #    if musicIsMuted == False:
                        #        pygame.mixer.music.stop()
                        #        musicIsMuted = True
                        #        time.sleep(.1)
                        #    else:
                        #        pygame.mixer.music.play()
                        #        musicIsMuted = False
                        #        time.sleep(.1)
#Suicide script
                        if key[pygame.K_k]:                               #Kill yourself
                               game_over = -1
                               #print(randomNumber2)
                               playDeath()
                               randomNumber = random.randint(1,10)
                               #print("NUM = " + str(randomNumber))
                               setDeathMessage()
                               pygame.mixer.music.stop()
                               deathCountReal += 1
#cheats
                        # if key[pygame.K_u]:
                        #         global pointsSave
                        #         pointsSave += 200
                        #         chaching_sfx.play()
                        # if key[pygame.K_y]:                                 #Advance to next level immediately
                        #         global level
                        #         print("Skipping...")
                        #         # level += 1
                        #         game_over = 1





                        if key[pygame.K_SPACE] == False:
                                self.jumped = False
                        if key[pygame.K_a]:
                                self.counter += 1
                                dx -= 4
                                self.direction = -1
                        if key[pygame.K_d]:
                                self.counter += 1
                                dx += 4
                                self.direction = 1
                        if key[pygame.K_d] == False and key[pygame.K_a] == False:
                                self.counter = 0
                                self.index = 0
                                if self.direction == 1:
                                        self.image = self.images_right[self.index]
                                if self.direction == -1:
                                        self.image = self.images_left[self.index]



                #Animations
                        if self.counter > walk_cooldown:
                                self.counter = 0
                                self.index += 1
                                if self.index == len(self.images_right):
                                        self.index = 0

                                if self.direction == 1:
                                        self.image = self.images_right[self.index]
                                if self.direction == -1:
                                        self.image = self.images_left[self.index]
                        
                

                #Calc velocity (set gravity)
                        self.vel_y += .5
                        if self.vel_y > 10:
                                self.vel_y = 10
                        
                        dy += self.vel_y


                        #check collision
                        self.airborne = True
                        for tile in world.tile_list:
                                #check x pos
                                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                                        dx = 0
                                        can_jump = True
                                        
                                #check y pos
                                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                                        #check if ground below (jumping)
                                        if self.vel_y < 0:
                                                dy = tile[1].bottom - self.rect.top
                                                self.vel_y = 0
                                        elif self.vel_y > 0:
                                                dy = tile[1].top - self.rect.bottom                
                                                self.vel_y = 0
                                                self.airborne = False
                                                self.jumpcount = 0 

                        #Check Collision                                                                                                        --Check Collision
                        
                        if pygame.sprite.spritecollide(self, leaf_group, False):
                                randomNumber = random.randint(1,7)
                                #randomNumber2 = random.randint(0,3)
                                setDeathMessage()
                                #print(randomNumber)
                                game_over = -1
                                playDeath()
                                pygame.mixer.music.stop()
                                deathCountReal += 1

                        if pygame.sprite.spritecollide(self, lava_group, False):
                                randomNumber = random.randint(1,7)
                                #randomNumber2 = random.randint(0,3)
                                setDeathMessage()
                                #print(randomNumber)
                                game_over = -1
                                playDeath()
                                pygame.mixer.music.stop()
                                deathCountReal += 1

                        if pygame.sprite.spritecollide(self, lavabig_group, False):
                                randomNumber = random.randint(1,7)
                                #randomNumber2 = random.randint(0,3)
                                setDeathMessage()
                                #print(randomNumber)
                                game_over = -1
                                playDeath()
                                pygame.mixer.music.stop()
                                deathCountReal += 1
                                
                        if pygame.sprite.spritecollide(self, exit_group, False):
                                game_over = 1
                                if level > 14:
                                    tada_sfx.play()
                                else:
                                    star_sfx.play()
                               
                                
                
                #Set ground limit
                        self.rect.x += dx
                        self.rect.y += dy                

                elif game_over == -1:
                        self.image = self.dead_pic

                
                
                #render character
                screen.blit(self.image, self.rect)

                if shouldDrawGrid == True:                                                                                                                        #--Draw hitbox on player \/\/\/\/\/
                    pygame.draw.rect(screen, (255,255,255), self.rect, 2)

                return game_over


        def reset(self, x, y):
                self.images_right = []
                self.images_left = []
                self.index = 0
                self.counter = 0
                global activeskin
                        
                
                for num in range(1, 21):
                        char_right = pygame.image.load(f'skins/{activeskin}/r{num}.png')
                        char_right = pygame.transform.scale(char_right, (40, 49))
                        char_left = pygame.transform.flip(char_right, True, False)
                        self.images_right.append(char_right)
                        self.images_left.append(char_left)

                self.dead_pic = pygame.image.load(f'skins/{activeskin}/dead.png')
                self.image = self.images_right[self.index]
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.width = self.image.get_width()
                self.height = self.image.get_height()
                self.vel_y = 0
                self.jumped = False
                self.direction = 0
                self.isairborne = True
                self.jumpcount = 0
                        
class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		txt_dirt = pygame.image.load('textures/dirttxt.png')
		txt_grass = pygame.image.load('textures/grasstxt.png')
		txt_grass_r = pygame.image.load('textures/grass_r_edge_txt.png')
		txt_water = pygame.image.load('textures/watertxt.png')
		txt_crate = pygame.image.load('textures/cratetxt.png')
		txt_r_edge = pygame.image.load('textures/dirt_r_edge_txt.png')
		txt_float_l = pygame.image.load('textures/float_l_grass.png')
		txt_float_c = pygame.image.load('textures/float_c_grass.png')
		txt_float_r = pygame.image.load('textures/float_r_grass.png')
		invis_barrier = pygame.image.load('textures/barrier.png')
		txt_star = pygame.image.load('textures/startxt.png')
		txt_bush = pygame.image.load('textures/sbush.png')
		txt_stone = pygame.image.load('textures/stoneflat.png')
		txt_rocket = pygame.image.load('textures/stoneflat.png')
                
		
#Map Textures
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
                                #Dirt                                
				if tile == 1:
					img = pygame.transform.scale(txt_dirt, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
                                #Grass
				if tile == 2:
					img = pygame.transform.scale(txt_grass, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
                                #Grass (Right Edge)
				if tile == 3:
					img = pygame.transform.scale(txt_grass_r, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
                                #Water (Can collide)
				if tile == 4:
					img = pygame.transform.scale(txt_water, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
                                #Crate
				if tile == 5:
					img = pygame.transform.scale(txt_crate, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
                                #Dirt Right Side Breakoff
				if tile == 6:
					img = pygame.transform.scale(txt_r_edge, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
                                #Floating Land (Left)
				if tile == 7:
					img = pygame.transform.scale(txt_float_l, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
                                #Floating Land (Center)
				if tile == 8:
					img = pygame.transform.scale(txt_float_c, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
                                #Floating Land (Right)
				if tile == 9:
					img = pygame.transform.scale(txt_float_r, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
                                #Bush (Can collide)
				if tile == 10:
					img = pygame.transform.scale(txt_bush, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
                                #Enemy (Moves 1 block left and right)
				if tile == 11:
					leaf = Enemy(col_count * tile_size, row_count * tile_size)
					leaf_group.add(leaf)
                                #Lava
				if tile == 12:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
                                #Invisible Barrier
				if tile == 13:
					img = pygame.transform.scale(invis_barrier, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
                                #Lava (Full size cube)
				if tile == 14:
					lavabig = Lavabig(col_count * tile_size, row_count * tile_size)
					lavabig_group.add(lavabig)
                                #Finish Line
				if tile == 15:
					exit = Exit(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					exit_group.add(exit)
					
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])
                        #                                                                                                                       -Draw Grid on World
			#pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy/leaf.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1 
        

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('textures/lava.png')
        self.image = pygame.transform.scale(image, (tile_size, tile_size // 2)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Lavabig(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('textures/olava.png')
        self.image = pygame.transform.scale(image, (tile_size, tile_size)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('textures/startxt.png')
        self.image = pygame.transform.scale(image, (tile_size, tile_size // 2)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#Grid = 16x16


player = Player(100, HEIGHT - 195)


#Groups                                                                                                                                         --Groups
leaf_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
lavabig_group = pygame.sprite.Group()
noclip_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#Load Level Data/Create Level


world_data = world_1

world = World(world_data)


## UI Buttons
restart_button = UI(WIDTH // 2 - 50, HEIGHT // 2 + 100, restart_img)


exit_button = UI(WIDTH // 2 - 200, HEIGHT // 2, exit_btn)              #
start_button = UI(WIDTH // 2 - 110, HEIGHT // 2, start_btn)            #
closet_button = UI(WIDTH // 2 - 20, HEIGHT // 2, closet_btn)           #
level_edit_button = UI(WIDTH // 2 + 70, HEIGHT // 2, level_edit_img)   #
playcustom_button = UI(WIDTH // 2 + 160, HEIGHT // 2, playcustom_btn)  #

shop_bg = UI(WIDTH // 2 - 150, HEIGHT // 2 + 150, shopbg)
clear_button = UI(WIDTH // 2 - 350, HEIGHT // 2 - 350, clear_btn)


#UI shop icons

purplePrevImg = UI(WIDTH // 2 + 10 , HEIGHT // 2 + 100, purplePrev)
greenPrevImg = UI(WIDTH // 2 - 70 , HEIGHT // 2 + 100, greenPrev)
cyanPrevImg = UI(WIDTH // 2 - 150 , HEIGHT // 2 + 100, cyanPrev)
redPrevImg = UI(WIDTH // 2 + 90 , HEIGHT // 2 + 100, redPrev)
blackPrevImg = UI(WIDTH // 2 - 150 , HEIGHT // 2 + 200, blackPrev)
pinkPrevImg = UI(WIDTH // 2 - 70 , HEIGHT // 2 + 200, pinkPrev)
bluePrevImg = UI(WIDTH // 2 - 70 , HEIGHT // 2 + 200, bluePrev)
copPrevImg = UI(WIDTH // 2 + 10 , HEIGHT // 2 + 200, copPrev)
goldPrevImg = UI(WIDTH // 2 + 90 , HEIGHT // 2 + 200, goldPrev)



#Different select marks changed for position of previews
selectedPurple = UI(WIDTH // 2 + 10 , HEIGHT // 2 + 150, equippedico)
selectedGreen = UI(WIDTH // 2 - 70 , HEIGHT // 2 + 150, equippedico)
selectedCyan = UI(WIDTH // 2 - 150 , HEIGHT // 2 + 150, equippedico)
selectedRed = UI(WIDTH // 2 + 90 , HEIGHT // 2 + 150, equippedico)
selectedBlack = UI(WIDTH // 2 - 150 , HEIGHT // 2 + 250, equippedico)
selectedBlue = UI(WIDTH // 2 - 70 , HEIGHT // 2 + 250, equippedico)
selectedCop = UI(WIDTH // 2 + 10 , HEIGHT // 2 + 250, equippedico)
selectedGold = UI(WIDTH // 2 + 90 , HEIGHT // 2 + 250, equippedico)

lockedCyan = UI(WIDTH // 2 - 130, HEIGHT // 2 + 110, lockedico)
lockedGreen = UI(WIDTH // 2 - 50 , HEIGHT // 2 + 110, lockedico)

lockedblack = UI(WIDTH // 2 - 130, HEIGHT // 2 + 140, lockedico)
lockedPink = UI(WIDTH // 2 - 130, HEIGHT // 2 + 140, lockedico)


lockedPurple = UI(WIDTH // 2 + 30, HEIGHT // 2 + 110, lockedico)
lockedBlack = UI(WIDTH // 2 - 130 , HEIGHT // 2 + 210, lockedico)
lockedRed = UI(WIDTH // 2 + 110 , HEIGHT // 2 + 110, lockedico)
lockedBlue = UI(WIDTH // 2 - 50 , HEIGHT // 2 + 210, lockedico)
lockedCop = UI(WIDTH // 2 + 30, HEIGHT // 2 + 210, lockedico)
lockedGold = UI(WIDTH // 2 + 110, HEIGHT // 2 + 210, lockedico)



pricePurple = UI(WIDTH // 2 + 30, HEIGHT // 2 + 160, price500ico)
priceGreen = UI(WIDTH // 2 - 50, HEIGHT // 2 + 160, price1500ico)
priceRed = UI(WIDTH // 2 + 110, HEIGHT // 2 + 160, price3000ico)
priceBlack = UI(WIDTH // 2 - 130 , HEIGHT // 2 + 260, price3000ico)
priceBlue = UI(WIDTH // 2 - 50 , HEIGHT // 2 + 260, price10000ico)
priceCop = UI(WIDTH // 2 + 30 , HEIGHT // 2 + 260, price10000ico)
priceGold = UI(WIDTH // 2 + 110 , HEIGHT // 2 + 260, icon60s)


givePoints = True
overridePoints = str(pointsSave)

isFullscreen = False

musicIsMuted = False

#Run Game                                                                                                                               -- Run Game  

running = True
while running:
    #Set FPS
    clock.tick(FPS)                                                                                                    # ------------------------------ Tick

    #Create background
    screen.blit(background1, (0, 0))

    

    
# IF TITLE SCREEN IS ACTIVE --------------------------------------------------------------------------                           --Check for Title Screen    
    if title_screen == True:
        key = pygame.key.get_pressed()
        draw_text('Super Sussy Boy Part II (Enhanced Edition)', font_title, BLACK, WIDTH//2 - 358, HEIGHT // 2 - 78)
        draw_text('Super Sussy Boy Part II (Enhanced Edition)', font_title, WHITE, WIDTH//2 - 360, HEIGHT // 2 - 80)
        draw_text('[A/D] Move', font_hint, BLACK, WIDTH//2 - 350, 110)
        draw_text('[SPACE] Jump/Double Jump', font_hint, BLACK, WIDTH//2 - 350, 130)
        draw_text('[M] Music', font_hint, BLACK, WIDTH//2 - 350, 150)
        draw_text('[K] kys', font_hint, BLACK, WIDTH//2 - 350, 170)
        draw_text('Best Run:', font_level, BLACK, WIDTH//2 + 200, 65)
        draw_text('Best Run:', font_level, WHITE, WIDTH//2 + 198, 67)
        draw_text('Time: ' + str(bestRealMins) + ':' + str(bestMins)[0:2] + '.' + str(bestSec), font_hint, BLACK, WIDTH//2 + 200, 100)
        

        draw_text("Exit", font_small, GREY, exit_button.rect.x + 22, exit_button.rect.y + exit_button.rect.height + 5)
        draw_text("Start", font_small, GREY, start_button.rect.x + 17, start_button.rect.y + start_button.rect.height + 5)
        draw_text("Closet", font_small, GREY, closet_button.rect.x + 11, closet_button.rect.y + closet_button.rect.height + 5)
        draw_text("Editor", font_small, GREY, level_edit_button.rect.x + 15, level_edit_button.rect.y + level_edit_button.rect.height + 5)
        draw_text("Play Custom", font_small, GREY, playcustom_button.rect.x - 10, playcustom_button.rect.y + playcustom_button.rect.height + 5)
        
        
        if bestDeaths == 999:
            draw_text('Deaths: -', font_hint, BLACK, WIDTH//2 + 200, 120)
        else:
            draw_text('Deaths: ' + str(bestDeaths), font_hint, BLACK, WIDTH//2 + 200, 120)
        
        # if key[pygame.K_F11]:
        #     if isFullscreen != True:
        #         pygame.display.toggle_fullscreen()
        #         isFullscreen = True
        #         time.sleep(.5)
        #     else:
        #         pygame.display.toggle_fullscreen()
        #         isFullscreen = False
                # time.sleep(.5)

        if key[pygame.K_m]:
            if musicIsMuted == False:
                pygame.mixer.music.stop()
                musicIsMuted = True
                time.sleep(.5)
            else:
                pygame.mixer.music.play()
                musicIsMuted = False
                time.sleep(.5)
            
        if exit_button.draw():
            pygame.mixer.music.set_volume(0.0)
            click_sfx.play()
            time.sleep(0.2)
            running = False
            print("SSB2 has been closed.")
        if start_button.draw():
            givePoints = True
            shouldDrawGrid = False
            click_sfx.play()
            level = 1
            world_data = world_1
            world = reset_level(level)
            game_over = 0
            deathCountReal = 0 
            #reset stopwatch
            milliseconds = 0
            seconds = 0
            minutes = 0
            realmins = 0
            timeInSeconds = 0
            title_screen = False
            
        if clear_button.draw():
                lineData[0] = '0\n'
                lineData[1] = '0\n'
                lineData[2] = '1\n'
                lineData[3] = '0\n'
                lineData[4] = '0\n'
                lineData[5] = '0\n'
                lineData[6] = '0\n'
                lineData[7] = 'cyan\n'
                lineData[9] = '0\n'
                lineData[10] = '0\n'
                lineData[11] = '0\n'
                lineData[13] = '0\n'
                lineData[14] = '0\n'
                lineData[15] = '0\n'
                lineData[16] = '999999\n'
                lineData[17] = '999\n'
                with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                click_sfx.play()
                print("Clearing data...")
                time.sleep(.5)
                pygame.mixer.music.set_volume(0.0)
                err_sfx.play()
                time.sleep(0.1)
                err_sfx.play()
                running = False
                print("Game data cleared. Restart the game.")
                print("SSB2 has been closed.")
                time.sleep(.3)
                        
        if closet_button.draw():
            click_sfx.play()
            if closet_open == False:
                closet_open = True
                #print("closet opened")
            elif closet_open == True:
                closet_open = False
               # print("closet closed")



        if level_edit_button.draw():
            click_sfx.play()
            switch_message = "Launching SSB Level Editor..."
            print("\nOpening LevelEditor - Please Wait...\n")
            # Clear screen and draw background
            screen.blit(background1, (0, 0))
            # Render the message (using a title font for clarity)
            message_surface = font_small.render(switch_message, True, WHITE)
            message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            # Create a semi-transparent overlay with some padding around the text
            overlay = pygame.Surface((message_rect.width + 20, message_rect.height + 20))
            overlay.set_alpha(128)  # 50% opacity
            overlay.fill(BLACK)
            overlay_rect = overlay.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(overlay, overlay_rect.topleft)
            screen.blit(message_surface, message_rect)
            pygame.display.update()
            time.sleep(.4)
            print("Closing SSB2...\n")
            subprocess.Popen(["python3", "leveleditV1.py"])
            pygame.quit()
            sys.exit()
            
       
        if playcustom_button.draw():
            load_custom_level_from_file()
            if customExists:
                print("Loading custom level...")
                print("world_0 data:")
                for row in world_0:
                    print(row)
                givePoints = True
                shouldDrawGrid = False
                click_sfx.play()
                level = 16
                world_data = world_0
                world = reset_level(level)
                game_over = 0
                deathCountReal = 0
                # Reset stopwatch
                milliseconds = 0
                seconds = 0
                minutes = 0
                realmins = 0
                timeInSeconds = 0
                title_screen = False
                playing_custom = True
            else:
                err_sfx.play()
                print("\nERR: No custom level found.")
                print("Made a world but cant play?\n Go to Editor > Show All > [Send]\n")
       
       
       
        ######################  ##SHOP ASSETS## ############################                                                    ----------------SHOP ASSETS
        if closet_open == True:
           shop_bg.draw()
           draw_text('Dough: ' + str(pointsSave), font_titleinfo, BLACK, WIDTH//2 - 140, HEIGHT // 2 + 320)
           if purplePrevImg.draw():                                                                                       #Purple
               if purpleSave == 1:
                   click_sfx.play()
                   lineData[7] = 'purple\n'
                   activeskin = str(lineData[7])[0:len(str(lineData[7])) -1]
                   with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                   #print("Skin set to purple")
           if purpleSave == 0:
               if pricePurple.draw():
                   if pointsSave < 500:
                       err_sfx.play()                      
                       #print("ERR: Not enough dough")
                   elif pointsSave >= 500:
                       pointsSave -= 500
                       purpleSave = 1

                       lineData[0] = str(pointsSave) + "\n"
                       lineData[5] = '1\n'
                       with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                       print("Game Saved")
                       
                       chaching_sfx.play()


                   
           if greenPrevImg.draw():                                                                                      #Green
               if greenSave == 1:
                   click_sfx.play()
                   lineData[7] = 'green\n'
                   activeskin = str(lineData[7])[0:len(str(lineData[7])) -1]
                   with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                   activeskin = str(lineData[7])[0:len(str(lineData[7])) -1]
                   #print("Skin set to green")
                             
           if greenSave == 0:
                   if priceGreen.draw():
                       if pointsSave < 1500:
                           err_sfx.play()
                           #print("ERR: Not enough dough")
                       elif pointsSave >= 1500:
                           pointsSave -= 1500
                           greenSave = 1

                           lineData[0] = str(pointsSave) + "\n"
                           lineData[3] = '1\n'
                           with open('playerstats.txt','w+') as file:
                               file.writelines(lineData)
                           print("Game Saved")
                           
                           chaching_sfx.play()        


                               
           if redPrevImg.draw():                                                                                       #Red
               if redSave == 1:
                   click_sfx.play()
                   lineData[7] = 'red\n'
                   activeskin = str(lineData[7])[0:len(str(lineData[7])) -1]
                   with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                   #print("Skin set to red")
           if redSave == 0:
               if priceRed.draw():
                   if pointsSave < 3000:
                       err_sfx.play()
                       #print("ERR: Not enough dough")
                   elif pointsSave >= 3000:
                       pointsSave -= 3000
                       redSave = 1

                       lineData[0] = str(pointsSave) + "\n"
                       lineData[6] = '1\n'
                       with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                       print("Game Saved")
                       
                       chaching_sfx.play()

           if blackPrevImg.draw():                                                                                       #Black
               if blackSave == 1:
                   click_sfx.play()
                   lineData[7] = 'black\n'
                   activeskin = str(lineData[7])[0:len(str(lineData[7])) -1]
                   with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                   #print("Skin set to black")
           if blackSave == 0:
               if priceBlack.draw():
                   if pointsSave < 3000:
                       err_sfx.play()
                       #print("ERR: Not enough dough")
                   elif pointsSave >= 3000:
                       pointsSave -= 3000
                       blackSave = 1

                       lineData[0] = str(pointsSave) + "\n"
                       lineData[1] = '1\n'
                       with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                       print("Game Saved")
                       
                       chaching_sfx.play()  



           if bluePrevImg.draw():                                                                                       #Blue
               if blueSave == 1:
                   click_sfx.play()
                   lineData[7] = 'blue\n'
                   activeskin = str(lineData[7])[0:len(str(lineData[7])) -1]
                   with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                   #print("Skin set to blue")
           if blueSave == 0:
               if priceBlue.draw():
                   if pointsSave < 10000:
                       err_sfx.play()
                       #print("ERR: Not enough dough")
                   elif pointsSave >= 10000:
                       pointsSave -= 10000
                       blueSave = 1
                       lineData[0] = str(pointsSave) + "\n"
                       lineData[9] = '1\n'
                       with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                       print("Game Saved")
                       
                       chaching_sfx.play()






           if copPrevImg.draw():                                                                                       #Cop
               if copSave == 1:
                   click_sfx.play()
                   lineData[7] = 'cop\n'
                   activeskin = str(lineData[7])[0:len(str(lineData[7])) -1]
                   with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                  #print("Skin set to cop")
           if copSave == 0:
               if priceCop.draw():
                   if pointsSave < 10000:
                       err_sfx.play()
                       #print("ERR: Not enough dough")
                   elif pointsSave >= 10000:
                       pointsSave -= 10000
                       copSave = 1
                       lineData[0] = str(pointsSave) + "\n"
                       lineData[10] = '1\n'
                       with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                       print("Game Saved")
                       
                       chaching_sfx.play()        


           if goldPrevImg.draw():                                                                                       #Cop
               if goldSave == 1:
                   click_sfx.play()
                   lineData[7] = 'gold\n'
                   activeskin = str(lineData[7])[0:len(str(lineData[7])) -1]
                   with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                   #print("Skin set to gold")

           if goldSave == 0:
               if priceGold.draw():
                       err_sfx.play()
                       #print("ERR: Beat the game in under 60 seconds.")




                        
                       
           if cyanPrevImg.draw():                                                                                       #Cyan (Default)
                   click_sfx.play()
                   lineData[7] = 'cyan\n'
                   activeskin = str(lineData[7])[0:len(str(lineData[7])) -1]
                   with open('playerstats.txt','w+') as file:
                           file.writelines(lineData)
                   activeskin = str(lineData[7])[0:len(str(lineData[7])) -1]
                   #print("Skin set to cyan")          

           #Padlock Locked Skins
           if purpleSave == 0:
                lockedPurple.draw()
           if greenSave == 0:
                lockedGreen.draw()
           if redSave == 0:
                lockedRed.draw()
           if blackSave == 0:
                lockedBlack.draw()
           if blueSave == 0:
               lockedBlue.draw()
           if copSave == 0:
               lockedCop.draw()
           if goldSave == 0:
               lockedGold.draw()


           
           #PUT CHECKMARK NEXT TO APPLIED SKIN
           if activeskin == "green":
                   selectedGreen.draw()
           if activeskin == "cyan":
                   selectedCyan.draw()
           if activeskin == "purple":
                   selectedPurple.draw()
           if activeskin == "red":
                   selectedRed.draw()
           if activeskin == "black":
                   selectedBlack.draw()
           if activeskin == "blue":
                   selectedBlue.draw()
           if activeskin == "cop":
                   selectedCop.draw()
           if activeskin == "gold":
                   selectedGold.draw()
               
        
        

    else:                
        world.draw()
        #                                                                                                                               --Draw Collision boxes
        if shouldDrawGrid == True:
            draw_grid()

        if level <= max_levels: 
            milliseconds = pygame.time.get_ticks()
            if milliseconds > 1000:
                seconds += 1
                fire_time =- 1000
            if seconds > 59:
                minutes += 1
                seconds -= 60
                timeInSeconds += 1
            if minutes > 59:
                realmins += 1
                minutes -= 60
            
            
        if game_over == 0:

            leaf_group.update()
            draw_text('Level: ' + str(level), font_level, WHITE, tile_size - 10, 15)
            #draw_text('[SPACE] Jump/Double Jump', font_hint, WHITE, 300, 20)
            #draw_text('[A][D] Move', font_hint, WHITE, 200, 20)
            #draw_text('Get the cake!', font_hint, CYAN,550, 20)
            draw_text(str(realmins) + ':' + str(minutes) + '.' + str(seconds), font_hint, WHITE,150,25)

              
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.set_volume(0.0)
                err_sfx.play()
                time.sleep(0.3)
                running = False
                print("SSB2 has been closed.")

        
        leaf_group.draw(screen)
        lava_group.draw(screen)
        lavabig_group.draw(screen)
        exit_group.draw(screen)
        noclip_group.draw(screen)

        
        game_over = player.update(game_over) 

        
        #if player has died
        if game_over == -1:
            key = pygame.key.get_pressed()                
            draw_text('[R]', font_titleinfo, WHITE, WIDTH//2 - 25, HEIGHT // 2 + 190)
            draw_text(deathMessage, font_win_big, BLACK, WIDTH//2 - 100, HEIGHT // 2)
            draw_text('Press [P] to return to main menu', font_hint, WHITE, WIDTH//2 - 125, HEIGHT // 2 + 215)
            if restart_button.draw():
                click_sfx.play()
                player.reset(100, HEIGHT - 130)
                game_over = 0
                if musicIsMuted == False:
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.stop()
            if key[pygame.K_r]:
                player.reset(100, HEIGHT - 130)
                game_over = 0
                if musicIsMuted == False:
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.stop()
            if key[pygame.K_p]:
                title_screen = True
                closet_open = False
                if musicIsMuted == False:
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.stop()

        #if player beats level                                                                                                          --Switch Levels
        if game_over == 1:
                level += 1
                if level <= max_levels:
                        if world_data == world_1:
                                world_data = world_2
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_2:
                                world_data = world_3
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_3:
                                world_data = world_4
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_4:
                                world_data = world_5
                                shouldDrawGrid = True
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_5:
                                shouldDrawGrid = False
                                world_data = world_6
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_6:
                                world_data = world_7
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_7:
                                world_data = world_8
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_8:
                                world_data = world_9
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_9:
                                world_data = world_10
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_10:
                                world_data = world_11
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_11:
                                world_data = world_12
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_12:
                                world_data = world_13
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_13:
                                world_data = world_14
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_14:
                                world_data = world_15
                                world = reset_level(level)
                                game_over = 0
                        elif world_data == world_0:             #For imported custom levels
                                world_data = world_0
                                world = reset_level(level)
                                game_over = 0  
                                playing_custom = True              
                else:                                       #if player has beaten the game
                        #Award Points
                        if givePoints == True:
                            if playing_custom == False:
                                pointsGiven = 0
                                if timeInSeconds < 60:
                                    pointsGiven = 6000
                                    goldSave = 1
                                elif timeInSeconds < 120:
                                    pointsGiven = 2500
                                elif timeInSeconds < 180:
                                    pointsGiven = 1500
                                else:
                                    pointsGiven = 800
                            else:
                                  pointsGiven = 200         ##Custom levels give 200 points


                            if deathCountReal == 0:
                                if playing_custom == False:
                                    pointsGiven += 2500
                                #print("+500 No death bonus applied!")

                            pointsSave = int(pointsSave) + pointsGiven 
                            
                            #print("Modified points save: " + str(pointsSave))


                            if timeInSeconds < bestTime:
                                if not playing_custom:
                                    bestRealMins = realmins
                                    bestMins = minutes
                                    bestSec = seconds
                                    if deathCountReal < bestDeaths:
                                        bestDeaths = deathCountReal

                                    lineData[13] = str(bestRealMins) + "\n"
                                    lineData[14] = str(bestMins) + "\n"
                                    lineData[15] = str(bestSec) + "\n"
                                    lineData[16] = str(timeInSeconds) + "\n"
                                    lineData[17] = str(bestDeaths) + "\n"
                                    print("New Best!")
                                    with open('playerstats.txt','w+') as file:
                                        file.writelines(lineData)
                                    
                                lineData[0] = str(pointsSave) + "\n"
                                lineData[11] = str(goldSave) + "\n"
                                with open('playerstats.txt','w+') as file:
                                    file.writelines(lineData)
                                print("Game Saved")
                                givePoints = False

                            
                        key = pygame.key.get_pressed() 
                        draw_text('Nice.', font_win_big, BLACK, WIDTH//2 - 78, HEIGHT // 2 - 75)
                        draw_text('Deaths: ' + str(deathCountReal)  , font_hint, WHITE, WIDTH//2 - 200, HEIGHT // 2 - 40)
                        draw_text('Time: ' + str(realmins) + ':' + str(minutes) + '.' + str(seconds), font_hint, WHITE, WIDTH//2 - 80, HEIGHT // 2 - 40)

                        if playing_custom == False:
                            if deathCountReal == 0:
                                draw_text('Dough: +' + str(pointsGiven) + " (+2500 No Death Bonus)", font_hint, WHITE, WIDTH//2 + 50, HEIGHT // 2 - 40)
                            else:
                                draw_text('Dough: +' + str(pointsGiven), font_hint, WHITE, WIDTH//2 + 50, HEIGHT // 2 - 40)
                        else:
                            draw_text('Dough: +' + str(pointsGiven), font_hint, WHITE, WIDTH//2 + 50, HEIGHT // 2 - 40)
                            
                        draw_text('Press [P] to return to main menu', font_hint, WHITE, WIDTH//2 - 125, HEIGHT // 2 + 215)
                        if restart_button.draw():
                                if playing_custom:
                                    click_sfx.play()
                                    closet_open = False
                                    title_screen = True
                                    playing_custom = False
                                else:
                                    level = 1
                                    world_data = world_1
                                    givePoints = True
                                world = reset_level(level)
                                game_over = 0
                                #reset stopwatch
                                milliseconds = 0
                                seconds = 0
                                minutes = 0
                                realmins = 0
                                timeInSeconds = 0
                                deathCountReal = 0
                                
                        if exit_button.draw():
                                pygame.mixer.music.set_volume(0.0)
                                click_sfx.play()
                                print("SSB2 has been closed.")
                                running = False
                        if key[pygame.K_p]:
                                closet_open = False
                                title_screen = True
                                playing_custom = False
                                
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.set_volume(0.0)
            err_sfx.play()
            time.sleep(0.2)
            print("SSB2 has been closed.")
            running = False
            
            
        
