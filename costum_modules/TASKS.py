# imports
# -----------------------------------------------------------------

import sys
from costum_modules.HOLIDAYS import *

from costum_modules.NOTIFICATIONS import *
from kivy.lang import Builder
from kivy.properties import ObjectProperty, OptionProperty, StringProperty, NumericProperty, ListProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDFloatingBottomButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (BaseListItem, ContainerSupport, IRightBody,
                             IRightBodyTouch, OneLineAvatarListItem, OneLineListItem, TwoLineAvatarListItem)
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import MDDropDownItem

from kivymd.color_definitions import colors
from kivy.clock import Clock
import datetime
import json
from kivymd.toast import toast

from kivymd.uix.picker import MDDatePicker, MDTimePicker


sys.path.append(
    r'C:\Users\Jens\Desktop\Programming\Python\Task_Game_kivy_with_custom_modules')

# -----------------------------------------------------------------


Builder.load_string('''
#<KvLang>
# TaskView
# ---------------------------------------------------
<TaskView>:
    ScrollView:
        adaptive_height: True
        size_hint_x: 0.86
        pos_hint: {'x': 0.05}

        MDList:
            id: task_list
    
    AddTaskButton:
        icon: 'plus'
        md_bg_color: app.theme_cls.primary_dark
        pos_hint: {'center_x': 0.95, 'center_y': 0.05}
        on_press: self.show_task_template(title='Create Task')

# TaskTemplate
# ---------------------------------------------------
<TaskTemplate>:
    adaptive_height: True
    orientation: 'vertical'
    padding: 15, 0
    
    MDTextField:
        id: task_description
        hint_text: 'Task Description'
        max_text_length: 30
        
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
    
    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        padding: 0, 35
        
        MDLabel:
            text: 'Due Date and Time:'
        
        MDBoxLayout:
            orientation: 'horizontal'
            adaptive_height: True
            size_hint_x: 0.45
        
            DueDate:
                id: due_date_time_task
                theme_text_color: 'Custom'
                text_color: self.theme_cls.primary_color
                on_press: self.choose_due_date()
            
            MDIconButton:
                icon: 'window-close'
                size_hint_x: None
                width: dp(50)
                on_press:
                    due_date_time_task.text = ''


# Task
# ---------------------------------------------------
<BasicTask>:
    theme_text_color: 'Custom'
    text_color: root.theme_cls.primary_color
    font_style: 'H6'
    text: self.description
    
    LeftCheckbox:
        state: root.check_state
        on_state:
            root.check_state = self.state
    
    MDBoxLayout:
        id: _right_container
        size_hint: None, None
        x: root.width - len(self.children) * self.width
        y: root.y + root.height/2 - self.height/2
        size: dp(48), dp(48)
        
        PriorityLabel:
            id: priority_id
            priority: int(root.priority)
    
        RightMenuIconButton:
            task_instance: root

<LeftCheckbox@ILeftBodyTouch+MDCheckbox>:

<PriorityLabel>:
    text: '!' * self.priority
    font_size: 26
    theme_text_color: 'Custom'
    size_hint: None, None
    size: dp(50), dp(48)
    on_priority: self.change_priority_color()

<RightMenuIconButton>:
    icon: 'dots-vertical'
    on_press: self.task_menu.open()
    
<TwoLineTask>:
    secondary_text: self.due_date
    
    
#</KvLang>
''')

# TaskView
# ---------------------------------------------------


