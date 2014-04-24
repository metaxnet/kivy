import kivy

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import random

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.core.window import Window
SCREEN_WIDTH = Window.size[0]
SCREEN_HEIGHT = Window.size[1]
from kivy.graphics.context_instructions import Rotate, PushMatrix, PopMatrix
__version__ = '1.0'

PATH = "./media/"

from kivy.core.audio import SoundLoader

Y_BLOCK = SCREEN_HEIGHT / 6
X_BLOCK = SCREEN_WIDTH / 8

class TestView(BoxLayout):
    def __init__ (self):
        super(TestView, self).__init__()
        #buttons = []
        #for i in range(3):
        #    button = Button(text = str(i), size=(100, 100))
        #    buttons.append(button)
        #    self.add_widget(button)
        #
        #button.bind(on_press = self.callback) #COMPARE WITH NEXT LINE!
        #button.bind(on_touch_down = self.callback)
        self.graphics_widget = FloatLayout(size_hint = (1.0, 0.8))
        self.image_background = Image(source = PATH + "tira.jpg", keep_ratio=False, allow_stretch=True)
        self.graphics_widget.add_widget(self.image_background)
        self.image = RotatedImage(source = PATH + "abir.png", size_hint = (.2, .2)) #, pos=(100,100))
        self.scatter_hero = Scatter(do_rotation=False, do_scale=False)
        self.scatter_hero.add_widget(self.image)
        self.scatter_hero.pos = (100, 100)
        self.graphics_widget.add_widget(self.scatter_hero)
        self.add_widget(self.graphics_widget)
        self.index = 0
        self.direction = 1
        self.hero_direction = -6
        Clock.schedule_interval(self.move_hero, 1.0 / 40)
        
        
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
        
    
    def callback(self, widget, event):
        print widget, event

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
            rgb: (0,0,0)
        Rectangle: 
            source: self.source
            pos: (self.pos[0]+10, self.pos[1])
            size: self.size
    canvas.after:
        PopMatrix
    Label:
        y: root.center_y - 5
        x: root.center_x - 10
        size: min(self.size)*0.1, min(self.size)*0.1
        markup: True
