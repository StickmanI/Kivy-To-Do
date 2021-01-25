# imports
# -----------------------------------------------------------------
import json
import sys

from costum_modules.HOLIDAYS import *

from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from costum_modules.NOTIFICATIONS import *
from kivy.lang import Builder
from kivy.properties import ObjectProperty, OptionProperty, StringProperty, NumericProperty, ListProperty, DictProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDFloatingBottomButton, MDIconButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (BaseListItem, ContainerSupport, ILeftBodyTouch,
                             IRightBody, IRightBodyTouch, MDCheckbox,
                             OneLineListItem, ThreeLineAvatarListItem)
from kivymd.uix.menu import MDDropdownMenu

from kivy.clock import Clock
import datetime
from kivymd.toast import toast

from kivymd.uix.picker import MDTimePicker


sys.path.append(
    r'C:\Users\Jens\Desktop\Programming\Python\Task_Game_kivy_with_custom_modules')

# -----------------------------------------------------------------


Builder.load_string('''
#<KvLang>

# Habit View
# -----------------------------------------------------------------
<HabitView>:    
    ScrollView:
        adaptive_height: True
        size_hint_x: 0.86
        pos_hint: {'x': 0.05}

        MDList:
            id: habit_list
    
    AddHabitButton:
        icon: 'plus'
        md_bg_color: app.theme_cls.primary_dark
        pos_hint: {'center_x': 0.95, 'center_y': 0.05}
        on_press: self.show_task_template(title='Create Habit')


# Habit
# -----------------------------------------------------------------
<BasicHabit>:
    theme_text_color: 'Custom'
    text_color: root.theme_cls.primary_color
    font_style: 'H6'

    LeftCheckboxHabit:
        id: check_box_habit
        state: root.check_state
        on_state:
            root.check_state = self.state

    MDBoxLayout:
        id: _right_container
        size_hint: None, None
        x: root.width - len(self.children) * dp(41)
        y: root.y + root.height/2 - self.height/2
        size: dp(24) * len(root.children), dp(48)

        MDIcon:
            icon: 'reload'
            size_hint_x: None
            width: dp(25)
            theme_text_color: 'Custom'
            text_color: [1, 1, 1, 0.3]

        DoneCounter:
            id: done_count
            text: 'test'
            size_hint_x: None
            width: dp(75)
            font_size: 21
            theme_text_color: 'Custom'
            text_color: [1, 1, 1, 0.3]
            text: str(root.done_counter) + ' / ' + str(root.done_counter_max)

        PriorityLabel:
            id: priority_id
            priority: int(root.priority)
            size_hint_x: None
            width: dp(24)

        RightMenuIconButtonHabit:
            id: right_menu_habit
            habit_instance: root
            icon: 'dots-vertical'
            on_press: self.habit_menu.open()

<PriorityLabel>:
    text: '!' * self.priority
    font_size: 26
    theme_text_color: 'Custom'
    size_hint: None, None
    size: dp(50), dp(48)
    on_priority: self.change_priority_color()


# Habit Template
# -----------------------------------------------------------------
<HabitTemplate>:
    adaptive_height: True
    orientation: 'vertical'
    padding: 15, 0

    MDTextField:
        id: habit_description
        hint_text: 'Task Description'

    MDBoxLayout:
        orientation: 'horizontal'
        adaptive_height: True
        width: dp(200)
        size_hint_x: None

        MDLabel:
            text: 'Priority:'

        PriorityChooser:
            id: priority_choice
            text: 'low'
            on_release:
                self.priority_menu.open()

    MDGridLayout:
        id: reminder_days
        cols: 5
        orientation: 'horizontal'
        adaptive_size: True
        padding: 0, 25

        MyToggleButton:
            text: 'Mon'
            state: root.habit_repetition[str(self.text)]
            on_press: self.toggle_habit_repetition(root)
        MyToggleButton:
            text: 'Tue'
            state: root.habit_repetition[str(self.text)]
            on_press: self.toggle_habit_repetition(root)
        MyToggleButton:
            text: 'Wed'
            state: root.habit_repetition[str(self.text)]
            on_press: self.toggle_habit_repetition(root)
        MyToggleButton:
            text: 'Thu'
            state: root.habit_repetition[str(self.text)]
            on_press: self.toggle_habit_repetition(root)
        MyToggleButton:
            text: 'Fri'
            state: root.habit_repetition[str(self.text)]
            on_press: self.toggle_habit_repetition(root)
        MyToggleButton:
            text: 'Sat'
            state: root.habit_repetition[str(self.text)]
            on_press: self.toggle_habit_repetition(root)
        MyToggleButton:
            text: 'Sun'
            state: root.habit_repetition[str(self.text)]
            on_press: self.toggle_habit_repetition(root)

    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        padding: 0, 15

        MDLabel:
            text: 'Repetition per Day'
        
        MDTextField:
            id: times_repetition
            text: '1'
            size_hint_x: None            
            halign: 'center'
    

    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        padding: 0, 15

        MDLabel:
            text: 'Reminder'

        MDBoxLayout:
            orientation: 'vertical'
            adaptive_height: True
            padding: 0, 10

            AddReminderButton:
                text: 'Add Reminder'
                reminder_list_instance: reminder_list
                root_instance: root
                text_color: self.theme_cls.primary_dark
                on_press: self.add_reminder()

        MDBoxLayout:
            orientation: 'vertical'
            adaptive_height: True

            ScrollView:
                size_hint_x: 0.9
                pos_hint: {'center_x': 0.5}

                MDList:
                    id: reminder_list



<Reminder>:
    theme_text_color: 'Custom'
    text_color: self.theme_cls.primary_color
    on_press: self.change_reminder()

    MDBoxLayout:
        id: _right_container
        size_hint: None, None
        x: root.width - len(self.children) * dp(50)
        y: root.y + root.height/2 - self.height/2
        size: dp(24) * len(root.children), dp(48)

        MDIconButton:
            icon: 'minus'
            on_press: root.self_removal()



#</KvLang>
''')

