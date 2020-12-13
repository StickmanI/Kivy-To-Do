from plyer import notification


def make_overview_notefication(notification_for, content, *args):
    """
    - calls notification with Description of Task or Habit
    Args:
        content (list): [content to be displayed as bullet list]
    """
    # makes bulleted list from list elements
    modified_content = '\n'.join(['• ' + str(item) for item in content])

    # creates notification
    notification.notify(
        title=f"Don't forget today's {notification_for}s",
        message=modified_content,
        timeout=7.5 * len(content),
        # app_icon=r'python.ico',
    )


def deadline_notification(title, next_notification, final_notification=False, *agrs):

    content = f'---------------------\nNext notification in {next_notification} minutes' if final_notification == False else '---------------------\nLast notification'

    notification.notify(
        title=str(title),
        message=content,
        # app_icon=r'python.ico',
    )


def normal_notification(title, *args):
    notification.notify(
        title=str(title),
        message=' ',
        # app_icon=r'python.ico',
    )
