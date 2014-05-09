import random, math

import kivy

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.graphics.context_instructions import Rotate, PushMatrix, PopMatrix

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

import kivy.resources
kivy.resources.resource_add_path("./girls_have_many_secrets/")

__version__ = '1.0'

SCREEN_WIDTH = Window.size[0]
SCREEN_HEIGHT = Window.size[1]
Y_BLOCK = SCREEN_HEIGHT / 6
X_BLOCK = SCREEN_WIDTH / 8

PATH = "./media/"

def divide(num):
        div = 2
        current = num
        dividers = []
        index = 0
        while div <= current and div <= num / 2 and current > 1:
            index = index + 1
            if current % div == 0:  #and div < num:
                dividers.append(div)
                current = current / div
            else:
                div = div + 1
        return dividers


class TestView(BoxLayout):
    def __init__ (self):
        super(TestView, self).__init__()
        self.graphics_widget = FloatLayout(size_hint = (1.0, 0.8))
        self.image_background = Image(source = PATH + "castle.png", keep_ratio=False, allow_stretch=False)
        self.graphics_widget.add_widget(self.image_background)
        self.image = RotatedImage(source = PATH + "hero.png", size_hint = (.2, .2)) #, pos=(100,100))
        self.scatter_hero = Scatter(do_rotation=False, do_scale=False)
        self.scatter_hero.add_widget(self.image)
        self.scatter_hero.pos = (500, 500)
        self.graphics_widget.add_widget(self.scatter_hero)
        self.add_widget(self.graphics_widget)
        scatters = []
        for i in range(3):
            image = RotatedImage(source = PATH + "hero.png", size_hint = (.2, .2)) #Button(text = str(i))
            image.set_score(i)
            scatter = Scatter(do_rotation=False, do_scale=False)
            scatter.add_widget(image)
            self.graphics_widget.add_widget(scatter)
            scatter.pos = (i * 100, i * 100)
            scatter.size_hint=(.2, .2)
            image.bind(on_touch_down = self.callback1)
            image.bind(on_touch_up = self.callback2)
            #scatter.bind(on_transform_with_touch=self.callback)
            scatters.append(scatter)
            print image.size

        self.index = 0
        self.direction = 1
        self.hero_direction = -6
        #Clock.schedule_interval(self.move_hero, 1.0 / 40)
        self.feedback = Label(text = "")
        self.graphics_widget.add_widget(self.feedback)
        self.chosen_widgets = []
        
        
    def move_hero(self, dt=None):
        self.index = self.index + 1
        if self.index > 500:
            Clock.unschedule(self.move_hero)
        else:
            self.image.angle = self.index % 10
            #self.scatter_hero.rotation += self.direction
            #self.scatter_hero.x = self.index % 5
            if self.index % 10 == 0:
                self.direction = - self.direction
            #self.scatter_hero.y = 100
            #self.scatter_hero.center = (400, 400)
            #print "Center=", self.scatter_hero.center
        
    def callback1(self, widget=None, event=None):
        self.chosen_widgets.append(widget)
        print widget.children[-1].text
        #print event.pos
        #x = widget.parent.x
        #y = widget.parent.y
        #w = widget.width
        #h = widget.height
        #print widget.parent.pos, widget.size, event.pos, event.spos
        #if event.x > x and event.x < x + w and event.y > y and event.y < y + h:
        #    text = "hit "+ widget.children[-1].text
        #else:
        #    text = "miss " + widget.children[-1].text
        #self.feedback.text = self.feedback.text + "\n"+ text
        #return True
        pass
    
    def callback2(self, widget=None, event=None):
        print widget.children[-1].text, event.x + widget.parent.x, event.spos[0], event.y + widget.parent.y, event.spos[1]
        target_x = self.image.parent.x + self.image.center[0]
        target_y = self.image.parent.y + self.image.center[1]
        x = widget.parent.x
        y = widget.parent.y
        w = widget.width
        h = widget.height
        #print widget.parent.pos, widget.size, self.image.parent.pos, self.image.size, self.image.center
        #if target_x > x and target_x < x + w and target_y > y and target_y < y + h:
        #    text = "hit "+ widget.children[-1].text + "("+str(event.pos)+")"
        #else:
        #    text = "miss " + widget.children[-1].text + "("+str(event.pos)+")"
        #return True
        text = []
        for widget in self.chosen_widgets:
           text.append(widget.children[-1].text)
        self.feedback.text = self.feedback.text + "\n"+ ",".join(text)
        self.chosen_widgets = []

