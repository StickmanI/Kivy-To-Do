
# imports
# -----------------------------------------------------------------
import os
import random
import re
import sys
from configparser import ConfigParser, NoOptionError, NoSectionError

from kivy.lang import Builder
from kivy.properties import (BoundedNumericProperty, NumericProperty,
                             ObjectProperty, StringProperty)
from kivymd.uix.boxlayout import MDBoxLayout

sys.path.append(
    r'C:\Users\Jens\Desktop\Programming\Python\Task_Game_kivy_with_custom_modules')

# -----------------------------------------------------------------


Builder.load_string('''
#<KvLang>

<Enemy>:
    py_id: enemy
    id: enemy

    orientation: 'horizontal'
    spacing: 15, 15
    padding: 15, 15
    adaptive_height: True

    MDStackLayout:
        orientation: 'lr-bt'
        spacing: 5, 5
        padding: 5, 5

        MDLabel:
            id: hp_bar
            text: '{} / {}'.format(enemy.current_health, enemy.maximum_health)
            halign: 'center'
            font_size:  35
            bold: True
            size_hint_y: None
            height: '60sp'
            canvas.before:
                Color:
                    rgba:   1, 0, 0, 1
                Rectangle:
                    size: self.width * enemy.current_health / enemy.maximum_health, self.height
                    pos: self.pos
                Color:
                    rgba:   0, 0, 0, 1
                Line:
                    points: self.x, self.y, self.width + self.x, self.y, self.width + self.x, self.height + self.y, self.x, self.height + self.y
                    close:  True
                    width:  2

        MDLabel:
            text: enemy.name
            size_hint: 0.5, None
            text_size: self.size
            halign: 'left'
            valign: 'bottom'
            bold: True
            font_size: 25
            markup: True

        MDLabel:
            text: 'Lv: {}'.format(enemy.level)
            size_hint: 0.5, None
            text_size: self.size
            halign: 'right'
            valign: 'bottom'
            bold: True
            font_size: 25

    Image:
        source: enemy.picture_path
        size_hint: None, None
        size: '150sp', '150sp'

<MirrorEnemy>:
    orientation: 'horizontal'
    spacing: 15, 15
    padding: 15, 15
    adaptive_height: True

    MDStackLayout:
        orientation: 'lr-bt'
        spacing: 5, 5
        padding: 5, 5

        MDLabel:
            id: hp_bar
            text: '{} / {}'.format(root.current_health, root.maximum_health,)
            halign: 'center'
            font_size:  35
            bold: True
            size_hint_y: None
            height: '60sp'
            canvas.before:
                Color:
                    rgba:   1, 0, 0, 1
                Rectangle:
                    size: 0 if root.mirror_of == None else root.mirror_of.ids.hp_bar.width * root.current_health / root.maximum_health, self.height
                    pos: self.pos
                Color:
                    rgba:   0, 0, 0, 1
                Line:
                    points: self.x, self.y, self.width + self.x, self.y, self.width + self.x, self.height + self.y, self.x, self.height + self.y
                    close:  True
                    width:  2

        MDLabel:
            text: root.name
            size_hint: 0.5, None
            text_size: self.size
            halign: 'left'
            valign: 'bottom'
            bold: True
            font_size: 25
            markup: True

        MDLabel:
            text: 'Lv: ' + str(root.level)
            size_hint: 0.5, None
            text_size: self.size
            halign: 'right'
            valign: 'bottom'
            bold: True
            font_size: 25

    Image:
        # source: '' if root.mirror_of == None else root.mirror_of.picture_path
        source: root.picture_path
        size_hint: None, None
        size: '150sp', '150sp'


#</KvLang>
''')


