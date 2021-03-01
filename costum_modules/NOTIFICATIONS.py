from os import stat
from plyer import notification
from kivy.clock import Clock
import datetime


class OverviewNotification:

    def __init__(self, content_notification):
        self.content = self.format_content(content_notification)
        self.title = f'Do not forget:\n'
        
        if len(content_notification) > 3:
            self.content = self.reduce_content_length(self.content)

        self.call_overview_notification()
        return None

    def format_content(self, unformated_content, *args):
        return '\n'.join(['• ' + str(item) for item in unformated_content])

    def reduce_content_length(self, text):
        items_in_content = text.split('\n')
        number_items_in_content = len(items_in_content)

        # +3 due to len not counting special character (bullet point)
        new_end_of_content = sum([len(item)
                                  for item in items_in_content[:3]], 3)
        number_items_cut_off = number_items_in_content - 3

        new_content = self.content[:new_end_of_content] + \
            f'+{number_items_cut_off} more tasks'
        return new_content

    def call_overview_notification(self):

        # too long notification content gets reduced
        # only <4 lines visible
        notification.notify(
            title=self.title,
            message=self.content,
            timeout=7.5 * len(self.content),
        )
        return None


class Notification:

    def __init__(self, text, notification_time, execute_after_notification=None, *args):

        # format notificaion_time = hour:minutes
        super().__init__()
        self.notification_text = text
        self.notification_time = self.string_to_datetime(notification_time)
        self.execute_after_notification = lambda *args: execute_after_notification(
        ) if execute_after_notification != None else None

        self.calculate_remaining_time()
        self.active = True if self.remaining_time is not None else False
        self.initiate_trigger()
        return None

    def string_to_datetime(self, datetime_as_string, *args):
        today = f'{datetime.datetime.now() :%d.%m.%Y}'
        time_today = ' '.join([today, datetime_as_string])
        return datetime.datetime.strptime(time_today, '%d.%m.%Y %H:%M')

    def calculate_remaining_time(self, offset=1, *args):

        # time now to compare to
        now = datetime.datetime.now()

        trigger_notification_time = (
            self.notification_time - now).total_seconds()
        state_check_time = (self.notification_time - now -
                            datetime.timedelta(minutes=offset)).total_seconds()

        # times in past not allowed
        trigger_notification_time = None if trigger_notification_time <= 0 else trigger_notification_time
        state_check_time = 0 if state_check_time <= 0 else state_check_time

        self.remaining_time = trigger_notification_time
        self.check_time = state_check_time

        return None

    def pre_notification_launch_test(self, *args):

        # prevents calling notification if remaining_time in past
        if self.active is True and self.remaining_time is not None:
            Clock.schedule_once(
                lambda *args: self.call_pyler_notification(
                    self.notification_text),
                self.remaining_time - self.check_time
            )            
        return None

    def initiate_trigger(self, *args):
        self.new_trigger(self.check_time)
        return None

    def new_trigger(self, time, *args):
        self.trigger = Clock.create_trigger(
            lambda *args: self.pre_notification_launch_test(),
            time
        )
        self.trigger()
        return None

    def stop(self, *args):
        self.trigger.cancel()
        return None

    def call_pyler_notification(self, text, *args):
        if self.active:
            notification.notify(
                title=str(text),
                message=' ',
                timeout=10,
            )
        self.deactivate()

        # executes function after notification if defined
        if self.execute_after_notification != None:
            self.execute_after_notification()
        return None

    def deactivate(self, *args):
        self.active = False
        self.stop()
        return None

    def reactivate(self, *args):
        self.active = True
        return None

    def __repr__(self):
        return f'text: {self.notification_text}, reminder time: {self.notification_time}, active?: {self.active}'
