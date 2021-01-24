

# imports
# -----------------------------------------------------------------
import random
import sys
from pathlib import Path
from configparser import ConfigParser, NoOptionError, NoSectionError

from kivy.lang import Builder
from kivy.properties import (
    BoundedNumericProperty, NumericProperty, ObjectProperty, StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import (MDFlatButton)
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager


sys.path.append(
    r'C:\Users\Jens\Desktop\Programming\Python\Task_Game_kivy_with_custom_modules')

# -----------------------------------------------------------------


Builder.load_string('''
#<KvLang>

<Avatar>:
    py_id: avatar
    id: avatar

    orientation: 'horizontal'
    spacing: 15, 15
    padding: 15, 15
    adaptive_height: True

    MDStackLayout:
        orientation: 'lr-bt'
        spacing: 5, 5
        padding: 5, 5

        MDProgressBar:
            value: avatar.exp / avatar.exp_level_up * 100
            orientation: "horizontal"
            size_hint: 1, None
            color: [0.14, 0.62, 1, 1]
            height: '15sp'

        MDLabel:
            id: hp_bar
            text: '{} / {}'.format(avatar.current_health, avatar.maximum_health)
            halign: 'center'
            font_size:  35
            bold: True
            size_hint_y: None
            height: '60sp'
            canvas.before:
                Color:
                    rgba:   1, 0, 0, 1
                Rectangle:
                    size: self.width * avatar.current_health / avatar.maximum_health, self.height
                    pos: self.pos
                Color:
                    rgba:   0, 0, 0, 1
                Line:
                    points: self.x, self.y, self.width + self.x, self.y, self.width + self.x, self.height + self.y, self.x, self.height + self.y
                    close:  True
                    width:  2

        MDLabel:
            text: '[ref=name]{}[/ref]'.format(avatar.name)
            size_hint: 0.5, None
            text_size: self.size
            halign: 'left'
            valign: 'bottom'
            bold: True
            font_size: 25
            markup: True
            on_ref_press: avatar.show_dialog()

        MDLabel:
            text: 'Lv: {}'.format(avatar.level)
            size_hint: 0.5, None
            text_size: self.size
            halign: 'right'
            valign: 'bottom'
            bold: True
            font_size: 25

    ImageWithPressEvent:
        source: avatar.picture_path
        size_hint: None, None
        size: '150sp', '150sp'

<ChangeTextDialog>:
    adaptive_height: True
    MDTextField:
        id: change_name_text_field
        hint_text: 'Change to:'
        text: app.root.ids.avatar.py_id.name

<ImageWithPressEvent@ButtonBehavior+Image>:
    on_press: app.root.ids.avatar.py_id.file_manager_open()



#</KvLang>
''')


class ChangeTextDialog(MDBoxLayout):
    pass


class Avatar(MDBoxLayout):

    level = BoundedNumericProperty(1, min=1, errorvalue=1)
    name = StringProperty('Knight')
    picture_path = StringProperty('knight.png')
    current_health = NumericProperty(15)
    maximum_health = NumericProperty(15)
    attack = NumericProperty(2)
    exp = BoundedNumericProperty(0, min=0, errorvalue=0)
    exp_level_up = NumericProperty(20)

    py_id = ObjectProperty()
    opponent = ObjectProperty()

    save_file = ConfigParser()
    avatar_stats_save_file = r"C:\Users\Jens\Desktop\Programming\Python\Task_Game_kivy_with_custom_modules\avatar.ini"

    attribute_list = [
        'level',
        'name',
        'picture_path',
        'current_health',
        'maximum_health',
        'attack',
        'exp',
        'exp_level_up',
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # check for saved avatar stats
        self.check_for_save_file()

        # loading avatar stats from enemy_and_avatar.ini
        self.load_avatar_from_file()

        # for file chooser (click image)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            ext=['.png', '.ico', '.jpg', 'jpeg'],
            preview=False,
        )

    def on_current_health(self, *args):
        # keep current_health below maximum_health
        if self.current_health > self.maximum_health:
            self.current_health = self.maximum_health

        # being defeated
        elif self.current_health <= 0:
            self.being_defeated()

    def being_defeated(self, *args):
        # leval down penalty and loose exp for this level by defeat
        self.level -= 1
        self.exp = 0
        
        self.refill_health()

    def refill_health(self):
        self.current_healt = self.maximum_health
        return None

    def on_level(self, *args):
        # change stats depending on level by level up
        self.maximum_health = int(15 + self.level * random.uniform(3.5, 3.7))
        self.current_health = self.maximum_health
        self.attack = int(2 + 0.42 * self.level)
        self.exp = 0
        self.exp_level_up = int(random.uniform(1.5, 2) * self.exp_level_up)

    def on_exp(self, *args):
        # level up if exp sufficient
        if self.exp >= self.exp_level_up:
            self.level += 1

    def show_dialog(self, *args):
        """
        opens a MDDialog popup for changing name of avatar
        """
        self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                title='Change Name',
                type="custom",
                content_cls=ChangeTextDialog(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda *args: self.close_dialog(
                            instance=self)
                    ),
                    MDFlatButton(
                        text="SAVE",
                        on_release=lambda *args: self.change_name(
                            instance=self,
                            value=self.dialog.content_cls.ids.change_name_text_field.text
                        )
                    ),
                ],
            )
        # self.dialog.set_normal_height()
        self.dialog.open()

    def close_dialog(self, instance, *args):
        # closing MDDialog
        instance.dialog.dismiss()

    def change_name(self, instance, value):
        # no blank input allowed
        if len(value) > 0:
            instance.name = value
        self.close_dialog(instance=self)

    def file_manager_open(self):
        """
        opens filemanager at path of this file
        """
        self.file_manager.show(
            path=str(Path(__file__).parent.parent.absolute()))
        self.manager_open = True

    def select_path(self, path):
        """
        It will be called when you click on the file name
        or the catalog selection button.
        """
        self.picture_path = path
        self.exit_manager()

    def exit_manager(self, *args):
        """
        Called when the user reaches the root of the directory tree
        """
        # closes file chooser
        self.manager_open = False
        self.file_manager.close()

    def check_for_save_file(self, *args):
        """
        - check if configuration file exists
        - if not, file is created with initial stats
        """

        try:
            # check for all avatar stats in sava_file
            self.save_file.read(self.avatar_stats_save_file)
            for attribute in self.attribute_list:
                self.save_file.get('Avatar', attribute)

        except (NoSectionError, NoOptionError):
            # if section or option not in sava_file --> create file form default values for stats (defined on class level)
            self.save_file.add_section('Avatar')
            for attribute in self.attribute_list:
                self.save_file.set(
                    'Avatar',
                    f'{attribute}',
                    str(getattr(self, attribute))
                )

            with open(self.avatar_stats_save_file, 'w') as file:
                self.save_file.write(file)
        finally:
            # reading content to save_file (ConfigParser object)
            self.save_file.read(self.avatar_stats_save_file)

    def load_avatar_from_file(self, *args):
        """
        loads avatars stats from enemy_and_avatar.ini
        """
        for attribute in self.attribute_list:

            # check type of attribute
            # if type == str --> set attribute
            if type(getattr(self, attribute)) == str:
                setattr(self, attribute, self.save_file.get(
                    'Avatar', f'{attribute}'))

            # check type of attribute
            # if type == int --> set attribute
            elif type(getattr(self, attribute)) == int:
                setattr(self, attribute, self.save_file.getint(
                    'Avatar', f'{attribute}'))

    def save_avatar_to_file(self, *args):
        """
        saves avatars stats to enemy_and_avatar.ini
        """
        for attribute in self.attribute_list:
            # update save_file (ConfigParser object) with avatars stats
            self.save_file.set('Avatar', attribute,
                               str(getattr(self, attribute)))

        # write to save_file
        with open(self.avatar_stats_save_file, 'w') as file:
            self.save_file.write(file)

    def get_hit(self, value, *args):
        self.current_health -= value