# Habit View
# -----------------------------------------------------------------


class HabitView(MDFloatLayout):

    opponent = ObjectProperty()
    avatar = ObjectProperty()

    attribute_list = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attribute_list = [
            attribute for attribute in [
                'text',
                'secondary_text',
                'tertiary_text',
                'done_counter',
                'done_counter_max',
                'priority',
                'finish_date',
                'last_used',
            ]
        ]

        # calling notifications
        Clock.schedule_interval(self.call_overview_notification, 3600)

    def add_habit(self, description='', week_day='', reminder=[], priority='0', repetition_done=0, repetition=0, finish_date='', last_used='', *args):
        self.ids.habit_list.add_widget(
            ThreeLineHabit(
                text=str(description),
                secondary_text=str(week_day),
                tertiary_text=str(', '.join(reminder)),
                priority=str(priority),
                done_counter=int(repetition_done),
                done_counter_max=int(repetition),
                finish_date=str(finish_date),
                last_used=str(last_used),
                opponent=self.opponent,
                avatar=self.avatar,
            )
        )

    def save_habits(self, *args):

        # collect infos for each habit
        # format: [
        #   {attribute 1: value 1, ...},    (Habit 1)
        #   {attribute 1: value 1, ...},    (Habit 2)
        #   ...
        # ]
        saved_habits = [
            {
                attribute: getattr(child, str(attribute))
                for attribute in self.attribute_list
            }
            for child in self.ids.habit_list.children[::-1]
        ]

        with open(r'saves/save_habits.json', 'w') as file:
            json.dump(saved_habits, file, indent=4)

    def load_habits(self, *args):
        try:
            # loads habits from save file
            with open(r'saves/save_habits.json', 'r') as file:
                data_saved_habits = json.load(file)

            # creates habit instances form content of save file
            for habit in data_saved_habits:
                self.add_habit(
                    description=str(habit['text']),
                    week_day=str(habit['secondary_text']),
                    reminder=habit['tertiary_text'].split(', '),
                    priority=str(habit['priority']),
                    repetition_done=int(habit['done_counter']),
                    repetition=int(habit['done_counter_max']),
                    finish_date=str(habit['finish_date']),
                    last_used=str(habit['last_used']),
                )

            # habits already done today --> disabled
            self.check_for_disabeling()

        except IOError:
            pass

    def check_for_disabeling(self, *args):
        for child in self.ids.habit_list.children:
            child.check_for_disableing()

    def call_overview_notification(self, *args):
        
        # collects Habit.description of all active habits if habit is scheduled for this day
        content = [
            child.text for child in self.ids.habit_list.children[::-1] 
            if child.done_counter < child.done_counter_max 
            and f'{datetime.datetime.today() :%a}' in child.secondary_text
            ]
        
        if len(content) > 0:
            self.new_overview_notification(content)
        return None
    
    def new_overview_notification(self, notification_content, *args):        
        return OverviewNotification(notification_content)

    def check_for_failed_habits(self):
        
        # checks at end of day (start of application next day) for not done habits
        # iterate over all habits
        # for each habit execute check_for_failed()
        for child in self.ids.habit_list.children:
            child.check_for_failed()
        
    class AddHabitButton(MDFloatingBottomButton):

        def show_task_template(self, title):
            self.dialog = None
            if not self.dialog:
                self.dialog = MDDialog(
                    title=str(title) + ':',
                    type="custom",
                    content_cls=HabitTemplate(),
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            text_color=self.theme_cls.primary_color,
                            on_release=self.close_habit_template
                        ),
                        MDFlatButton(
                            text="SAVE",
                            text_color=self.theme_cls.primary_color,
                            on_release=(lambda *args: self.create_habit())
                        ),
                    ],
                )
            self.dialog.open()

        def close_habit_template(self, *args):
            self.dialog.dismiss()

        def create_habit(self, *args):

            # for easier referencing
            template = self.dialog.content_cls.ids

            # geting values for new Habit (inserted in HabitTemplate)
            description = template.habit_description.text
            reminder_days = ', '.join(
                [day.text for day in template.reminder_days.children[::-1] if day.state == 'down'])
            repetition = template.times_repetition.text
            reminder_times = sorted(
                set(
                    [time.text for time in template.reminder_list.children[::-1]]
                )
            )

            # get priority as text from priority_choice ---> into string of number
            priority_translation = {
                '0': 'low',
                '1': 'normal',
                '2': 'high',
                '3': 'very high'
            }
            priority = [key for key, item in priority_translation.items() if item ==
                        self.dialog.content_cls.ids.priority_choice.text][0]

            # check if any item in list is emplty
            def items_in_list_empty(list):
                results = [
                    True if i not in [None, '', ' '] else False
                    for i in list
                ]
                return all(results)

            # create new habit
            if items_in_list_empty([description, reminder_days, reminder_times]):
                self.parent.add_habit(
                    description=description,
                    week_day=reminder_days,
                    reminder=reminder_times,
                    priority=priority,
                    repetition=repetition,
                )
                # close TaskTemplate
                self.close_habit_template()

            else:
                toast("No Description or reminders?", duration=3.5)


