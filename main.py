import arabic_reshaper
from bidi.algorithm import get_display
import math

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Line, Ellipse

# تنظیمات اولیه
Window.size = (800, 850)
Window.clearcolor = (0.06, 0.09, 0.15, 1)

FONT = "Vazirmatn-RD-UI-Regular.ttf"


def C(hex_color):
    from kivy.utils import get_color_from_hex
    return get_color_from_hex(hex_color)


# رسم دار و آدمک
class HangmanDrawing(Widget):

    def __init__(self, **kwargs):
        self.stage = 0
        super().__init__(**kwargs)
        self.bind(pos=self.redraw, size=self.redraw)
        self.redraw()

    def set_stage(self, stage):
        self.stage = max(0, min(6, stage))
        self.redraw()

    def redraw(self, *args):

        self.canvas.clear()

        x, y = self.pos
        w, h = self.size

        with self.canvas:

            Color(*C("#FFD700"))

            # پایه کوتاه‌تر
            Line(
                points=[
                    x + w * 0.34, y + h * 0.12,
                    x + w * 0.42, y + h * 0.12
                ],
                width=3
            )

            # ستون دار
            Line(
                points=[
                    x + w * 0.38, y + h * 0.12,
                    x + w * 0.38, y + h * 0.98
                ],
                width=3
            )

            # تیر بالایی کوتاه‌تر
            Line(
                points=[
                    x + w * 0.38, y + h * 0.98,
                    x + w * 0.48, y + h * 0.98
                ],
                width=3
            )

            # طناب
            Line(
                points=[
                    x + w * 0.48, y + h * 0.98,
                    x + w * 0.48, y + h * 0.68
                ],
                width=3
            )

            Color(*C("#F2F4F4"))

            center_x = x + w * 0.48
            head_y = y + h * 0.61
            radius = h * 0.065

            if self.stage >= 1:
                Line(
                    circle=(center_x, head_y, radius),
                    width=3
                )

            # بدن
            if self.stage >= 2:
                Line(
                    points=[
                        center_x, head_y - radius,
                        center_x, y + h * 0.39
                    ],
                    width=3
                )

            # دست چپ
            if self.stage >= 3:
                Line(
                    points=[
                        center_x, y + h * 0.52,
                        x + w * 0.44, y + h * 0.47
                    ],
                    width=3
                )

            # دست راست
            if self.stage >= 4:
                Line(
                    points=[
                        center_x, y + h * 0.52,
                        x + w * 0.52, y + h * 0.47
                    ],
                    width=3
                )

            # پای چپ
            if self.stage >= 5:
                Line(
                    points=[
                        center_x, y + h * 0.39,
                        x + w * 0.44, y + h * 0.31
                    ],
                    width=3
                )

            # پای راست
            if self.stage >= 6:
                Line(
                    points=[
                        center_x, y + h * 0.39,
                        x + w * 0.52, y + h * 0.31
                    ],
                    width=3
                )