class TaskView(MDFloatLayout):

    opponent = ObjectProperty()
    avatar = ObjectProperty()

    attribute_list = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attribute_list = [
            attribute for attribute in [
                'description',
                'due_date',
                'priority',
            ]
        ]

        # calling notifications
        Clock.schedule_interval(self.call_overview_notification, 3600)
        return None

    def add_task(self, *args, description='', due_date='', priority='0', index=0):

        # add task with due date
        if due_date not in [None, '', ' ']:
            self.ids.task_list.add_widget(
                TwoLineTask(
                    description=description,
                    due_date=due_date,
                    priority=priority,
                    opponent=self.opponent,
                    avatar=self.avatar,
                ), index
            )

        # add task without due date
        else:
            self.ids.task_list.add_widget(
                OneLineTask(
                    description=description,
                    priority=priority,
                    opponent=self.opponent,
                    avatar=self.avatar,
                ), index
            )
        return None

    def save_tasks(self, *args):
        # collect infos for each habit
        # format: [
        #   {attribute 1: value 1, ...},    (Habit 1)
        #   {attribute 1: value 1, ...},    (Habit 2)
        #   ...
        # ]
        saved_tasks = [
            {
                attribute: getattr(child, str(attribute))
                for attribute in self.attribute_list
            }
            for child in self.ids.task_list.children[::-1]
        ]

        with open(r'saves/save_tasks.json', 'w') as file:
            json.dump(saved_tasks, file, indent=4)
        return None

    def load_tasks(self, *args):
        try:
            # loads tasks from save file
            with open(r'saves/save_tasks.json', 'r') as file:
                data_saved_tasks = json.load(file)

            # creates task instances form content of save file
            for task in data_saved_tasks:
                self.add_task(
                    description=str(task['description']),
                    due_date=str(task['due_date']),
                    priority=str(task['priority']),
                )

        except IOError:
            pass
        return None

    def call_overview_notification(self, *args):
        content = [
            child.description for child in self.ids.task_list.children[::-1]]

        if len(content) > 0:
            self.new_overview_notification(content)
        return None

    def new_overview_notification(self, notification_content, *args):
        return OverviewNotification(notification_content)

    def switch_task_type(self, description='', due_date='', priority='0', index=0, *args):
        task_list = self.children[1].children[0].children

        # removes old task
        task_list[index].self_removal()

        # adds new task at same position
        self.add_task(
            description=description,
            due_date=due_date,
            priority=priority,
            index=index
        )
        return None

    class AddTaskButton(MDFloatingBottomButton):

        def show_task_template(self, title):
            self.dialog = None
            if not self.dialog:
                self.dialog = MDDialog(
                    title=str(title) + ':',
                    type="custom",
                    content_cls=TaskTemplate(),
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            text_color=self.theme_cls.primary_color,
                            on_release=self.close_task_template
                        ),
                        MDFlatButton(
                            text="SAVE",
                            text_color=self.theme_cls.primary_color,
                            on_release=(lambda *args: self.create_task())
                        ),
                    ],
                )
            self.dialog.open()

        def close_task_template(self, *args):
            self.dialog.dismiss()

        def create_task(self, *args):

            # geting values for description, priority and due_date
            description = self.dialog.content_cls.ids.task_description.text
            due_date = self.dialog.content_cls.ids.due_date_time_task.text

            # get priority as text from priority_choice ---> into string of number
            priority_translation = {
                '0': 'low',
                '1': 'normal',
                '2': 'high',
                '3': 'very high'
            }
            priority = [key for key, item in priority_translation.items() if item ==
                        self.dialog.content_cls.ids.priority_choice.text][0]

            # create new task if description is not empty
            if description not in [None, '', ' ']:
                self.parent.add_task(
                    description=description,
                    due_date=due_date,
                    priority=priority,
                )

                # close TaskTemplate
                self.close_task_template()
            else:

                # reminds user to fill in task description
                toast("No Description?", duration=3.5)