# Habit
# -----------------------------------------------------------------


class BasicHabit(ContainerSupport, BaseListItem):

    # check_state linked to checkbox
    # checked --> Task is done
    check_state = OptionProperty("normal", options=["normal", "down"])

    opponent = ObjectProperty(None)
    avatar = ObjectProperty(None)

    done_counter = NumericProperty(0)
    done_counter_max = NumericProperty(1)
    finish_date = StringProperty('')
    last_used = StringProperty('')

    priority = OptionProperty("1", options=[
        '0',    # no
        '1',    # normal
        '2',    # high
        '3',    # very high
    ])

    trigger_list = ListProperty([])

    _no_ripple_effect = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.create_notifications()
        
        self.bind(
            text=lambda *args: self.update_notifications(),
            secondary_text=lambda *args: self.update_notifications(),
            tertiary_text=lambda *args: self.update_notifications(),
            )

    def update_last_used(self, value, *args):
        
        # changes last_used variable to today
        # called after habit done
        today = f'{datetime.datetime.today() :%d.%m.%Y}'
        if value != today:
            self.last_used = today
            
        return None
    
    def check_for_failed(self):
        
        # habit fails if done_counter less than done_counter_max
        if self.done_counter < self.done_counter_max and self.last_used != f'{datetime.datetime.today() :%d.%m.%Y}':
            self.habit_failed()
            self.update_last_used(self.last_used)
        return None
        
    def reset_done_counter(self):
        self.done_counter = 0
        return None

    def is_today_normal_day(self, *args):
        calender = MyCalender()
        today = datetime.datetime.today()
        
        return True if f'{today :%d.%m}' not in calender.holidays else False
        
    def habit_failed(self, *args):
        if self.is_today_normal_day():
            self.avatar.get_hit(
                (1 + 0.1 * int(self.priority)) * self.opponent.attack
                )
            
        # need to reset habit done_counter
        self.reset_done_counter()            
        return None

    def create_notifications(self, *args):
        
        # no notifications on holidays
        if self.is_today_normal_day():
            reminder_times = self.tertiary_text.split(', ')
            
            # creates list of notification objects (rest done by object)
            self.notification_list = [
                Notification(self.text, reminder_time)
                for reminder_time in reminder_times
                ]
            
            # disables notifications of reminders done before firing notification
            self.deactivate_previously_done_notifications()
        return None
    
    def deactivate_previously_done_notifications(self):
        
        reminder_times = self.tertiary_text.split(', ')
                
        # deactivate notification of reminder times already done previously
        done_reminder = len(reminder_times) if self.done_counter >= len(reminder_times) else self.done_counter
        
        done_reminder_indices = [index for index in range(done_reminder)]
        
        for done_index in done_reminder_indices:
            self.notification_list[done_index].deactivate()
            
        return None
        
        # from which reminder time to start
        # still_acitve_reminder = self.done_counter_max - self.done_counter if self.done_counter > len(self.tertiary_text) else self.done_counter

        # make sure reminder times are not empty and today in reminder days
        # if all([
        #     f'{datetime.datetime.now() :%a}' in self.secondary_text.split(', '),
        #     self.tertiary_text not in [None, '', ' '],
        #     self.ids.check_box_habit.disabled != True,
        # ]):
        #     # iterates over remaining active reminders (Habit.tertiary_text)
        #     for index, time in enumerate(self.tertiary_text.split(', ')[still_acitve_reminder:]):
        #         now_time = datetime.datetime.strptime(f'{now:%H:%M}', '%H:%M')
        #         remaining_time = (datetime.datetime.strptime(
        #             time, '%H:%M') - now_time).total_seconds()
           
    def update_notifications(self, *args):
        
        # overrides old notifications --> therefore no error by deleting or adding notifications
        self.create_notifications()
        
        return None
    
    def on_check_state(self, *args):
        if self.check_state == 'down' and self.ids.check_box_habit.disabled == False:

            # reducing enemy current_healt
            self.opponent.get_hit(
                (1 + 0.1 * int(self.priority)) * self.avatar.attack)
            self.check_state = 'normal'
            self.update_last_used(self.last_used)

            # increase done_counter
            if self.done_counter_max > 0:
                self.done_counter += 1
                self.update_notifications()

            # habit completed for today

    def on_done_counter_max(self, *args):

        # done_counter_max has to be upper limit for done_counter
        if self.done_counter_max < 1:
            self.done_counter_max = 1

        self.check_for_disableing()

    def on_done_counter(self, *args):

        # done counter should never be less than 0
        if self.done_counter < 0:
            self.done_counter = 0

        # by finishing habit finish_date is set to today
        # check for opponent == None, due to also execution by init (loading habit changes done_counter --> firing on_done_counter)
        elif self.done_counter == self.done_counter_max and self.opponent not in [None, '', ' ']:
            self.finish_date = f'{datetime.datetime.today():%d.%m.%Y}'

        self.check_for_disableing()

    def on_finish_date(self, *args):

        # resets finish_date to None if finish_date is in past
        if self.finish_date not in [None, '', f'{datetime.datetime.today():%d.%m.%Y}']:
            self.finish_date = ''
            self.reset_done_counter()

    def check_for_disableing(self, *args):
        """
        - checking if habit should be disabled (exept RightMenuIconButtonHabit)
        """
        # only deactivate habit if done today
        if self.done_counter >= self.done_counter_max and self.finish_date == f'{datetime.datetime.today() :%d.%m.%Y}':
            self.disable_habit()
            # self.ids.check_box_habit.active = True

        # for re-activation of habit in case done_counter_max is increased after compleating habit
        elif self.done_counter < self.done_counter_max:
            self.reactivate_habit()

    def disable_habit(self, *args):

        # self.ids is empty due by Habit.__init__()
        # this method is called in initialitation of habit, due to check method by loading habits from file
        if len(self.ids) != 0:

            # disable all widgets in Habit exept RightMenuIconButtonHabit
            for kv_id in [self.ids.priority_id, self.ids._text_container]:
                setattr(kv_id, 'disabled', 'True')

            # set backgroung to gray as inactivation indicator
            self.bg_color = [1, 1, 1, 0.03]

    def reactivate_habit(self, *args):

        # self.ids is empty due by Habit.__init__
        # this method is called in initialitation of habit, due to check method by loading habits from file
        if len(self.ids) != 0:
            self.disabled = False

            # reactivating every widget seperatly (did not work by self.disabled = False alone)
            for kv_id in [self.ids.priority_id, self.ids._text_container]:
                kv_id.disabled = False

                # checkbox needs to be avtive set to False (removing cheked mark)
                if issubclass(kv_id.__class__, BasicHabit.LeftCheckboxHabit):
                    kv_id.active = False

            # set backgroung back to normal
            self.bg_color = self.theme_cls.bg_normal

    def self_removal(self, *args):
        self.parent.remove_widget(self)

    class LeftCheckboxHabit(ILeftBodyTouch, MDCheckbox):
        '''
        class for placing checkbox to right of text
        '''
        pass

    class PriorityLabel(IRightBody, MDLabel):
        priority = NumericProperty()

        def change_priority_color(self, *args):
            # defines color as rgb
            colors = {
                0: [0, 0, 0, 0],        # no priority
                1: [0.1, 0.7, 1, 1],    # normal priority
                2: [1, 0.7, 0, 1],      # high priority
                3: [1, 0.15, 0, 1],     # very high priority
            }
            self.text_color = colors[self.priority]

    class RightMenuIconButtonHabit(IRightBodyTouch, MDIconButton):
        habit_instance = ObjectProperty()

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # content for menu
            habit_menu_items = [
                {"text": 'edit', },
                {'text': 'delete', }
            ]
            # created menu as dropdown menu
            self.habit_menu = MDDropdownMenu(
                caller=self,
                items=habit_menu_items,
                width_mult=2,
                selected_color=self.theme_cls.primary_dark_hue,
            )
            # pressing triggeres habit_menu_call
            self.habit_menu.bind(on_release=self.habit_menu_call)

        def habit_menu_call(self, instance_menu, instance_menu_item, *args):

            # for easier referencing of Habit (for delition, editing, ...)
            habit_instance = self.parent.parent
            habit_list_instance = self.parent.parent.parent

            # click delete
            if instance_menu_item.text == 'delete':
                self.habit_menu_delete(
                    instance_menu, habit_instance, habit_list_instance)

            # click edit
            elif instance_menu_item.text == 'edit':
                self.edit_habit_menu(instance_menu, habit_instance)

        def habit_menu_delete(self, menu_instance, habit_instance, habit_list_instance, *args):
            habit_list_instance.remove_widget(habit_instance)
            menu_instance.dismiss()

        def edit_habit_menu(self, menu_instance, habit_instance, *args):

            # task_instance needs to be parsed to self.change_habit (parsed function)
            self.show_habit_template(title='Change Habit', habit_instance=habit_instance, function=lambda *args: self.change_habit(habit_instance, template, priority_dict=priority_translation)
                                     )

            # reference to content of MDDialog
            template = self.dialog.content_cls

            # dictionary for convertion of priority as int (in Habit) and HabitTemplate.MDBoxLayout.priority_choice
            priority_translation = {
                '0': 'low',
                '1': 'normal',
                '2': 'high',
                '3': 'very high'
            }
            priority_key = str(len(habit_instance.ids.priority_id.text))

            # set habit attributes in HabitTemplate Widgets
            template.ids.habit_description.text = habit_instance.text

            # set priority chooser to value of priority in Habit
            template.ids.priority_choice.text = priority_translation[str(
                priority_key)]

            # set value for reminder days to value habit.secondary_text if not empty
            downed_keys = [item for item in habit_instance.secondary_text.split(
                ', ') if item not in [None, '', ' ']]
            for key in downed_keys:
                template.habit_repetition[str(key)] = 'down'

            # sets value for repetition times per day
            repetition = int(habit_instance.done_counter_max)
            template.ids.times_repetition.text = str(repetition)

            # set value for reminder days to value habit.tertiary_text if not empty
            times = [item for item in habit_instance.tertiary_text.split(
                ', ') if item not in [None, '', ' ']]
            for time in times:
                template.ids.reminder_list.add_widget(
                    template.Reminder(text=time)
                )

            # close HabitTemplate
            menu_instance.dismiss()

        def show_habit_template(self, title, habit_instance=None, function=None):
            self.dialog = None
            if not self.dialog:
                self.dialog = MDDialog(
                    title=str(title) + ':',
                    type="custom",
                    content_cls=HabitTemplate(habit_instance=habit_instance),
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            text_color=self.theme_cls.primary_color,
                            on_release=self.close_habit_template
                        ),
                        MDFlatButton(
                            text="SAVE",
                            text_color=self.theme_cls.primary_color,
                            on_release=(lambda *args: function())
                        ),
                    ],
                )
            # deactivated due to visible, not focused background after self.task_menu.dismiss()
            # self.dialog.set_normal_height()
            self.dialog.open()

        def close_habit_template(self, *args):
            self.dialog.dismiss()

        def change_habit(self, habit_instance, template, priority_dict, * args):

            # collect date from template
            description = template.ids.habit_description.text
            reminder_days = ', '.join([
                key for key, value in template.habit_repetition.items() if value == 'down'
            ])
            reminder_times = ', '.join(sorted(set([
                child.text for child in template.ids.reminder_list.children
            ])))
            new_priority = [key for key, value in priority_dict.items(
            ) if value == template.ids.priority_choice.text]
            repetition_times = int(template.ids.times_repetition.text)

            # update values of habit_instance
            habit_instance.text = str(description)
            habit_instance.secondary_text = str(reminder_days)
            habit_instance.tertiary_text = str(reminder_times)
            habit_instance.priority = str(new_priority[0])
            habit_instance.done_counter_max = int(repetition_times)

            # close HabitTemplate
            self.dialog.dismiss()

    class DoneCounter(IRightBody, MDLabel):
        pass


