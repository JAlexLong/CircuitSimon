import board # type: ignore
import random

from time import sleep, time
from digitalio import DigitalInOut, Direction, Pull # type: ignore

# configure buttons
red_button = DigitalInOut(board.GP13)
red_button.direction = Direction.INPUT
red_button.pull = Pull.UP

yellow_button = DigitalInOut(board.GP15)
yellow_button.direction = Direction.INPUT
yellow_button.pull = Pull.UP

green_button = DigitalInOut(board.GP18)
green_button.direction = Direction.INPUT
green_button.pull = Pull.UP

blue_button = DigitalInOut(board.GP16)
blue_button.direction = Direction.INPUT
blue_button.pull = Pull.UP

menu_button = DigitalInOut(board.GP20)
menu_button.direction = Direction.INPUT
menu_button.pull = Pull.UP

BUTTONS = {'red': red_button,
           'yellow': yellow_button,
           'green': green_button,
           'blue': blue_button,
           'menu': menu_button,
           }

# configure LEDs
red_led = DigitalInOut(board.GP7)
red_led.direction = Direction.OUTPUT

yellow_led = DigitalInOut(board.GP9)
yellow_led.direction = Direction.OUTPUT

green_led = DigitalInOut(board.GP26)
green_led.direction = Direction.OUTPUT

blue_led = DigitalInOut(board.GP22)
blue_led.direction = Direction.OUTPUT

menu_led = DigitalInOut(board.GP11)
menu_led.direction = Direction.OUTPUT

power_led = DigitalInOut(board.LED)
power_led.direction = Direction.OUTPUT

LEDS = {'red': red_led,
        'yellow': yellow_led,
        'green': green_led,
        'blue': blue_led,
        'menu': menu_led,
        'power': power_led,
        }


class SimonGame():
    def __init__(self):
        self.colors = ['red', 'green', 'yellow', 'blue']
        self.score = 0
        self.pattern = []
        self.playing = False

    def start(self):
        self.reset()
        self.grow_pattern(3)
        self.play()

    def reset(self):
        self.blink_all()
        self.pattern = []

    def play(self):
        self.playing = True
        while self.playing:
            self.grow_pattern()
            self.show_pattern()
            self.guess_pattern()

    def blink(self, led, interval=.5):
        if led in LEDS:
            LEDS[led].value = True
            sleep(interval)
            LEDS[led].value = False
            sleep(interval)

    def blink_all(self, blinks=3, interval=.2):
        for i in range(blinks):
            red_led.value = True
            yellow_led.value = True
            green_led.value = True
            blue_led.value = True
            menu_led.value = True
            sleep(interval)
            red_led.value = False
            yellow_led.value = False
            green_led.value = False
            blue_led.value = False
            menu_led.value = False
            sleep(interval)

    def grow_pattern(self, iterations=1):
        for i in range(iterations):
            new_color = random.choice(self.colors)
            self.pattern.append(new_color)

    def show_pattern(self):
        for color in self.pattern:
            self.blink(color)

    def show_pattern(self):
        self.blink_all(blinks=self.score, interval=.1)
        self.reset()

    def guess_pattern_old(self):
        temp_pattern = self.pattern.copy()
        while len(temp_pattern) > 0:
            next_color = temp_pattern[0]
            # if they want to start over
            if not BUTTONS['menu'].value:
                self.start()
            # if they guess correctly
            elif not BUTTONS[next_color].value:
                self.blink(next_color, interval=.2)
                temp_pattern.pop(0)

        self.score += 1

    def guess_pattern(self):
        temp_pattern = self.pattern.copy()
        #while len(temp_pattern) > 0:
        #    for


# mainloop
def main():
    game = SimonGame()
    while True:
        # button values are False while being pressed down,
        # which is backward from LED values.
        # Wait for player to press menu button before starting the game
        if not menu_button.value:
            break
    game.start()


if __name__ == "__main__":
    start = time()
    main()
    end = time()
    total = end - start
    print(f"Played game for {total} seconds.")