# TaskTemplate
# ---------------------------------------------------
class TaskTemplate(MDBoxLayout):

    task_instance = ObjectProperty()

    class PriorityChooser(MDDropDownItem):

        primary_color_hex = StringProperty()

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            # set primary color
            self.primary_color_hex = colors[self.theme_cls.primary_palette][self.theme_cls.primary_hue]

            # content for menu
            priority_menu_items = [
                {'text': f'[color={self.primary_color_hex}] low [/color]', },
                {'text': f'[color={self.primary_color_hex}] normal [/color]', },
                {'text': f'[color={self.primary_color_hex}] high [/color]'},
                {'text': f'[color={self.primary_color_hex}] very high [/color]'}
            ]

            # created menu as dropdown menu
            self.priority_menu = MDDropdownMenu(
                caller=self,
                items=priority_menu_items,
                width_mult=2.5,
                selected_color=self.theme_cls.primary_dark_hue,
            )

            # pressing triggeres task_menu_call
            self.priority_menu.bind(on_release=self.priority_menu_call)

        def priority_menu_call(self, instance_menu, instance_menu_item, *args):

            # change MDDropDownItem text to chosen priority
            # additional code for color removed via rstrip and slicing
            self.text = instance_menu_item.text.rstrip('[/color]')[15:-1]
            self.priority_menu.dismiss()

        def on_text(self, instance, value):

            # sets text of label to value with primary color as text_color
            self.ids.label_item.text = value
            self.ids.label_item.color = self.theme_cls.primary_color

    class DueDate(OneLineListItem):

        def choose_due_date(self, *args):

            # default_date is date from task.secondary_text (first part / date-part)
            due_date = '' if self.text in [None, '', ' '] else self.text.split(' ')[
                0]
            default_date = datetime.datetime.today() if due_date in [
                None, '', ' '] else datetime.datetime.strptime(due_date, '%d.%m.%Y')

            # open MDDatePicker set to default_date
            date_dialog = MDDatePicker(
                callback=lambda date, *args: self.choose_due_time(date),
                year=default_date.year,
                month=default_date.month,
                day=default_date.day,
            )
            date_dialog.open()

        def choose_due_time(self, date, *args):

            # define default_time from task.secondary_text (second part / time-part)
            due_time = '' if self.text in [None, '', ' '] else self.text.split(' ')[
                1]
            default_time = datetime.datetime.now() if due_time in [
                None, '', ' '] else datetime.datetime.strptime(due_time, '%H:%M')

            # setting Task.due_date to values from MDDatePicker and MDTimePicker
            def set_due_date_time(self, date, time, *args):
                if all([date != None, time != None]):
                    due_date_time = ' '.join(
                        [f'{date:%d.%m.%Y}', f'{time:%H:%M}'])
                    self.text = due_date_time

            # open MDTimePicker preset to default_time
            time_dialog = MDTimePicker()
            time_dialog.set_time(default_time)
            time_dialog.open()
            time_dialog.bind(
                on_dismiss=lambda *args: set_due_date_time(
                    self, date, time_dialog.time)
            )