class TestApp(App):
    def build(self):
        view = TestView()
        return view

from kivy.properties import NumericProperty
from kivy.lang import Builder
Builder.load_string('''
<RotatedImage>:
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
    canvas.after:
        PopMatrix
    Label:
        y: root.center_y + root.label_deltax
        x: root.center_x + root.label_deltay
        size: min(self.size)*0.1, min(self.size)*0.1
        markup: True
''')

class RotatedImage(Image):
    angle = NumericProperty()
    score = 0
    label_deltax = NumericProperty(-5)
    label_deltay = NumericProperty(-5)
    shadow_opacity = NumericProperty(0.8)
    
    def set_shadow(self, shadow_on):
        if shadow_on:
            self.shadow_opacity = 0.8
        else:
            self.shadow_opacity = 0
    
    def set_label_position(self, deltax, deltay):
        self.label_deltax = deltax
        self.label_deltay = deltay
    
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
                
class Sound():
    def __init__(self, core_sound):
        self.core_sound = core_sound
        
    def play(self, dt=None):
        self.core_sound.play()

def get_state():
    text = open(PATH+"state.txt", "rb").read()
    return text

def save_state(level):
    return
    f = open(PATH+"state.txt", "wb")
    f.write(str(level))
    f.close()

def get_level_data(level_number):
    text = open(PATH+"levels.txt", "rb").read()
    lines = text.split("\n")
    level_data = lines[level_number+1].replace(" ","").split("|")
    return level_data