class Enemy(MDBoxLayout):
    """
    - Use inside kv file/language:
        Enemy:
            id: enemy       # always use an id, for referencing within the main file
            opponent: <reference to avatar object>  # always assign this; needed for interaction with enemy
            # possible to set stats if desired like this:
            name: 'initial name'
            ...
    """

    level = BoundedNumericProperty(1, min=1, errorvalue=1)
    name = StringProperty('Aluba')
    picture_path = StringProperty('enemy_pictures\Aluba.png')
    current_health = BoundedNumericProperty(25, min=0, errorvalue=0)
    maximum_health = NumericProperty(25)
    attack = NumericProperty(2)
    exp_give = NumericProperty(2)

    py_id = ObjectProperty()

    opponent = ObjectProperty()
    mirror_image = ObjectProperty()

    save_file = ConfigParser()
    enemy_stats_save_file = r"C:\Users\Jens\Desktop\Programming\Python\Task_Game_kivy_with_custom_modules\enemy.ini"

    attribute_list = [
        'level',
        'name',
        'picture_path',
        'current_health',
        'maximum_health',
        'attack',
        'exp_give',
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # check for saved avatar stats
        self.check_for_save_file()

        # loading avatar stats from enemy_and_avatar.ini
        self.load_enemy_from_file()

    def on_current_health(self, *args):

        if self.current_health > self.maximum_health:
            self.current_health = self.maximum_health

        elif self.current_health == 0:
            self.opponent.exp += self.exp_give
            self.respawn()
            self.save_enemy_to_file()
            self.mirror_image.update(self)

    def respawn(self, *args):
        # change stats depending on level
        self.level += random.choices(population=[-1, 0, 1],
                                     weights=[0.20, 0.4, 0.4])[0]
        self.maximum_health = int(
            25 + self.level * random.uniform(1.4, 1.5) * 2)
        self.current_health = self.maximum_health
        self.attack = int(2 + 1.5 * self.level)
        self.exp_give = int(2 + self.level * 1.3)
        self.update_looks()

    def update_looks(self, *args):
        """
        - randomly choses new image for enemy
        - name of image --> name of enemy
        """
        # regular expression for endings (.png, ...) and digits
        digits = r'[0-9]+'
        endings = r'\..+'

        # chosen = list of files in path
        path = r'enemy_pictures'
        chosen = random.choice(os.listdir(path))

        # removes digits and endings like .png from name
        chosen_semi_clean = re.sub(digits, '', chosen)
        chosen_clean = re.sub(endings, '', chosen_semi_clean)

        # set picture_path and name to chosen file
        self.picture_path = path + '\\' + chosen
        self.name = chosen_clean

    def check_for_save_file(self, *args):
        """
        - check if configuration file exists
        - if not, file is created with initial stats
        """
        try:
            # check for all avatar stats in sava_file
            self.save_file.read(self.enemy_stats_save_file)
            for attribute in self.attribute_list:
                self.save_file.get('Enemy', attribute)

        except (NoSectionError, NoOptionError):
            # if section or option not in sava_file --> create file form default values for stats (defined on class level)
            self.save_file.add_section('Enemy')
            for attribute in self.attribute_list:
                self.save_file.set(
                    'Enemy',
                    f'{attribute}',
                    str(getattr(self, attribute))
                )

            with open(self.enemy_stats_save_file, 'w') as file:
                self.save_file.write(file)
        finally:
            # reading content to save_file (ConfigParser object)
            self.save_file.read(self.enemy_stats_save_file)

    def load_enemy_from_file(self, *args):
        """
        loads enemys stats from enemy_and_avatar.ini
        """
        for attribute in self.attribute_list:
            # check type of attribute
            # if type == str --> set attribute
            if type(getattr(self, attribute)) == str:
                setattr(self, attribute, self.save_file.get(
                    'Enemy', f'{attribute}'))

            # check type of attribute
            # if type == int --> set attribute
            elif type(getattr(self, attribute)) == int:
                setattr(self, attribute, self.save_file.getint(
                    'Enemy', f'{attribute}'))

    def save_enemy_to_file(self, *args):
        """
        saves enemys stats to enemy_and_avatar.ini
        """
        for attribute in self.attribute_list:
            # update save_file (ConfigParser object) with enemys stats
            self.save_file.set('Enemy', attribute,
                               str(getattr(self, attribute)))

        # write to save_file
        with open(self.enemy_stats_save_file, 'w') as file:
            self.save_file.write(file)

    def get_hit(self, value, *args):
        self.current_health -= value
        self.save_enemy_to_file()
        self.mirror_image.update(self)


class MirrorEnemy(MDBoxLayout):
    mirror_of = ObjectProperty()

    level = BoundedNumericProperty(1, min=1, errorvalue=1)
    name = StringProperty('Aluba')
    picture_path = StringProperty('enemy_pictures\Aluba.png')
    current_health = BoundedNumericProperty(25, min=0, errorvalue=0)
    maximum_health = NumericProperty(25)

    save_file = ConfigParser()
    enemy_stats_save_file = r"C:\Users\Jens\Desktop\Programming\Python\Task_Game_kivy_with_custom_modules\enemy.ini"

    attribute_list = [
        'level',
        'name',
        'picture_path',
        'current_health',
        'maximum_health',
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # check for saved avatar stats
        self.check_for_save_file()

        # loading avatar stats from enemy_and_avatar.ini
        self.load_enemy_from_file()

    def check_for_save_file(self, *args):
        """
        - check if configuration file exists
        - if not, file is created with initial stats
        """
        try:
            # check for all avatar stats in sava_file
            self.save_file.read(self.enemy_stats_save_file)
            for attribute in self.attribute_list:
                self.save_file.get('Enemy', attribute)

        except (NoSectionError, NoOptionError):
            # if section or option not in sava_file --> create file form default values for stats (defined on class level)
            self.save_file.add_section('Enemy')
            for attribute in self.attribute_list:
                self.save_file.set(
                    'Enemy',
                    f'{attribute}',
                    str(getattr(self, attribute))
                )

            with open(self.enemy_stats_save_file, 'w') as file:
                self.save_file.write(file)
        finally:
            # reading content to save_file (ConfigParser object)
            self.save_file.read(self.enemy_stats_save_file)

    def load_enemy_from_file(self, *args):
        """
        loads enemys stats from enemy_and_avatar.ini
        """
        self.check_for_save_file()
        
        for attribute in self.attribute_list:
            # check type of attribute
            # if type == str --> set attribute
            if type(getattr(self, attribute)) == str:
                setattr(self, attribute, self.save_file.get(
                    'Enemy', f'{attribute}'))

            # check type of attribute
            # if type == int --> set attribute
            elif type(getattr(self, attribute)) == int:
                setattr(self, attribute, self.save_file.getint(
                    'Enemy', f'{attribute}'))

    def update(self, original_enemy, *args):
        
        # in case file is updated
        self.check_for_save_file()
        self.load_enemy_from_file()