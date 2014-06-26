import random, math

import kivy
kivy.require('1.7.2')
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.graphics.context_instructions import Rotate, PushMatrix, PopMatrix

from kivy.properties import NumericProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.uix.progressbar import ProgressBar

import kivy.utils

PATH = "./media/"
if kivy.utils.platform == "win":
    PATH = r".\media\\"

import kivy.metrics
import kivy.core.window

__version__ = '1.0'
#print kivy.metrics.Metrics.density
#print kivy.metrics.Metrics.dpi
SCREEN_DENSITY = kivy.metrics.Metrics.density + 0.0
SCREEN_WIDTH = kivy.metrics.dp(Window.size[0]) / kivy.metrics.Metrics.density
SCREEN_HEIGHT = kivy.metrics.dp(Window.size[1]) / kivy.metrics.Metrics.density
Y_BLOCK = SCREEN_HEIGHT / 6
X_BLOCK = SCREEN_WIDTH / 8
SCREEN_RATIO = (SCREEN_WIDTH + 0.0) / (SCREEN_HEIGHT + 0.0)

print "SCREEN_DENSITY: %f\nSCREEN_WIDTH: %f\nSCREEN_HEIGHT: %f\nSCREEN_RATIO: %f\nX_BLOCK: %f: Y_BLOCK: %f" %\
       (SCREEN_DENSITY,SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_RATIO,X_BLOCK,Y_BLOCK)

from kivy.lang import Builder
Builder.load_string('''
<MyImage>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0, 0, 1
            origin: root.center
        Color: 
            rgba: (0,0,0, root.shadow_opacity)
        Rectangle: 
            source: self.source
            size: (self.size[0], self.size[1])
            pos: (self.pos[0]+7, self.pos[1])
        Color: 
            rgba: (.9,.1,.1, root.highlight_opacity)
        Rectangle: 
            source: self.source
            size: (self.size[0]+2, self.size[1]+2)
            pos: (self.pos[0]-1, self.pos[1]-1)
        
    canvas.after:
        PopMatrix
    Label:
        font_size: self.parent.font_size
        y: root.center_y + root.label_deltay
        x: root.center_x + root.label_deltax
        size: min(self.size)*0.1, min(self.size)*0.1
        markup: True
''')


class MyImage(Image):
    angle = NumericProperty()
    is_flashable = NumericProperty(1)
    score = 0
    label_deltax = NumericProperty(-5)
    label_deltay = NumericProperty(-5)
    shadow_opacity = NumericProperty(0.8)
    highlight_opacity = NumericProperty(0)
    font_size = NumericProperty(15)
    
    def set_shadow(self, shadow_on):
        if shadow_on:
            self.shadow_opacity = 0.8
        else:
            self.shadow_opacity = 0

    def set_highlight(self, highlight_on):
        if highlight_on and self.is_flashable == 1:
            self.highlight_opacity = 0.8
        else:
            self.highlight_opacity = 0
            
    def stop_flash(self):
        self.is_flashable = 0
    
    def flash(self, times):
        self.flash_index = 0
        for i in range(times):
            Clock.schedule_once(lambda dt: self.set_highlight(True), 0.4 * i)
            Clock.schedule_once(lambda dt: self.set_highlight(False), 0.2 + 0.4 * i)
    
    def set_label_position(self, deltax, deltay):
        self.label_deltax = deltax
        self.label_deltay = deltay
    
    def set_font_size(self, size):
        self.children[0].font_size = size
    
    def set_score(self, score):
        self.score = score
        self.children[0].text = "[color=000000]"+str(score)+"[/color]"
    
    def celebrate(self, speed, times):
        self.do_jump = True
        self.do_walk = True
        self.move(speed, times)
    
    def jump(self,speed, times):
        self.do_jump = True
        self.do_walk = False
        self.move(speed, times)

    def walk(self,speed, times):
        self.do_jump = False
        self.do_walk = True
        self.hero_direction = -6
        self.move(speed, times)

    def move(self, speed, times):
        self.index = 0
        self.times = times
        self.direction = 1
        Clock.schedule_interval(self._move, 1.0 / speed)
        
    def look_alive(self, dt=None):
        action = random.choice([0,0,1,2,3])
        if action == 1:
            self.move(60, 12)
        elif action == 2:
            self.walk(60, 12)
        elif action == 3:
            self.jump(60, 12)
        
    def _move(self, dt=None):
        self.index = self.index + 1
        if self.index > self.times:
            Clock.unschedule(self._move)
        else:
            if self.do_walk:
                self.angle = self.index % 6
            if self.do_jump:
                self.y = self.y + self.direction
            if self.index % 6 == 0:
                self.direction = - self.direction      

