import cv2 as cv
import numpy as np
import os
import pyautogui
import time
import pydirectinput

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# image names
default_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
pnj_to_speak_img = 'pnj_to_speak_minimal.png'
quest_button_img = 'quest_button.png'
jouer_button_img = 'jouer_button.png'
fin_tour_button = 'fin_tour.png'
menu_button = 'menu_button.png'
abandoneer_button = 'abandonner_button.png'
confirm_abandon_button = 'confirm_abandon_button.png'

# spells image names
spell_eau_2          = 'spell_eau_2_minimal.png'
spell_eau_6          = 'spell_eau_6_minimal.png'
spell_feu_2          = 'spell_feu_2_minimal.png'
spell_feu_6          = 'spell_feu_6_minimal.png'
spell_terre_2        = 'spell_terre_2_minimal.png'
spell_terre_4        = 'spell_terre_4_minimal.png'
spell_vent_2         = 'spell_vent_2_minimal.png'
spell_vent_4         = 'spell_vent_4_minimal.png'
spell_fureur_kartana = 'spell_fureur_kartana_minimal.png'
deck = [spell_fureur_kartana, spell_vent_2, spell_vent_4, spell_terre_2, spell_terre_4, spell_feu_6, spell_eau_2,
        spell_eau_6, spell_feu_2]

# seconds to wait
enemy_turn = 15   # in seconds
wait_to_play = 7  # in seconds

# chack setup
board_setup = 0

# position on screen
start_position = {'x': 775, 'y': 659}
first_movement_end = {'x': 835, 'y': 566}
first_square = {'x': 963, 'y': 501}
second_square = {'x': 1026, 'y': 540}
third_square = {'x': 894, 'y': 533}
fourth_square = {'x': 960, 'y': 565}
last_square = {'x': 892, 'y': 469}


def detect(object_to_find):
    object_to_find_coordinates = pyautogui.locateOnScreen(default_path + object_to_find, confidence=0.9)
    if object_to_find_coordinates is None:
        return 0
    else :
        return 1


def detect_move_click(object_to_find, name):
    # get pnj coordinates
    object_to_find_coordinates = pyautogui.locateOnScreen(default_path + object_to_find, confidence=0.85)
    print('%s coordinates :' % name, object_to_find_coordinates)

    if object_to_find_coordinates is None:
        print('%s not found' % name)
        return 1

    # move mouse to pnj and click
    object_to_find_center = (object_to_find_coordinates.left + (object_to_find_coordinates.width / 2), object_to_find_coordinates.top + (object_to_find_coordinates.height / 2))
    print('%s center :' % name, object_to_find_center)
    pydirectinput.moveTo(int(object_to_find_center[0]), int(object_to_find_center[1]))
    time.sleep(.2)
    pydirectinput.mouseDown()
    time.sleep(.1)
    pydirectinput.mouseUp()
    time.sleep(0.5)
    return 0

def make_board():
    board_to_build = []
    for card in deck:
        detect_res = detect(card)
        if detect_res == 1:
            board_to_build.append(card)
    return board_to_build


def detect_board_setup_turns():
    global board_setup
    hand = make_board()
    print(hand)
    number_of_six = 0
    number_of_four = 0
    number_of_two = 0
    number_of_kartana = 0
    for card in hand:
        match card:
            case 'spell_eau_6_minimal.png':
                number_of_six = number_of_six + 1
            case 'spell_feu_6_minimal.png':
                number_of_six = number_of_six + 1
            case 'spell_eau_2_minimal.png':
                number_of_two = number_of_two + 1
            case 'spell_feu_2_minimal.png':
                number_of_two = number_of_two + 1
            case 'spell_terre_2_minimal.png':
                number_of_two = number_of_two + 1
            case 'spell_vent_2_minimal.png':
                number_of_two = number_of_two + 1
            case 'spell_terre_4_minimal.png':
                number_of_four = number_of_four + 1
            case 'spell_vent_4_minimal.png':
                number_of_four = number_of_four + 1
            case 'spell_fureur_kartana_minimal.png':
                number_of_kartana = number_of_kartana + 1
    print("6 :", number_of_six)
    print("4 :", number_of_four)
    print("2 :", number_of_two)
    print("kartana :", number_of_kartana)
    if number_of_six >= 1 and number_of_two >= 2 and number_of_kartana >= 1:
        board_setup = 1
        return 0
    elif number_of_four >= 1 and number_of_two >= 3 and number_of_kartana >= 1:
        board_setup = 1
        return 0
    elif number_of_two >= 4 and number_of_kartana >= 1:
        board_setup = 1
        return 0
    elif number_of_four >= 1 and number_of_two >= 3:
        return 1
    elif number_of_four >= 1 and number_of_two >= 2 and number_of_kartana >= 1:
        return 1
    elif number_of_six >= 1 and number_of_two >= 2 :
        return 1
    elif number_of_six >= 1 and number_of_two >= 1 and number_of_kartana >= 1 :
        return 1
    elif number_of_two >= 4:
        return 1
    elif number_of_two >= 3 and number_of_kartana >= 1:
        return 1
    else:
        return 2


def detect_second_setup():
    hand = make_board()
    number_of_two = 0
    number_of_kartana = 0
    for card in hand:
        match card:
            case 'spell_eau_2_minimal.png':
                number_of_two = number_of_two + 1
            case 'spell_feu_2_minimal.png':
                number_of_two = number_of_two + 1
            case 'spell_terre_2_minimal.png':
                number_of_two = number_of_two + 1
            case 'spell_vent_2_minimal.png':
                number_of_two = number_of_two + 1
            case 'spell_fureur_kartana_minimal.png':
                number_of_kartana = number_of_kartana + 1
    if number_of_two >= 2 and number_of_kartana >= 1:
        return 0
    else:
        return 1


def play_first_turn():
    # move character
    print("im here")
    print(int(start_position['x']))
    print(start_position['x'])
    pyautogui.moveTo(start_position['x'], start_position['y'])
    pyautogui.click()
    print("im here 2")
    pyautogui.dragTo(first_movement_end['x'], first_movement_end['y'], 1, button='left')
    print("im here 3")


def play_second_turn():
    print("second turn")


def launch_abandon():
    detect_move_click(menu_button, "menu button")
    time.sleep(.5)
    detect_move_click(abandoneer_button, "abandon_button")
    time.sleep(.5)
    detect_move_click(confirm_abandon_button, "oui button")
    time.sleep(4)


while True:
    # sleep to have waven screen selected
    time.sleep(5)

    res = detect_move_click(pnj_to_speak_img, "pnj")
    if res == 1:
        continue
    res = detect_move_click(quest_button_img, "quest button")
    if res == 1:
        continue
    res = detect_move_click(jouer_button_img, 'jouer button')
    if res == 1:
        continue
    time.sleep(wait_to_play)

    turn_to_setup = detect_board_setup_turns()
    print("turn to setup :", turn_to_setup)
    if turn_to_setup > 1:
        launch_abandon()
        continue
    play_first_turn()
    if board_setup != 1:
        setup = detect_second_setup()
        if setup != 0:
            launch_abandon()
            continue
    time.sleep(enemy_turn)
    play_second_turn()
    board_setup = 0