''')

class RotatedImage(Image):
    angle = NumericProperty()
    score = 0
    
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
        self.reset_game()
        self.label_hero_score = Label(text = "HERO")
        self.title_box.add_widget(self.label_hero_score)
        self.label_baddy_score = Label(text = "BADDY")
        self.title_box.add_widget(self.label_baddy_score)
        self.bind_buttons()

    def load_sounds(self):
        self.sounds = {}
        for f in ["abir_charge", "abir_song", "abir_talk", "boss_charge", "boss_talk", "sword1", "sword2", "sword3"]:
            sound = SoundLoader.load(PATH + f + '.wav')
            self.sounds[f] = sound
       
    def calc_baddy_points(self, numbers, n_multiplications):
        product = 1
        for i in range(n_multiplications):
            product = product * random.choice(numbers)
        return product
    
    def reset_game(self):
        self.phase = 0
        self.score = 0
        self.numbers = [2,3,5] #[2,3,4,5,6,7,8,9] #[2,3,5]
        self.n_multiplications = 3
        self.create_buttons([2,3,4,5,6,7,8,9])
        self.setup_battle()
        
    def setup_battle(self, dt=None):
        self.set_background()
        self.introduce_hero()
        Clock.schedule_once(self.introduce_baddy, 5)
        Clock.schedule_once(self.start_battle, 7)

    def start_battle(self, dt=None):
        Clock.schedule_once(self.play_boss_talk, 1.0)
        Clock.schedule_once(self.play_abir_talk, 2.6)
        Clock.schedule_once(self.play_boss_talk, 3.5)

    def create_buttons(self, numbers):
        self.buttons = []
        self.button_values = []
        for n in numbers:
            button = Button(text="[size=30][color=000000]"+str(n)+"[/color][/size]", markup=True,size_hint = (1.0 / len(self.numbers), None), opacity = 0.9, background_normal="",background_color=[1,1,1,0])
            self.control_box.add_widget(button)
            self.buttons.append(button)
            self.button_values.append(n)
        
    def bind_buttons(self, widget=None, event=None):
        for b in self.buttons:
           b.bind(on_press=self.handle_button_press)

    def set_background(self):
        if self.phase > 0:
            self.graphics_widget.remove_widget(self.image_background) 
        self.image_background = Image(source = PATH + "tira"+str(self.phase)+".jpg", keep_ratio=False, allow_stretch=True)
        self.image_background.size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.graphics_widget.add_widget(self.image_background)

    def introduce_hero(self):
        Clock.schedule_once(self.play_abir_song, 0.5)
        self.image_hero = RotatedImage(source = PATH + "abir.png", keep_ratio=False, allow_stretch=True)
        self.scatter_hero = Scatter(do_rotation=False, do_scale=False, do_translation=False)
        self.scatter_hero.add_widget(self.image_hero)        
        self.hero_position = [- X_BLOCK, Y_BLOCK]
        self.scatter_hero.pos = (self.hero_position[0], self.hero_position[1])
        self.graphics_widget.add_widget(self.scatter_hero)
        #
        self.image_hero.walk(60, 2.4 * X_BLOCK)
        anim = Animation(x = X_BLOCK, duration=4)
        anim.start(self.scatter_hero)
        
    def introduce_baddy(self, dt=None):
        self.baddy_size_ratio = self.n_multiplications
        self.baddy_points = self.calc_baddy_points(self.numbers, self.n_multiplications)
        self.image_baddy = RotatedImage(source = PATH + "boss.png", keep_ratio=False, allow_stretch=True)
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
        
    def play_boss_talk(self, dt):
        self.image_baddy.walk(30, 30)
        self.sounds['boss_talk'].play()
        
    def play_abir_talk(self, dt):
        self.image_hero.jump(50, 50)
        self.sounds['abir_talk'].play()

    def play_abir_song(self, dt):
        self.sounds['abir_song'].play()

    def play_boss_charge(self, dt):
        self.sounds['boss_charge'].play()
        
    def play_abir_charge(self, dt):
        self.sounds['abir_charge'].play()

    def play_sword1(self, dt):
        self.sounds['sword1'].play()

    def handle_button_press(self, widget=None):
        self.image_hero.angle = -30
        self.image_baddy.angle = 30

        self.image_hero.walk(40, 60)
        self.image_baddy.walk(40, 60)

        anim1 = Animation(x = 3 * X_BLOCK)
        anim1.start(self.scatter_hero)
        anim2 = Animation(x = 3.1 * X_BLOCK)
        anim2.start(self.scatter_baddy)
        
        value = self.button_values[self.buttons.index(widget)]
        
        Clock.schedule_once(self.play_abir_charge, 0.1)
        Clock.schedule_once(self.play_boss_charge, 0.5)

        if self.baddy_points / (value + 0.0) == self.baddy_points / value:
            if self.baddy_size_ratio <= self.n_multiplications:
                self.score = self.score + value * self.baddy_points
            self.baddy_points = self.baddy_points / value
            self.baddy_size_ratio = self.baddy_size_ratio - 1
        else:
            self.baddy_points = self.baddy_points * value
            self.baddy_size_ratio = self.baddy_size_ratio + 1
        if self.baddy_points == 1:
            print "BADDY VANQUISHED!"
            self.baddy_size_ratio = 0.25
            anim1.bind(on_complete = self.baddy_vanquished)
        else:
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
        anim1 = Animation(scale=self.baddy_size_ratio) 
        anim1.start(self.scatter_baddy)        
        anim2 = Animation(y= self.baddy_position[1]) 
        anim3 = Animation(x= 3.5 * X_BLOCK)
        anim1.start(self.scatter_baddy)
        anim2.start(self.scatter_baddy)
        anim3.start(self.scatter_baddy)
        Clock.schedule_once(self.move_to_next_battle, 2)
        
    def move_to_next_battle(self, widget=None, event=None):
        self.graphics_widget.remove_widget(self.scatter_baddy)        
        Clock.schedule_once(self.play_abir_song, .5)            
        Clock.schedule_once(self.play_abir_song, 3)            
        anim4 = Animation(x = 6 * X_BLOCK, duration = 8)
        self.image_hero.walk(10, 4 * X_BLOCK)        
        anim4.start(self.image_hero)
        Clock.schedule_once(self.next_battle, 8)

    def next_battle(self, dt=None):
        self.scatter_baddy.rotation = 0
        self.graphics_widget.remove_widget(self.scatter_hero)
        self.phase = self.phase + 1
        anim = Animation(x = - 9 * X_BLOCK)
        anim.start(self.image_background)
        Clock.schedule_once(self.setup_battle, 1)
        
    def update(self, widget=None, event=None):
        self.image_hero.angle = 0
        self.image_baddy.angle = 0

        self.label_baddy_score.text = str(self.baddy_points)
        self.label_hero_score.text = str(self.score)        

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
            anim1.bind(on_complete=self.hero_celebrate)
        else:
            anim1.bind(on_complete=self.baddy_celebrate)

        

class KnightApp(App):
    def build(self):
        view = GameView()
        return view
        
if __name__ == '__main__':
    KnightApp().run()