class HangmanApp(App):

    title = "Hangman Game"

    def fa(self, text):
        return get_display(arabic_reshaper.reshape(text))

    def build(self):

        self.root_box = BoxLayout(
            orientation="vertical",
            padding=18,
            spacing=10
        )

        # عنوان
        self.heading = Label(
            text=self.fa("بازی هنگ من"),
            font_name=FONT,
            font_size=35,
            color=C("#FFD700"),size_hint_y=None,
            height=60
        )

        # ورودی کلمه
        self.word_input = TextInput(
            hint_text=self.fa("کلمه مورد نظر را وارد کن"),
            multiline=False,
            font_name=FONT,
            font_size=22,
            size_hint_y=None,
            height=50
        )

        # دکمه شروع
        self.start_button = Button(
            text=self.fa("شروع بازی"),
            font_name=FONT,
            font_size=24,
            size_hint_y=None,
            height=55,
            background_color=C("#2471A3"),
            background_normal=""
        )

        self.start_button.bind(on_press=self.start_game)

        # وضعیت بازی
        self.status = Label(
            text=self.fa("اول یک کلمه وارد کن"),
            font_name=FONT,
            font_size=22,
            size_hint_y=None,
            height=45
        )

        # تصویر دار و آدمک
        self.drawing = HangmanDrawing(
            size_hint_y=None,
            height=170
        )

        # نمایش سه خط اصلی
        self.word_label = Label(
            text="",
            font_name=FONT,
            font_size=30,
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=120
        )

        # حروف اشتباه
        self.wrong_label = Label(
            text="",
            font_name=FONT,
            font_size=20,
            size_hint_y=None,
            height=40
        )

        # ورودی حدس
        self.guess_input = TextInput(
            hint_text=self.fa("یک حرف یا کل کلمه را حدس بزن"),
            multiline=False,
            font_name=FONT,
            font_size=22,
            size_hint_y=None,
            height=50,
            disabled=True
        )

        # دکمه ثبت حدس
        self.guess_button = Button(
            text=self.fa("ثبت حدس"),
            font_name=FONT,
            font_size=24,
            size_hint_y=None,
            height=55,
            background_color=C("#2471A3"),
            background_normal="",
            disabled=True
        )

        self.guess_button.bind(on_press=self.guess)

        # دکمه بازی مجدد
        self.restart_button = Button(
            text=self.fa("بازی مجدد"),
            font_name=FONT,
            font_size=24,
            size_hint_y=None,
            height=55,
            background_color=C("#C0392B"),
            background_normal="",
            disabled=True
        )

        self.restart_button.bind(
            on_press=self.restart_game
        )

        # اضافه کردن اجزای صفحه
        self.root_box.add_widget(self.heading)
        self.root_box.add_widget(self.word_input)
        self.root_box.add_widget(self.start_button)
        self.root_box.add_widget(self.status)
        self.root_box.add_widget(self.drawing)
        self.root_box.add_widget(self.word_label)
        self.root_box.add_widget(self.wrong_label)
        self.root_box.add_widget(self.guess_input)
        self.root_box.add_widget(self.guess_button)
        self.root_box.add_widget(self.restart_button)

        self.game_started = False

        return self.root_box

    # شروع بازی
    def start_game(self, instance):

        self.word = self.word_input.text.strip().lower()

        if not self.word:
            self.status.text = self.fa(
                "لطفاً یک کلمه وارد کن"
            )
            return

        self.top = [" "] * len(self.word)
        self.middle = ["-"] * len(self.word)
        self.bottom = [" "] * len(self.word)

        self.chance = 2
        self.wrong = 0
        self.guessed_letters = set()

        self.game_started = True

        self.word_input.disabled = True
        self.start_button.disabled = True

        self.guess_input.disabled = False
        self.guess_button.disabled = False
        self.restart_button.disabled = True

        self.status.text = self.fa("بازی شروع شد!")

        self.update_screen()

    # ثبت حدس
    def guess(self, instance):

        if not self.game_started:
            return

        guess = self.guess_input.text.strip().lower()
        self.guess_input.text = ""

        if not guess:
            return

        # حدس کل کلمه
        if len(guess) == len(self.word):

            if guess == self.word:
                self.end_game(True)
                return

            self.chance -= 1

            if self.chance == 0:
                self.end_game(False)
                return

        # حدس یک حرف
        elif len(guess) == 1:

            if guess in self.guessed_letters:
                self.status.text = self.fa(
                    "این حرف را قبلاً حدس زده‌ای"
                )
                return

            self.guessed_letters.add(guess)

            flag = False

            for i in range(len(self.word)):

                if self.word[i] == guess:
                    self.top[i] = guess
                    flag = True

            if not flag:

                self.bottom[self.wrong] = guess
                self.wrong += 1

            if self.top == list(self.word):
                self.end_game(True)
                return

            if self.wrong >= len(self.word):
                self.end_game(False)
                return

        else:

            self.status.text = self.fa(
                "یک حرف یا کل کلمه را وارد کن"
            )
            return

        self.update_screen()

    # به روزرسانی نمایش
    def update_screen(self):

        top_text = "   ".join(self.top)
        middle_text = "   ".join(self.middle)
        bottom_text = "   ".join(self.bottom)

        self.word_label.text = (
            top_text + "\n" +
            middle_text + "\n" +
            bottom_text
        )

        wrong_letters = [
            x for x in self.bottom if x != " "
        ]

        self.wrong_label.text = (
            self.fa("حروف اشتباه:") +
            " " + "   ".join(wrong_letters)
        )

        # رسم تدریجی آدمک
        if len(self.word) > 0:
            stage = math.ceil(
                self.wrong * 6 / len(self.word)
            )
        else:
            stage = 0

        self.drawing.set_stage(stage)

        self.status.text = self.fa(
            f"فرصت حدس کلمه: {self.chance}"
        )

    # پایان بازی
    def end_game(self, won):

        self.game_started = False

        self.update_screen()

        if won:

            self.status.text = self.fa(
                "آفرین! برنده شدی"
            )

        else:

            self.status.text = self.fa(
                "باختی! کلمه این بود: " + self.word
            )

        self.guess_input.disabled = True
        self.guess_button.disabled = True

        self.restart_button.disabled = False

    # بازی مجدد
    def restart_game(self, instance):

        self.word_input.text = ""
        self.guess_input.text = ""

        self.word_input.disabled = False
        self.start_button.disabled = False

        self.guess_input.disabled = True
        self.guess_button.disabled = True

        self.restart_button.disabled = True

        self.word_label.text = ""
        self.wrong_label.text = ""

        self.drawing.set_stage(0)

        self.status.text = self.fa(
            "یک کلمه جدید وارد کن"
        )

        self.game_started = False


HangmanApp().run()