class ThreeLineHabit(ThreeLineAvatarListItem, BasicHabit):
    pass

# HabitTemplate
# -----------------------------------------------------------------


class HabitTemplate(MDBoxLayout):

    habit_instance = ObjectProperty()

    habit_repetition = DictProperty({
        'Mon': 'normal',
        'Tue': 'normal',
        'Wed': 'normal',
        'Thu': 'normal',
        'Fri': 'normal',
        'Sat': 'normal',
        'Sun': 'normal',
    })

    class MyToggleButton(MDRectangleFlatButton, MDToggleButton):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.background_down = self.theme_cls.primary_light
            self.text_color = self.theme_cls.primary_dark

        def toggle_habit_repetition(self, root, *args):
            root.habit_repetition[str(self.text)] = str(self.state)

    class Reminder(OneLineListItem):

        def self_removal(self, *args):
            self.parent.remove_widget(self)

        def change_reminder(self, *args):

            # sets default time for value of Reminder.text
            # if empty --> default time is now
            default_time = datetime.datetime.now() if self.text in [
                None, '', ' '] else datetime.datetime.strptime(self.text, '%H:%M')

            # open MDTimePicker preset to default_time
            time_dialog = MDTimePicker()
            time_dialog.set_time(default_time)
            time_dialog.open()
            time_dialog.bind(
                on_dismiss=lambda *args: self.update_reminder_time(
                    time_dialog.time)
            )

        def update_reminder_time(self, new_time, *args):
            if new_time not in [None, '', ' ']:
                self.text = f'{new_time:%H:%M}'

    class AddReminderButton(MDFlatButton):

        reminder_list_instance = ObjectProperty()
        root_instance = ObjectProperty()

        def add_reminder(self, *args):

            # sets default time to now
            default_time = datetime.datetime.now()

            # creates new Reminder with text of time from MDTimePicker
            def set_reminder_time(self, time, *args):
                if time not in [None, '', ' ']:
                    self.reminder_list_instance.add_widget(
                        self.root_instance.Reminder(text=f'{time:%H:%M}')
                    )

            # open MDTimePicker set to default_time
            time_dialog = MDTimePicker()
            time_dialog.set_time(default_time)
            time_dialog.open()
            time_dialog.bind(
                on_dismiss=lambda *args: set_reminder_time(
                    self, time_dialog.time)
            )
