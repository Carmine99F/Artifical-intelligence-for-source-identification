import pyautogui
import config

class NumberSensorsInsufficient(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) :
        message="Il numero di centraline attive per il giorno {} è minore di 3".format(config.data)
        return message