# Task
# ---------------------------------------------------
class BasicTask(ContainerSupport, BaseListItem):

    opponent = ObjectProperty()
    avatar = ObjectProperty()

    # check_state linked to checkbox
    # checked --> Task is done
    check_state = OptionProperty("normal", options=["normal", "down"])

    description = StringProperty('')
    due_date = StringProperty('')
    priority = OptionProperty("1", options=[
        '0',    # no
        '1',    # normal
        '2',    # high
        '3',    # very high
    ])

    _no_ripple_effect = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.create_fail_notification()

        self.bind(
            text=lambda *args: self.update_fail_notification(),
            secondary_text=lambda *args: self.update_fail_notification(),
            tertiary_text=lambda *args: self.update_fail_notification(),
        )

    def self_removal(self, *args):
        self.parent.remove_widget(self)

    def is_today_normal_day(self, *args):
        calender = MyCalender()
        today = datetime.datetime.today()

        return True if f'{today :%d.%m}' not in calender.holidays else False

    def create_fail_notification(self, *args):

        # no notifications on holidays
        # only tasks with due_date can have fail notifications
        if self.is_today_normal_day() and len(self.secondary_text) > 0:

            due_date, due_time = self.secondary_text.split(' ')

            if due_date == f'{datetime.datetime.today() :%d.%m.%Y}':

                # creates list of notification objects (rest done by object)
                failure_text = 'You failed:\n'
                self.notification_list = [
                    Notification(failure_text + self.text, due_time,
                                 execute_after_notification=self.fail_task)
                ]
        return None

    def update_fail_notification(self, *args):

        # overrides old notifications --> therefore no error by deleting or adding notifications
        self.create_fail_notification()

        return None

    def fail_task(self, *args):

        # avatar receives damage
        self.avatar.get_hit(
            int((1 + 0.1 * int(self.priority)) * self.opponent.attack)
        )

        # remove task
        self.self_removal()

        return None

    def on_check_state(self, *args):
        if self.check_state == 'down':

            # done task --> damage enemy
            self.opponent.get_hit(
                int((1 + 0.1 * int(self.priority)) * self.opponent.attack)
            )

            # delete task
            self.self_removal()

        return None

    def find_task_index_in_TaskView(self, *args):
        task_list = self.parent.children
        index_task = task_list.index(self)
        return index_task

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

    class RightMenuIconButton(IRightBodyTouch, MDIconButton):

        task_instance = ObjectProperty()

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # content for menu
            task_menu_items = [
                {"text": 'edit', },
                {'text': 'delete', }
            ]
            # created menu as dropdown menu
            self.task_menu = MDDropdownMenu(
                caller=self,
                items=task_menu_items,
                width_mult=2,
                selected_color=self.theme_cls.primary_dark_hue,
            )
            # pressing triggeres task_menu_call
            self.task_menu.bind(on_release=self.task_menu_call)

        def task_menu_call(self, instance_menu, instance_menu_item, *args):
            # for easier referencing of Task (for delition, editing, ...)
            task_instance = self.parent.parent
            list_instance = self.parent.parent.parent

            # click delete
            if instance_menu_item.text == 'delete':
                self.task_menu_delete(
                    instance_menu, task_instance, list_instance)

            # click edit
            elif instance_menu_item.text == 'edit':
                self.edit_task_menu(menu_instance=instance_menu,
                                    task_instance=task_instance)

        def task_menu_delete(self, menu_instance, task_instance, list_instance, *args):
            list_instance.remove_widget(task_instance)
            menu_instance.dismiss()

        def edit_task_menu(self, menu_instance, task_instance, *args):
            # task_instance needs to be parsed to self.change_task (parsed function)
            self.show_task_template(title='Change Task', task_instance=task_instance,
                                    function=lambda *args: self.change_task(
                                        task_instance, template, priority_dict=priority_translation)
                                    )
            # reference to content of MDDialog
            template = self.dialog.content_cls.ids

            # dictionary for convertion of priority as int (in Task) and TaskTemplate.MDBoxLayout.priority_choice
            priority_translation = {
                '0': 'low',
                '1': 'normal',
                '2': 'high',
                '3': 'very high'
            }
            priority_key = str(len(task_instance.ids.priority_id.text))

            # set task attributes in TaskTemplate Widgets
            template.task_description.text = task_instance.description

            # set priority chooser to value of priority in Task
            template.priority_choice.text = priority_translation[str(
                priority_key)]

            # set value for due date to value Task.due_date
            template.due_date_time_task.text = task_instance.due_date

            # close TaskTemplate
            menu_instance.dismiss()
            return None

        def show_task_template(self, title, task_instance=None, function=None):
            self.dialog = None
            if not self.dialog:
                self.dialog = MDDialog(
                    title=str(title) + ':',
                    type="custom",
                    content_cls=TaskTemplate(task_instance=task_instance),
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            text_color=self.theme_cls.primary_color,
                            on_release=self.close_task_template
                        ),
                        MDFlatButton(
                            text="SAVE",
                            text_color=self.theme_cls.primary_color,
                            on_release=(lambda *args: function())
                        ),
                    ],
                )
            self.dialog.open()

        def close_task_template(self, *args):
            self.dialog.dismiss()

        def change_task(self, task_instance, template, priority_dict, * args):

            # update task description
            task_instance.description = template.task_description.text

            # update task priority
            new_priority = [key for key, item in priority_dict.items(
            ) if item == template.priority_choice.text][0]
            task_instance.priority = new_priority

            # update due date
            task_instance.due_date = template.due_date_time_task.text

            # get index of old taks
            task_index = task_instance.find_task_index_in_TaskView()

            # replace old task with new one
            # OnelineTask or TwolineTask depending on due_date
            # automaticly removes old task
            task_list = task_instance.parent.parent.parent
            task_list.switch_task_type(
                description=task_instance.description,
                due_date=task_instance.due_date,
                priority=new_priority,
                index=task_index
            )

            # closes TaskTemplate
            self.dialog.dismiss()
            return None


class OneLineTask(OneLineAvatarListItem, BasicTask):
    pass


class TwoLineTask(TwoLineAvatarListItem, BasicTask):
    pass
