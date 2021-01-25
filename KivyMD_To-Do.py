import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.config import Config
Config.read(r'C:\Users\Jens\Desktop\Programming\Python\Task_Game_kivy\config.ini')
# Kivy imports
# -----------------------------------------------------------------------------#


from costum_modules.HABITS import *
from costum_modules.TASKS import *
from costum_modules.ENAMY import *
from costum_modules.AVATAR import *
from kivymd.app import MDApp
from kivy.lang import Builder


from costum_modules.NOTIFICATIONS import *
# imports
# ----------------------------------------------------------------------------#

kv_string = '''
#<KvLang>




    

MDBottomNavigation:
    panel_color: app.theme_cls.bg_dark
    text_color_active: app.theme_cls.primary_color
        
    MDBottomNavigationItem:            
        name: 'task screen'
        text: 'Tasks'
        icon: 'check-box-outline'
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: 15, 15
            
            # canvas.before:
            #     Color:
            #         rgba: 0.5, 0.5, 0.5, 0.1
            #     Rectangle:
            #         size: self.size
            #         pos: self.pos
            #         source: 'hollow_knight_wallpaper\ending.jpg'
        
            Enemy:
                id: enemy
                opponent: avatar
                mirror_image: enemy_mirror
                    
            TaskView:
                id: task_view
                opponent: enemy
                avatar: avatar
        
    MDBottomNavigationItem:
        name: 'habit screen'
        text: 'habits'
        icon: 'clock-check-outline'
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: 15, 15
        
            MirrorEnemy:
                id: enemy_mirror
                mirror_of: enemy
            
            HabitView:
                id: habit_view
                opponent: enemy
                avatar: avatar
    
    # MDBottomNavigationItem:
    #     name: 'project screen'
    #     text: 'projects'
    #     icon: 'folder-open-outline'
        
    #     MDBoxLayout:
    #         orientation: 'vertical'
    #         padding: 15, 15
            
    #         Button:
    #             text: 'lv up'
    #             on_press: avatar.exp += 10
        
    #         MirrorEnemy:
    #             mirror_of: enemy
        
    
    MDBottomNavigationItem:            
        name: 'avatar screen'
        text: 'Avatar'
        icon: 'account'
        
        MDBoxLayout:
            orientation: 'vertical'
            padding: 15, 15
        
            Avatar:
                id: avatar
                opponent: enemy
            
            MDGridLayout:
                padding: 25, 25
                cols: 2
                size_hint_y: 0.7
                size_hint_x: 0.9
                
                MDLabel:
                    text: 'Name:'
                    size_hint_x: 0.5
                    font_size: 24
                    
                MDLabel:
                    text: '[ref=name]{}[/ref]'.format(avatar.name)
                    font_size: 24
                    markup: True
                    on_ref_press: avatar.show_dialog()
                        
                MDLabel:
                    text: 'Level:'
                    size_hint_x: 0.6
                    font_size: 24
                    
                MDLabel:
                    text: str(avatar.level)
                    font_size: 24
                    
                MDLabel:
                    text: 'Attack:'
                    size_hint_x: 0.6
                    font_size: 24
                    
                MDLabel:
                    text: str(avatar.attack)
                    font_size: 24
                    
                MDLabel:
                    text: 'Exp:'
                    size_hint_x: 0.6
                    font_size: 24
                    
                MDLabel:
                    text: str(avatar.exp) + ' / ' + str(avatar.exp_level_up)
                    font_size: 24
                




#</KvLang>
'''
# -----------------------------------------------------------------------------#


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(kv_string)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.title = 'KivyMD To-Do-List'
        self.theme_cls.primary_palette = 'DeepOrange'
        return self.screen

    def on_start(self):
        self.root.ids.avatar.load_avatar_from_file()
        self.root.ids.enemy.load_enemy_from_file()

        self.root.ids.habit_view.load_habits()
        self.root.ids.task_view.load_tasks()
        
        self.root.ids.habit_view.check_for_failed_habits()

    def on_stop(self):
        self.root.ids.enemy.save_enemy_to_file()
        self.root.ids.avatar.save_avatar_to_file()

        self.root.ids.habit_view.save_habits()
        self.root.ids.task_view.save_tasks()
    


if __name__ == '__main__':
    MainApp().run()
