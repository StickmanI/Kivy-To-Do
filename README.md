# Kivy To Do
A small To-Do-List app with game-like features written in python and Kivy/KivyMD

## Motivation
I started this project to organize my goals, tasks and appointments.
Previously I used To-Do-List apps like [TickTick](https://www.ticktick.com/), [Notion](https://www.notion.so/) and [todoist](https://todoist.com/home) until I stumbled upon [Habitica](https://habitica.com/static/home).
I really liked the gaming aspect, but soon came to realize that I had to be constantly online to not miss my tasks.
Due to bad to no reception all the time around my home and most other To-Do-List apps lacking the game aspect, I decided to make my own To-Do-List app with python and Kivy.


## Requirements
- [Python 3.7+](https://www.python.org/downloads/)
- [Kivy 1.11.1+](https://kivy.org/doc/stable/gettingstarted/installation.html)
- [KivyMD v0.104.2.dev0](https://kivymd.readthedocs.io/en/0.104.1/getting-started.html)

---

## Features
- locally stored files
- application window position and size depending on values in config.ini
    ```
    config.ini
    ...
    [graphics]
    height = 1009   --> height application
    left = 1319     --> position app left border
                        (from upper left display corner)
    top = 30        --> position app top border
                        (from upper left display corner)
    width = 600     --> width application
    ...
    ```



- ### Tasks 
    - with or without due date
    - Task failed (due date reached) --> Enemy attacks Avatar
    - completed Tasks --> Avatar attacks Enemy
    
<img width="300" src="demo gifs\Tasks.gif">

- ### Habits
    - adjustable amount of repetition per day
    - can have any number of reminders (amount reminder is independent of amount of repetition per day)
    - repetition cycle per week
    - like Tasks, can hurt Enemy or Avatar
    - fails day after not completing habit
    - can also be completed on days outside repetition cycle
    - habits can be skipped on holidays (no damage to Avatar)

<img width="300" src="demo gifs\Habits.gif">

- ### Enemy
    - gets attacked by Avatar via finishing Tasks and Habits
    - can respawn and gets stronger
    - enemy picture random from files in /enemy_pictures
    - name corresponds to file name
- ### Avatar
    - gets hurt by not completing Habits or Tasks with due dates (Enemy attacks Avatar)
    - receives exp after defeating Enemy
        - can than level up and deal more damage
    - Avatar picture can be changed by click on Avatar (in Avatar tab)
    - Avatar name can be changed by click on Avatar name (next to picture or at stats page)
    - level decreases after too many tasks/habits not finished (by 0 health)
        - maximum health and attack decrease together with level

---

## Getting started
1. Download/Clone repository
2. Run KivyMD_To_Dp.py
3. Done


## Roadmap
- [ ] annoyance factor to motivate task/habit completion
- [ ] make available for other systems (currently only works on windows)
- [ ] themed background

## Changes in Versions
> ### *Version 1.0*
>- habits cannot fail on holidays
>- notification fixed (still needs testing)
>- priority affects damage received and dealt (high priority --> high damage)

## License
[MIT License](LICENSE)
