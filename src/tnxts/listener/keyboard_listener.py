from pynput import keyboard
from PyQt5.QtCore import QThread

from src.tnxts.listener import _global_signal
from src.tnxts.util import _general_logger

class KeyboardListener(keyboard.Listener):
    """键盘监听器

    """
    def __init__(self):
        super().__init__(on_press= self.on_press,on_release= self.on_release)
        self.press_keys = set()

    
    def on_press(self, key):
        try:

            self.press_keys.add(key)
            if key.char in key_dict.keys():
                if key_dict[key.char] == ['ctrl','v']:
                    _global_signal.paste.emit("0")
                elif key_dict[key.char] == ['ctrl','c']:
                    _global_signal.copy.emit("0")
            # print('按键 {0} 被按下了。'.format(key.char))

        except AttributeError:
            pass
            # print('特殊按键 {0} 被按下了。'.format(key))
    def on_release(self, key):
        if key in self.press_keys:
            self.press_keys.remove(key)



class KeyboardListenerThread(QThread):
    def __init__(self):
        super(KeyboardListenerThread, self).__init__()

    
    def run(self) -> None:
        _keyboard_listener.start()
        _keyboard_listener.join()


_keyboard_listener = KeyboardListener()
_keyboard_thread = KeyboardListenerThread()

key_dict = {
    '\x01': ['ctrl', 'a'],
    '\x02': ['ctrl', 'b'],
    '\x03': ['ctrl', 'c'],
    '\x04': ['ctrl', 'd'],
    '\x05': ['ctrl', 'e'],
    '\x06': ['ctrl', 'f'],
    '\x07': ['ctrl', 'g'],
    '\x08': ['ctrl', 'h'],
    '\t': ['ctrl', 'i'],
    '\n': ['ctrl', 'j'],
    '\x0b': ['ctrl', 'k'],
    '\x0c': ['ctrl', 'l'],
    '\r': ['ctrl', 'm'],
    '\x0e': ['ctrl', 'n'],
    '\x0f': ['ctrl', 'o'],
    '\x10': ['ctrl', 'p'],
    '\x11': ['ctrl', 'q'],
    '\x12': ['ctrl', 'r'],
    '\x13': ['ctrl', 's'],
    '\x14': ['ctrl', 't'],
    '\x15': ['ctrl', 'u'],
    '\x16': ['ctrl', 'v'],
    '\x17': ['ctrl', 'w'],
    '\x18': ['ctrl', 'x'],
    '\x19': ['ctrl', 'y'],
    '\x1a': ['ctrl', 'z'],
    '\x1f': ['ctrl', 'shift', '-'],
    '<186>': ['ctrl', ';'],
    '<187>': ['ctrl', '='],
    '<189>': ['ctrl', '-'],
    '<192>': ['ctrl', '`'],
    '<222>': ['ctrl', "'"],
    '<48>': ['ctrl', '0'],
    '<49>': ['ctrl', '1'],
    '<50>': ['ctrl', '2'],
    '<51>': ['ctrl', '3'],
    '<52>': ['ctrl', '4'],
    '<53>': ['ctrl', '5'],
    '<54>': ['ctrl', '6'],
    '<55>': ['ctrl', '7'],
    '<56>': ['ctrl', '8'],
    '<57>': ['ctrl', '9'],
    '~': ['shift', '`'],
    '!': ['shift', '1'],
    '@': ['shift', '2'],
    '#': ['shift', '3'],
    '$': ['shift', '4'],
    '%': ['shift', '5'],
    '^': ['shift', '6'],
    '*': ['shift', '7'],
    '(': ['shift', '8'],
    ')': ['shift', '9'],
    '_': ['shift', '-'],
    '+': ['shift', '='],
    ':': ['shift', ';'],
    '\"': ['shift', "'"],
    '<': ['shift', ","],
    '{': ['shift', "["],
    '}': ['shift', "]"],
    '|': ['shift', "\\"],
    '?': ['shift', "/"],
}