class GameView(BoxLayout):
    def __init__ (self):
        super(GameView, self).__init__(orientation='vertical')
        self.title_box = BoxLayout(size_hint = (1.0, 0.1))
        #
        self.graphics_widget = FloatLayout()
        #
        self.control_box = BoxLayout(size_hint = (1.0, 0.01))
        #
        self.add_widget(self.title_box)
        self.add_widget(self.graphics_widget)
        self.add_widget(self.control_box)
        self.load_sounds()
        self.load_textures()
        self.load_sprites()
        self.load_gems()
        self.schedules = []
        self.reset_level()
        self.label_hero_score = Label(text = "HERO")
        self.title_box.add_widget(self.label_hero_score)
        self.button_reset = Button(text="RESET", on_press=self.reset)
        self.title_box.add_widget(self.button_reset)
        self.label_baddy_score = Label(text = "BADDY")
        self.title_box.add_widget(self.label_baddy_score)
        
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
        save_state(0)
        self.reset_level()

    def load_sounds(self):
        self.sounds = {}
        for f in ["hero_charge", "hero_song", "hero_talk", "baddy_charge", "baddy_talk", "sword1", "sword2", "sword3"]:
            sound = SoundLoader.load(PATH + f + '.wav')
            self.sounds[f] = Sound(sound)

    def load_gems(self):
        self.gem_sprites = [0] * 10
        for i in range(2,9,1):
            self.gem_sprites[i] = CoreImage(PATH+"gem_0"+str(i)+".png", color=(0,0,0,1))

    def load_textures(self):
        self.textures = {}
        for f in ["hill_01", "hill_02", "ground", "cloud", "blue", "night"]:
            self.textures[f] = CoreImage(PATH+f+".png")

    def load_sprites(self):
        self.sprites = {}
        for f in ["tree_green","tree_red","tree_yellow", "castle", "moon"]:
            self.sprites[f] = CoreImage(PATH+f+".png")
       
    def calc_baddy_points(self, numbers, n_multiplications):
        product = 1
        for i in range(n_multiplications):
            product = product * random.choice(numbers)
        return product
        
    def is_prime(self, num):
        if divide(num):
            return False
        return True

    def is_impossible(self, num):
        for weapon in self.weapons:
            if num % weapon == 0:
                return False
        return True

    def divide(self, num):
        div = 2
        current = num
        dividers = []
        while div <= current and div <= num / 2 and current > 1:
            if current % div == 0:
                dividers.append(div)
                current = current / div
            else:
                div = div + 1
        return dividers
        
    def reset_level(self):
        self.level = int(get_state())
        try:        
            for child in self.graphics_widget.children:
               self.graphics_widget.remove_widget(child)
        except:
            pass
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
        self.potions = [int(x) for x in data[9].split(",") if x]
        self.textures_data = data[10].split(";")
        self.sprites_data = data[11].split(";")
        
    def setup_battle(self, dt=None):
        self.schedule(self.introduce_baddy, 5)
        self.schedule(self.start_battle, 7)
        self.get_level_data()
        self.create_gems(self.weapons)
        self.level_score = 0
        self.attacks_tried = 0
        self.set_background()
        self.introduce_hero()

    def start_battle(self, dt=None):
        self.label_baddy_score.text = str(self.baddy_points)
        self.label_hero_score.text = str(self.level_score)        
        self.schedule(self.talk_baddy, 1.0)
        self.schedule(self.talk_hero, 2.5)
        self.schedule(self.talk_baddy, 3.5)
        self.schedule(self.show_gems, 5.0)
        self.schedule(self.show_potions, 5.0)
        self.schedule(self.look_alive, 5.0)

    def create_gems(self, numbers):
        self.gems = [0] * 10
        self.gem_values = [0] * 10
        for i in range(len(numbers)):
            n = numbers[i]
            gem = RotatedImage(keep_ratio=True, allow_stretch=False, color=(0,0,0,0))
            gem.set_shadow(False)
            with gem.canvas:
                Rectangle(texture=self.gem_sprites[n].texture, size = (75,75))
            self.gems[n] = gem
            self.gem_values[n] = n
            
    def drop_gem(self, widget=None, event=None):
        if widget not in self.graphics_widget.children:
            return True
        if widget.x > self.scatter_hero.x and widget.x < self.scatter_hero.x + self.image_hero.width:
            if widget.y > self.scatter_hero.y and widget.y < self.scatter_hero.y + self.image_hero.height:
                try:
                    self.graphics_widget.remove_widget(widget)
                except:
                    pass
                self.handle_button_press(widget)
                return True
            else:
                self.hide_gems()
                self.show_gems()
        else:
            self.hide_gems()
            self.show_gems()
        return False

    def hide_gems(self, dt=None, dummy=None):
        for scatter in self.gem_scatters:
            if scatter.children:
                scatter.remove_widget(scatter.children[-1])
            self.graphics_widget.remove_widget(scatter)
    
    def show_gems(self, dt=None, dummy=None):
        self.gem_scatters = []
        for i in range(len(self.weapons)):
            gem = self.gems[self.weapons[i]]
            scatter = Scatter(do_rotation=False, do_scale=False, color=(0,0,0,0))
            scatter.add_widget(gem)
            scatter.bind(on_touch_up=self.drop_gem)
            scatter.pos = ((i + 1) * X_BLOCK, Y_BLOCK / 2)
            scatter.scale = 0.5
            try:
                self.graphics_widget.add_widget(scatter)
                self.gem_scatters.append(scatter)
            except:
                print "Again in show gems!"
        
    def set_background(self):
        self.image_background = Image(color=(0,0,0,0))
        self.image_background.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.graphics_widget.add_widget(self.image_background)

        xpos_list = []
        scatters = []

        for td in self.textures_data:
            filename,xpos,ypos,width,height = td.split(":")
            xpos = float(xpos)
            ypos = float(ypos)
            image = RotatedImage(keep_ratio=True, allow_stretch=False, color=(0,0,0,0))
            image.set_shadow(False)
            with image.canvas:
                Rectangle(texture=self.textures[filename].texture, size=(float(width) * X_BLOCK, float(height) * Y_BLOCK))
            scatter = Scatter(do_rotation=False, do_scale=False, do_translation=False)
            scatter.pos = (8 * X_BLOCK + xpos * X_BLOCK, ypos * Y_BLOCK)
            scatter.add_widget(image)
            self.graphics_widget.add_widget(scatter)
            xpos_list.append(xpos)
            scatters.append(scatter)

        for td in self.sprites_data:
            filename,xpos,ypos,width,height = td.split(":")
            xpos = float(xpos)
            ypos = float(ypos)
            image = RotatedImage(texture = self.sprites[filename].texture, keep_ratio=True, allow_stretch=False)
            image.set_shadow(False)
            scatter = Scatter(do_rotation=False, do_scale=False, do_translation=False)
            scatter.pos = (8 * X_BLOCK + xpos * X_BLOCK, (ypos + 4) * Y_BLOCK / 2)
            scatter.add_widget(image)
            self.graphics_widget.add_widget(scatter)
            scatter.scale = 6 -  ypos * 1.5
            xpos_list.append(xpos)
            scatters.append(scatter)

        for i in range(len(xpos_list)):
            anim = Animation(x = xpos_list[i] * X_BLOCK, duration=2)
            anim.start(scatters[i])

    def introduce_hero(self):
        self.schedule(self.sounds['hero_song'].play, 1.0)

        self.image_hero = RotatedImage(source = PATH + "hero.png", keep_ratio=False, allow_stretch=True)
        self.scatter_hero = Scatter(do_rotation=False, do_scale=False, do_translation=False)
        self.scatter_hero.add_widget(self.image_hero)
        self.scatter_hero.scale= 1.5        
        self.hero_position = [- X_BLOCK, Y_BLOCK]
        self.scatter_hero.pos = (self.hero_position[0], self.hero_position[1])
        self.graphics_widget.add_widget(self.scatter_hero)
        #
        self.image_hero.walk(60, 2.4 * X_BLOCK)
        anim = Animation(x = X_BLOCK, duration=4)
        anim.start(self.scatter_hero)
        
    def introduce_baddy(self, dt=None):
        self.baddy_size_ratio = self.baddy_ratio_for_level
        self.baddy_points = self.baddy_points_for_level #self.calc_baddy_points(self.numbers, self.n_multiplications)
        self.image_baddy = RotatedImage(source = PATH + self.baddy_image, keep_ratio=False, allow_stretch=True)
        self.image_baddy.set_label_position(self.baddy_label_deltax, self.baddy_label_deltay)
        self.image_baddy.set_score(self.baddy_points)
        self.scatter_baddy = Scatter(do_rotation=False, do_scale=False, do_translation=False)
        self.scatter_baddy.add_widget(self.image_baddy)
        self.baddy_position = [8 * X_BLOCK, Y_BLOCK]
        self.baddy_size = [X_BLOCK, Y_BLOCK]
        self.label_baddy_score.text = str(self.baddy_points)
        self.scatter_baddy.scale = self.baddy_size_ratio
        self.scatter_baddy.pos = (self.baddy_position[0], self.baddy_position[1])
        self.graphics_widget.add_widget(self.scatter_baddy)
        self.image_baddy.walk(30, 60)
        anim = Animation(x=5 * X_BLOCK, duration=2)
        anim.start(self.scatter_baddy)
        self.baddy_position[0] = 5 * X_BLOCK

    def present_potions(self, numbers):
        self.potion_buttons = []
        self.potion_button_values = []
        for n in numbers:
            button = Button(text="[size=30][color=ffffff]"+str(n)+"[/color][/size]", markup=True,size_hint = (0.1, None), opacity = 1.0, background_normal="",background_color=[0,0,0,0])
            self.potion_buttons.append(button)
            self.potion_button_values.append(n)
            button.pos = (4 * X_BLOCK, 4 * Y_BLOCK)
            button.bind(on_press=self.handle_potion)
            self.graphics_widget.add_widget(button)
            with button.canvas:
                Color(0.0,0,2,0.2)
                Ellipse(size = button.size, pos = button.pos)

    def show_potions(self, dt=None, dummy=None):
        if self.potions:
            self.present_potions(self.potions)
            
    def talk_hero(self, dt=None):
        self.sounds['hero_talk'].play()
        self.image_hero.jump(60, 60)

    def talk_baddy(self, dt=None):
        self.sounds['baddy_talk'].play()
        self.image_baddy.jump(60, 60)
        
    def look_alive(self, dt=None, dummy=None):
        Clock.schedule_interval(self.image_baddy.look_alive, 1.5)
        Clock.schedule_interval(self.image_hero.look_alive, 2.0)
            
    def handle_potion(self, widget=None):
        value = self.potion_button_values[self.potion_buttons.index(widget)]
        self.baddy_points = self.baddy_points +  value
        self.image_baddy.set_score(self.baddy_points)
        self.label_baddy_score.text = str(self.baddy_points)
        self.graphics_widget.remove_widget(widget)
        if self.baddy_points > 1 and (self.is_impossible(self.baddy_points)):
            self.potions = [-1]
            self.show_potions()
        
    def handle_button_press(self, widget=None):
        image = widget.children[-1]
        self.hide_gems()

        Clock.unschedule(self.image_hero.look_alive)
        Clock.unschedule(self.image_baddy.look_alive)

        widget.pos = (-40,-30)
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
        
        self.label_baddy_score.text = str(self.baddy_points)
        self.label_hero_score.text = str(self.level_score)
        #
        if self.baddy_points > 1 and (self.is_impossible(self.baddy_points)):
            self.potions = [-1]
            self.show_potions()

        #Check if battle is over
        anim1.bind(on_complete = self.update)

    def celebrate(self):
        self.image_hero.celebrate(60, 60)

    def hero_celebrate(self, widget=None, event=None):
        self.image_hero.celebrate(60, 60)

    def baddy_celebrate(self, widget=None, event=None):
        self.image_baddy.celebrate(60, 60)
            
    def baddy_vanquished(self, widget=None, event=None):
        self.celebrate()
        self.image_baddy.walk(20, 40)  
        anim1 = Animation(scale=0.1)
        anim1.start(self.scatter_baddy)        
        anim2 = Animation(y= self.baddy_position[1]) 
        anim3 = Animation(x= self.baddy_position[0] + X_BLOCK) #3.5 * X_BLOCK)
        #anim1.start(self.scatter_baddy)
        anim2.start(self.scatter_baddy)
        anim3.start(self.scatter_baddy)
        self.hide_gems()
        if self.level_score < self.score_threshold:
            self.schedule(self.level_failed, 2)
        else:
            self.schedule(self.move_to_next_battle, 2)
        
    def level_failed(self, widget=None, event=None):
        self.graphics_widget.remove_widget(self.scatter_baddy)        
        anim4 = Animation(x = - 4 * X_BLOCK, duration = 18)
        self.image_hero.walk(10, 4 * X_BLOCK)        
        anim4.start(self.image_hero)
        
        self.schedule(self.setup_battle, 8)        
        
    def move_to_next_battle(self, widget=None, event=None):
        self.graphics_widget.remove_widget(self.scatter_baddy)        
        self.schedule(self.sounds['hero_song'].play, .5)            
        self.schedule(self.sounds['hero_song'].play, 3) 
        anim4 = Animation(x = 6 * X_BLOCK, duration = 8)
        self.image_hero.walk(60, 4 * X_BLOCK)        
        anim4.start(self.image_hero)
        self.schedule(self.next_battle, 8)

    def next_battle(self, dt=None):
        self.scatter_baddy.rotation = 0
        self.graphics_widget.remove_widget(self.scatter_hero)
        self.level = self.level + 1

        for item in self.graphics_widget.children:
            xpos = item.x
            anim = Animation(x = xpos - 9 * X_BLOCK, duration=2.5)
            anim.start(item)
        self.setup_battle()
        
    def update(self, widget=None, event=None):
        self.image_hero.angle = 0
        self.image_baddy.angle = 0
        self.current_gem.remove_widget(self.current_gem.children[-1])
        self.scatter_hero.remove_widget(self.current_gem)

        anim1 = Animation(scale=self.baddy_size_ratio) 
        anim2 = Animation(y= self.baddy_position[1]) 
        anim3 = Animation(x= self.baddy_position[0]) 
        anim4 = Animation(x = X_BLOCK)
        anim1.start(self.scatter_baddy)
        anim2.start(self.scatter_baddy)
        anim3.start(self.scatter_baddy)
        anim4.start(self.scatter_hero)
        self.image_baddy.set_score(self.baddy_points)
        
        if self.scatter_baddy.scale > self.baddy_size_ratio:
            self.hero_celebrate()
        else:
            self.baddy_celebrate()

        if self.baddy_points == 1:
            anim3.bind(on_complete = self.baddy_vanquished)
        elif self.attacks_tried == self.maximum_attacks:
            anim3.bind(on_complete = self.level_failed)
        else:
            anim3.bind(on_complete = self.show_gems)

class KnightApp(App):
    def build(self):
        view = GameView()
        return view
        
    def on_pause(self):
        print "Pause"
        save_state(self.root.level)
        return True

    def on_stop(self):
        print "Stop"
        save_state(self.root.level)

    def on_rotate(self):
        print "Stop"
        self.root.reset_level()

    def on_resume(self):
        print "Resume"
        self.root.reset_level()

        
if __name__ == '__main__':
    KnightApp().run()
    #TestApp().run()