Builder.load_string('''
<MyButton>:
    Image:
        source: self.parent.source
        y: self.parent.y
        x: self.parent.x
        width: self.parent.width
        height: self.parent.height
        allow_stretch: True
    Label:
        text: self.parent.label_text
        font_size: self.parent.font_size
        y: self.parent.y - 25
        x: self.parent.x + self.parent.width / 10.0
''')

class MyButton(Button):
    score = NumericProperty(0)
    source = StringProperty()
    label_text = StringProperty()
    font_size = NumericProperty(15)
    screen_ratio = NumericProperty(SCREEN_RATIO)
    screen_density = NumericProperty(SCREEN_DENSITY)
                
class MySound():
    def __init__(self, core_sound):
        self.core_sound = core_sound
        
    def play(self, dt=None):
        self.core_sound.play()

def get_state():
    text = open(PATH+"state.txt", "rb").read()
    return text

def save_state(level):
    f = open(PATH+"state.txt", "wb")
    f.write(str(level))
    f.close()

def get_level_data(level_number):
    text = open(PATH+"levels.txt", "rb").read()
    lines = text.split("\n")
    level_data = lines[level_number+1].replace(" ","").split("|")
    return level_data

class GameView(ScreenManager):
    def __init__ (self, app):
        super(GameView, self).__init__(transition=WipeTransition())
        self.app = app
        self.graphics_widget = FloatLayout()
        image = Image(source = PATH + "splash.png", keep_ratio=False, allow_stretch=True,\
               size=(SCREEN_WIDTH, SCREEN_HEIGHT), size_hint=(None, None), pos=(0,0))
        self.graphics_widget.add_widget(image)
        screen = Screen(name="0")
        screen.add_widget(self.graphics_widget)
        self.add_widget(screen)
        self.current = "0"
        #
        self.load_sounds()
        self.load_textures()
        #self.load_sprites()
        self.load_gems()
        #
        self.schedules = []
        self.image_hero = None
        #
        self.image_score = MyImage(source = PATH + "score_bg.png", allow_stretch=True)
        self.image_score.set_score(0)
        self.image_score.set_shadow(False)
        self.image_score.set_font_size(30)
        self.image_score.set_label_position(3,4)        
        self.image_score.size_hint = (.2, .2)
        self.image_score.pos_hint = {'x':.8, 'y':.8}
        #
        self.button_reset = MyButton(source=PATH + "restart.png", on_press=self.reset, opacity=0.5,\
                       background_color = (0,0,0,0), size = (X_BLOCK, Y_BLOCK), border=(0,0,0,0))
        self.button_reset.size_hint = (.1, .1)
        self.button_reset.pos_hint = {'x': 0, 'y':.9}
        
        self.progress_bar = ProgressBar(max=500, opacity=0) #CURRENTLY HIDDEN
        with self.progress_bar.canvas:
            Color(0,0,0,0)
        self.progress_bar.size_hint = (.6, .05)
        self.progress_bar.pos_hint = {'x': 0.2, 'y': 0}
        self.progress_bar.value = 0

        self.schedule(self.reset_level, 3)
        
    def unschedule_all(self):
        for s in self.schedules:
            Clock.unschedule(s)
        self.schedules = []       

    def unschedule_single(self, dt=None):
        self.schedules = self.schedules[1:]

    def schedule(self, func, delay):
        if func not in self.schedules:
            self.schedules.append(func)
        Clock.schedule_once(func, delay)
        Clock.schedule_once(self.unschedule_single, delay)

    def reset(self, widget=None):
        print "Reset"
        #save_state(1)
        #self.reset_level()
        self.level = 1
        save_state(1)
        self.app.stop()

    def reset_level(self, dt=None):
        self.level = int(get_state())
        try:
            Animation.cancel_all(self.scatter_hero)
        except:
            pass
        try:
            Animation.cancel_all(self.scatter_baddy)
        except:
            pass
        Animation.cancel_all(self.progress_bar)
        self.unschedule_all()
        self.setup_battle()
        
    def get_level_data(self):
        data = get_level_data(self.level)
        self.baddy_points_for_level = int(data[0])
        self.weapons = [int(x) for x in data[1].split(",")]
        self.score_threshold = int(data[2])
        self.maximum_attacks = int(data[3])
        self.time_limit = int(data[4])
        self.baddy_image = data[5]
        self.baddy_ratio_for_level = int(data[6])
        self.baddy_label_deltax = int(data[7])
        self.baddy_label_deltay = int(data[8])
        self.level_potions = [int(x) for x in data[9].split(",") if x]
        self.textures_data = data[10].split(";")
        #self.sprites_data = data[11].split(";")
        #if self.sprites_data == ['']:
        #    self.sprites_data = []
        
    def setup_battle(self, dt=None):
        self.graphics_widget.remove_widget(self.button_reset)
        self.graphics_widget.remove_widget(self.image_score)
        self.graphics_widget.remove_widget(self.progress_bar)
        if self.level == 11:
            graphics_widget = FloatLayout()
            image = Image(source = PATH + "end.png", keep_ratio=False, allow_stretch=True,\
               size=(SCREEN_WIDTH, SCREEN_HEIGHT), size_hint=(None, None), pos=(0,0))
            graphics_widget.add_widget(image)
            graphics_widget.add_widget(self.button_reset)
            screen = Screen(name="end")
            screen.add_widget(graphics_widget)
            self.add_widget(screen)
            self.current=screen.name
        else:
            self.get_level_data()

            graphics_widget = self.set_background()
            screen = Screen(name=str(self.level))
            screen.add_widget(graphics_widget)
            self.graphics_widget = graphics_widget
            self.add_widget(screen)
            self.current=screen.name
            if self.score_threshold > 0:
                self.level_score = - self.score_threshold
            else:
                self.level_score = 0
            self.image_score.set_score(self.level_score)
            if self.level < 3:
                self.start_battle()
            else:
                self.schedule(self.start_battle, 0) #WAS 2
            self.graphics_widget.add_widget(self.button_reset)
            self.graphics_widget.add_widget(self.progress_bar)
            self.graphics_widget.add_widget(self.image_score)
        
    def repeat_battle(self, dt=None):
        self.image_hero = None
        self.level_score = 0
        self.image_score.set_score(self.level_score)
        self.start_battle()

    def start_battle(self, dt=None):
        self.attacks_tried = 0
        self._picked_gems = []
        if self.level_potions:
            self.create_potions(self.level_potions)
        else:
            self.potion_buttons = []
        self.create_gems(self.weapons)
        #
        min_wait = 0 #WAS 3
        if self.level < 3:
            min_wait = 0
        self.schedule(self.introduce_hero, min_wait)
        if self.level == 1:
            self.schedule(self.introduce_baddy, min_wait)
        else:
            self.schedule(self.introduce_baddy, min_wait + 2)
        self.schedule(self.talk_baddy, min_wait + 4)
        self.schedule(self.talk_hero, min_wait + 5.5)
        self.schedule(self.talk_baddy, min_wait + 6.5)
        if self.level == 1:
            self.schedule(self.show_gems, 0)
        else:
            self.schedule(self.show_gems, min_wait + 8)
        if self.score_threshold > 0:
            self.image_score.flash(10)
        self.schedule(self.show_potions, min_wait + 8)
        self.schedule(self.look_alive, min_wait + 8)
        self.schedule(self.handle_timed_battle, min_wait + 8)
        if self.level == 1:
            self.schedule(self.flash_gem, min_wait + 11)
            #self.schedule(self.flash_hero, min_wait + 15)
        
    def flash_gem(self, dt=None):
        for g in self.gems:
            if g:
                g.flash(10)

    def flash_hero(self, widget=None, event=None):
        self.image_hero.flash(10)
        
    def handle_timed_battle(self, dt=None):
        if self.time_limit > 0:
            anim1 = Animation(x = X_BLOCK, duration=self.time_limit)
            anim1.bind(on_complete = self.level_failed)
            anim1.start(self.scatter_baddy)
            self.progress_bar.value = self.progress_bar.max
            anim2 = Animation(value = 0, duration=self.time_limit)
            anim2.start(self.progress_bar)
            
    def create_gems(self, numbers):
        self.gems = [None] * 10
        self.gem_values = [0] * 10
        for i in range(len(numbers)):
            n = numbers[i]
            #gem = MyImage(keep_ratio=True, allow_stretch=False, color=(0,0,0,0), keep_data=True)
            #gem.set_shadow(False)
            #with gem.canvas:
            #    gem.rectangle = Rectangle(texture=self.gem_sprites[n].texture, size = (X_BLOCK,Y_BLOCK))
            gem = MyImage(source = self.gem_sources[n],keep_ratio=False, allow_stretch=True, keep_data=True)
            gem.set_shadow(False)
            self.gems[n] = gem
            self.gem_values[n] = n
            
    def drop_gem(self, widget=None, event=None):
        if widget not in self.graphics_widget.children:
            return True

        if widget.x > self.scatter_hero.x and widget.x < self.scatter_hero.x + self.image_hero.width * 2:
            if widget.y > self.scatter_hero.y and widget.y < self.scatter_hero.y + self.image_hero.height * 2:
                self.image_hero.stop_flash()
                self.handle_player_action(widget)
                return True
            else:
                self.hide_gems()
                self.show_gems()
                self.hide_potions()
                self.show_potions()
        else:
            self.hide_gems()
            self.show_gems()
            self.hide_potions()
            self.show_potions()
        return False
        
    def pick_gem(self, widget=None, event=None):
        self._picked_gems.append(widget)
        self.flash_hero()

    def hide_gems(self, dt=None, dummy=None):
        for scatter in self.gem_scatters:
            if scatter.children:
                scatter.remove_widget(scatter.children[-1])
            self.graphics_widget.remove_widget(scatter)
    
    def show_gems(self, dt=None, dummy=None):
        self.gem_scatters = []
        filler = (8 - len(self.weapons)) / 2.0
        for i in range(len(self.weapons)):
            gem = self.gems[self.weapons[i]]
            scatter = Scatter(do_rotation=False, do_scale=False, color=(0,0,0,0), size_hint=(0.1,0.1))
            scatter.add_widget(gem)
            gem.bind(on_touch_down=self.flash_hero)            
            scatter.bind(on_touch_up=self.drop_gem)
            scatter.pos = ((filler + i) * X_BLOCK, 0)
            scatter.scale = 1
            try:
                self.graphics_widget.add_widget(scatter)
                self.gem_scatters.append(scatter)
            except:
                pass

    def bring_to_front(self, widget):
        self.graphics_widget.remove_widget(widget)        
        self.graphics_widget.add_widget(widget)        
        
    def set_background(self):
        graphics_widget = FloatLayout()

        for td in self.textures_data:
            filename,xpos,ypos,width,height = td.split(":")
            xpos = float(xpos)
            ypos = float(ypos)
            image = MyImage(keep_ratio=True, allow_stretch=False, color=(0,0,0,0))
            image.set_shadow(False)
            with image.canvas:
                Rectangle(texture=self.textures[filename].texture, size=(float(width) * X_BLOCK, float(height) * Y_BLOCK))
            scatter = Scatter(do_rotation=False, do_scale=False, do_translation=False)
            scatter.pos = (xpos * X_BLOCK, ypos * Y_BLOCK)
            scatter.add_widget(image)
            graphics_widget.add_widget(scatter)

        #for td in self.sprites_data:
        #    filename,xpos,ypos,width,height = td.split(":")
        #    xpos = float(xpos)
        #    ypos = float(ypos)
        #    image = MyImage(texture = self.sprites[filename].texture, keep_ratio=True, allow_stretch=False)
        #    image.set_shadow(False)
        #    scatter = Scatter(do_rotation=False, do_scale=False, do_translation=False)
        #    scatter.pos = (xpos * X_BLOCK, (ypos + 4) * Y_BLOCK / 2)
        #    scatter.add_widget(image)
        #    graphics_widget.add_widget(scatter)
        #    scatter.scale = 6 -  ypos * 1.5

        return graphics_widget

    def introduce_hero(self, dt=None):
        self.image_hero = MyImage(source = PATH + "hero.png", keep_ratio=False, allow_stretch=True, keep_data=True)
        self.image_hero.set_label_position(-4, -12)
        self.image_hero.set_shadow(True)
        self.scatter_hero = Scatter(do_rotation=False, do_scale=False, do_translation=False)
        self.scatter_hero.add_widget(self.image_hero)
        self.scatter_hero.scale= 2 + (0.5 * SCREEN_DENSITY)
        if self.level < 3:
            self.hero_position = [X_BLOCK, Y_BLOCK]
            self.scatter_hero.pos = (self.hero_position[0], self.hero_position[1])
            self.graphics_widget.add_widget(self.scatter_hero)
        else:    
            self.schedule(self.sounds['hero_song'].play, 1.0)
            self.hero_position = [- 2 * X_BLOCK, Y_BLOCK]
            self.scatter_hero.pos = (self.hero_position[0], self.hero_position[1])
            self.graphics_widget.add_widget(self.scatter_hero)
            #
            self.image_hero.walk(60, 2.4 * X_BLOCK)
            anim = Animation(x = X_BLOCK, duration=4)
            anim.start(self.scatter_hero)

        self.image_score.set_score(self.level_score)
        
    def introduce_baddy(self, dt=None):        
        self.baddy_size_ratio = self.baddy_ratio_for_level
        self.baddy_points = self.baddy_points_for_level
        self.image_baddy = MyImage(source = PATH + self.baddy_image, keep_ratio=False, allow_stretch=True)
        self.image_baddy.set_label_position(self.baddy_label_deltax, self.baddy_label_deltay)
        self.image_baddy.set_score(self.baddy_points)
        self.scatter_baddy = Scatter(do_rotation=False, do_scale=False, do_translation=False)
        self.scatter_baddy.add_widget(self.image_baddy)

        self.baddy_size = [X_BLOCK, Y_BLOCK]
        self.baddy_step = (4 * X_BLOCK + 0.0) / self.maximum_attacks

        self.scatter_baddy.scale = self.baddy_size_ratio # * SCREEN_DENSITY
        self.scatter_baddy.pos = (8 * X_BLOCK, Y_BLOCK)
        self.graphics_widget.add_widget(self.scatter_baddy)
        self.image_baddy.walk(30, 60)
        anim = Animation(x=5 * X_BLOCK, duration=2)
        anim.start(self.scatter_baddy)
        self.baddy_position = [5 * X_BLOCK, Y_BLOCK]

    def create_potions(self, numbers):
        self.potion_buttons = []
        self.potion_button_values = []
        for n in numbers:
            button = MyButton(source=PATH + "potion.png",background_color=[0,0,0,0], label_text="-1", font_size = 30)
            self.potion_buttons.append(button)
            self.potion_button_values.append(n)
            button.pos_hint = {'x': .45,'y': .85}
            button.size_hint = (0.12, 0.12)
            button.bind(on_press=self.handle_potion)
            
    def show_potions(self, dt=None):
        for button in self.potion_buttons:
            self.graphics_widget.add_widget(button)
            
    def hide_potions(self):
        for button in self.potion_buttons:
            self.graphics_widget.remove_widget(button)

    def handle_potion(self, widget=None):
        value = self.potion_button_values[self.potion_buttons.index(widget)]
        self.image_baddy.flash(5)
        self.baddy_points = self.baddy_points +  value
        self.image_baddy.set_score(self.baddy_points)

        self.graphics_widget.remove_widget(widget)
        self.potion_buttons.remove(widget)
        self.potion_button_values.remove(value)
        self.decide_next_stage()
        
    def handle_player_action(self, widget=None):
        # HANDLE MULTIPLE WIDGETS USING self._PICKED_GEMS AND THEN CLEAR IT!
        try:
            self.graphics_widget.remove_widget(widget)
        except:
            pass

        image = widget.children[-1]
        self.hide_gems()

        Clock.unschedule(self.image_hero.look_alive)
        Clock.unschedule(self.image_baddy.look_alive)
        #
        widget.pos = (X_BLOCK / (20.0 * (SCREEN_DENSITY **2) * SCREEN_RATIO ), Y_BLOCK / (16 * (SCREEN_DENSITY**2) * SCREEN_RATIO) )
        #
        widget.scale = 0.3
        widget.add_widget(image)
        self.current_gem = widget
        self.scatter_hero.add_widget(widget)

        self.image_hero.walk(40, 60)
        self.image_baddy.walk(40, 60)

        anim1 = Animation(x = 3 * X_BLOCK, t='out_quad')
        anim1.start(self.scatter_hero)
        anim2 = Animation(x = 3.1 * X_BLOCK, t='out_quad')
        anim2.start(self.scatter_baddy)
        
        self.attacks_tried = self.attacks_tried + 1
        if self.maximum_attacks > 0:
            self.baddy_position[0] = self.baddy_position[0] - ((self.attacks_tried +0.0) / self.maximum_attacks) * self.baddy_step
        self.schedule(self.sounds['hero_charge'].play, 0.1)
        self.schedule(self.sounds['baddy_charge'].play, 0.5)
        
        #Handle hit
        hit_value = self.gems.index(widget.children[-1])
        if self.baddy_points / (hit_value + 0.0) == self.baddy_points / hit_value:
            if self.baddy_size_ratio <= self.baddy_ratio_for_level:
                self.level_score = self.level_score + hit_value * self.baddy_points
            self.baddy_points = self.baddy_points / hit_value
            self.baddy_size_ratio = self.baddy_size_ratio - 1
            if self.baddy_size_ratio == 0:
                self.baddy_size_ratio = 0.1
        else:
            self.baddy_points = self.baddy_points * hit_value
            self.baddy_size_ratio = self.baddy_size_ratio + 1
        
        anim1.bind(on_complete = self.update)

    def baddy_vanquished(self, widget=None, event=None):
        self.graphics_widget.remove_widget(self.progress_bar)        
        Animation.cancel_all(self.progress_bar)
        Animation.cancel_all(self.scatter_baddy, 'x')
        self.celebrate()
        self.image_baddy.walk(20, 40) 
        self.image_baddy.children[-1].text=""
        anim1 = Animation(size = (1,1))
        anim1.start(self.image_baddy)        
        self.hide_gems()
        if self.level_score < 0:
            print "NOTIFY USER ABOUT THRESHOLD!"
            self.image_score.flash(10)
            self.schedule(self.level_failed, 2)
        else:
            self.schedule(self.move_to_next_battle, 2)
        
    def level_failed(self, widget=None, event=None):
        self.graphics_widget.remove_widget(self.progress_bar)
        Animation.cancel_all(self.progress_bar)
        Animation.cancel_all(self.scatter_baddy, 'x')
        if self.baddy_points < 2 and self.level_score >= self.score_threshold:
            return
        self.hide_gems()
        anim = Animation(x = - 4 * X_BLOCK, duration = 2)
        self.image_hero.walk(10, 4 * X_BLOCK)        
        anim.start(self.image_hero)

        self.image_baddy.celebrate(240,60)
        self.schedule(self.move_to_repeat_battle, 2)

    def move_to_repeat_battle(self, widget=None, event=None):
        self.graphics_widget.remove_widget(self.scatter_hero)        
        anim = Animation(x = 8 * X_BLOCK, duration = 12)
        self.image_baddy.walk(30, 8 * X_BLOCK)        
        anim.start(self.image_baddy)
        
        self.schedule(self.repeat_battle, 3)        
        
    def move_to_next_battle(self, widget=None, event=None):
        self.graphics_widget.remove_widget(self.scatter_baddy)
        if self.level == 1:
            self.next_battle()
        else:                
            self.schedule(self.sounds['hero_song'].play, .5)            
            self.schedule(self.sounds['hero_song'].play, 3) 
            anim = Animation(x = 8 * X_BLOCK, duration = 4.5)
            self.image_hero.walk(30, 6 * X_BLOCK)        

            anim.start(self.scatter_hero)
            anim.bind(on_complete = self.next_battle)

    def keep_hero_in_same_position(self, dt=None):
        self.image_hero.x = self.image_hero.x + 0.0
        
    def stop_hero_motion(self, event=None, widget=None):
        Clock.unschedule(self.keep_hero_in_same_position)

    def next_battle(self, widget=None, event=None):
        self.scatter_baddy.rotation = 0
        if self.level > 1:
            self.graphics_widget.remove_widget(self.scatter_hero)
        
        self.level = self.level + 1
        self.schedule(self.setup_battle, 2.0)

    def remove_item(self, animation=None, widget=None):
        self.graphics_widget.remove_widget(widget)
        widget.canvas.clear()
        widget = None
        
    def update(self, widget=None, event=None):
        self.image_hero.angle = 0
        self.image_baddy.angle = 0
        
        try:
            self.current_gem.remove_widget(self.current_gem.children[-1])
            self.scatter_hero.remove_widget(self.current_gem)
        except:
            pass

        anim1 = Animation(scale=self.baddy_size_ratio) 
        anim2 = Animation(y= self.baddy_position[1]) 
        anim3 = Animation(x= self.baddy_position[0]) 
        anim4 = Animation(x = X_BLOCK)
        anim1.start(self.scatter_baddy)
        anim2.start(self.scatter_baddy)
        if self.time_limit < 0:
            anim3.start(self.scatter_baddy)
        anim4.start(self.scatter_hero)
        self.image_baddy.set_score(self.baddy_points)
        self.image_score.set_score(self.level_score)
        
        if self.scatter_baddy.scale > self.baddy_size_ratio:
            self.hero_celebrate()
        else:
            self.baddy_celebrate()
            
        if self.level_score < 0:
            self.image_score.flash(10)
        
        anim4.bind(on_complete = self.decide_next_stage)

    def decide_next_stage(self, widget=None, event=None):
        if self.baddy_points == 1:
            self.baddy_vanquished()
        elif self.attacks_tried == self.maximum_attacks:
            self.level_failed()
        elif self.baddy_points > 1 and (self.is_impossible(self.baddy_points)) and not self.potion_buttons:
            self.level_failed()            
        else:
            self.hide_gems()
            self.show_gems()
            
    def talk_hero(self, dt=None):
        self.sounds['hero_talk'].play()
        self.image_hero.jump(60, 60)

    def talk_baddy(self, dt=None):
        self.sounds['baddy_talk'].play()
        self.image_baddy.jump(60, 60)
        
    def look_alive(self, dt=None, dummy=None):
        Clock.schedule_interval(self.image_baddy.look_alive, 1.5)
        Clock.schedule_interval(self.image_hero.look_alive, 2.0)

    def celebrate(self):
        self.image_hero.celebrate(60, 60)

    def hero_celebrate(self, widget=None, event=None):
        self.image_hero.celebrate(60, 60)

    def baddy_celebrate(self, widget=None, event=None):
        self.image_baddy.celebrate(60, 60)
                       
    def load_sounds(self):
        self.sounds = {}
        for f in ["hero_charge", "hero_song", "hero_talk", "baddy_charge", "baddy_talk", "sword1", "sword2", "sword3"]:
            sound = SoundLoader.load(PATH + "sounds/" + f + '.wav')
            self.sounds[f] = MySound(sound)

    def load_gems(self):
        self.gem_sprites = [None] * 10
        self.gem_sources = [""] * 10
        for i in range(2,10,1):
            self.gem_sources[i] = PATH + "gems/" +"gem_0"+str(i)+".png"
            self.gem_sprites[i] = CoreImage(PATH + "gems/" +"gem_0"+str(i)+".png", color=(0,0,0,1))

    def load_textures(self):
        self.textures = {}
        for f in ["splash", "bg_1", "bg_2", "bg_3", "bg_4", "bg_5", "bg_6", "bg_7", "bg_8", "bg_9"]:
            self.textures[f] = CoreImage(PATH+f+".png")

    #def load_sprites(self):
    #    self.sprites = {}
    #    for f in ["tree_green","tree_red","tree_yellow", "castle", "moon"]:
    #        self.sprites[f] = CoreImage(PATH+f+".png")
       
    def calc_baddy_points(self, numbers, n_multiplications):
        product = 1
        for i in range(n_multiplications):
            product = product * random.choice(numbers)
        return product
        
    #def is_prime(self, num):
    #    if divide(num):
    #        return False
    #    return True

    def is_impossible(self, num):
        for weapon in self.weapons:
            if num % weapon == 0:
                return False
        return True

    #def divide(self, num):
    #    div = 2
    #    current = num
    #    dividers = []
    #    while div <= current and div <= num / 2 and current > 1:
    #        if current % div == 0:
    #            dividers.append(div)
    #            current = current / div
    #        else:
    #            div = div + 1
    #    return dividers

class DivideAndConquerApp(App):
    def build(self):
        view = GameView(self)
        return view
        
    def on_pause(self):
        save_state(self.root.level)
        return True

    def on_stop(self):
        save_state(self.root.level)

    def on_rotate(self):
        self.root.reset_level()

    def on_resume(self):
        self.root.reset_level()

        
if __name__ == '__main__':
    DivideAndConquerApp().run()
