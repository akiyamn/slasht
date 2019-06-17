import pyperclip


class Clipboard:

    def get_text(self):
        return pyperclip.paste()
