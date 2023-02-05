import subprocess
import pygame as pg
import sys
import os

""" This is a GUI to run as the "OS" for the game console

    It will display 3 game options that the user can click on to then play
    the selected game. Once the game has ended, this application will run
    again. There will also be a restart and power off button, as well
    as a sleep button to listen for any controller input to wake up.

    Noah Chaney
    February 4, 2023
"""

# pygame initializations 
pg.init()
# pg.joystick.init()

# creating the canvas to run the app
canvas = pg.display.set_mode([0, 0], pg.FULLSCREEN)

def open_py_file(app):
    # specify game path
    application = '/home/pi/Desktop/console_system/games/{}/{}.py'.format(app, app)

    # system command to run the game
    cmd = 'python {}'.format(application)

    # calls the terminal command
    p = subprocess.Popen(cmd, shell=True)
    p.communicate()


# this function will return a dictionary of the game settings and files
""" Settings in order and format

    name Game_Name
    thumb_nail /image/path.jpg
    creator First_Last
    date_released MM_DD_YYYY
""" 
def get_settings(game):
    game_settings = {}
    # file = ""
    f = open("/home/pi/Desktop/console_system/games/{}/settings.txt", 'r')
    for line in f:
        setting = line.split(' ')
        game_settings[setting[0]] = setting[1]
    return game_settings


class Panel:
    def __init__(self, game, pos):
        self.size = canvas.get_width()/3.5
        self.pos = ''
        BUFFER = 250
        VBUFFER = (canvas.get_height() - self.size)/2 - 100
        match pos:
            case 'l':
                self.pos = (canvas.get_width()/2 - self.size - BUFFER, canvas.get_height()/2 - VBUFFER)
            case 'm':
                self.pos = (canvas.get_width()/2, canvas.get_height()/2 - VBUFFER)
            case 'r':
                self.pos = (canvas.get_width()/2 + BUFFER, canvas.get_height()/2 - VBUFFER)

       
        settings = get_settings(game)
        self.image = pg.image.load('{}'.format(settings['image']))
        self.image = pg.transform.scale(image, (self.size, self.size))

        font = pg.font.Font(None, 20)
        name = settings['name']
        for letter in name:
            if letter == '_':
                name = name.remove(letter) 
        self.text = font.render('{}'.format(name), True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.pos[0], self.pos[1] + 0.5*self.size + 50)
    
    def update():
        canvas.blit(self.image, (self.pos[0], self.pos[1]))
        canvas.blit(self.text, self.text_rect())

        
games = []      
for root, dirs, files in os.walk('console_system/games/'):
    games.append(dirs)

    
def draw_games():
    i = 0
    poss = ['l', 'm', 'r']
    for game in games:
        print(game)
        new_game = Panel(game, poss[i])
        new_game.update()
        i += 1
        if i == 3:
            i = 0

    
def main():
    
    exit = False
    while not exit:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                exit = True
        canvas.fill((100, 100, 235))
        draw_games()

        pg.display.update()
            
    

if __name__ == "__main__":
    main()

