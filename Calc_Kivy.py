from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.config import Config
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 300)
Config.set('graphics', 'height', 380)

from kivy.core.window import Window
Window.clearcolor = (.8, .8, .8, 1)

import math
import cmath

class CalculatorApp(App):
    def build(self):
        self.numbers, self.count, self.temp, self.formula = [], 0, '', '0'
        self.is_complex = False

        bl = BoxLayout(orientation='vertical', padding=[3])
        gl_button = GridLayout(cols=5, spacing=3, size_hint=(1, .6))

        self.lbl = Label(text='0', font_size=26, halign='right', valign='bottom',
                            size_hint=(1, .4), text_size=(270, 380 * .36 - 10), color=[0, 0, 0, .7])
        bl.add_widget(self.lbl)

        gl_button.add_widget(Button(text='!', on_press=self.fact))
        gl_button.add_widget(Button(text='(', on_press=self.add_par))
        gl_button.add_widget(Button(text=')', on_press=self.add_par))
        gl_button.add_widget(Button(text='C', on_press=self.del_all))
        gl_button.add_widget(Button(text='DEL', on_press=self.del_one_symbol))

        gl_button.add_widget(Button(text='ⁿ√x', on_press=self.sqrt_n))
        gl_button.add_widget(Button(text='√', on_press=self.sqrt))
        gl_button.add_widget(Button(text='x²', on_press=self.power_2))
        gl_button.add_widget(Button(text='xⁿ', on_press=self.power))
        gl_button.add_widget(Button(text='÷', on_press=self.add_operation))

        gl_button.add_widget(Button(text='sin', on_press=self.sin))
        gl_button.add_widget(Button(text='1', on_press=self.add_num, background_color=[.6, .6, .6, 1], background_normal=''))
        gl_button.add_widget(Button(text='2', on_press=self.add_num, background_color=[.6, .6, .6, 1], background_normal=''))
        gl_button.add_widget(Button(text='3', on_press=self.add_num, background_color=[.6, .6, .6, 1], background_normal=''))
        gl_button.add_widget(Button(text='×', on_press=self.add_operation))

        gl_button.add_widget(Button(text='cos', on_press=self.cos))
        gl_button.add_widget(Button(text='4', on_press=self.add_num, background_color=[.6, .6, .6, 1], background_normal=''))
        gl_button.add_widget(Button(text='5', on_press=self.add_num, background_color=[.6, .6, .6, 1], background_normal=''))
        gl_button.add_widget(Button(text='6', on_press=self.add_num, background_color=[.6, .6, .6, 1], background_normal=''))
        gl_button.add_widget(Button(text='-', on_press=self.add_minus))

        gl_button.add_widget(Button(text='tg', on_press=self.tg))
        gl_button.add_widget(Button(text='7', on_press=self.add_num, background_color=[.6, .6, .6, 1], background_normal=''))
        gl_button.add_widget(Button(text='8', on_press=self.add_num, background_color=[.6, .6, .6, 1], background_normal=''))
        gl_button.add_widget(Button(text='9', on_press=self.add_num, background_color=[.6, .6, .6, 1], background_normal=''))
        gl_button.add_widget(Button(text='+', on_press=self.add_operation))

        gl_button.add_widget(Button(text='ctg', on_press=self.ctg))
        gl_button.add_widget(Button(text='+/-', on_press=self.plus_minus))
        gl_button.add_widget(Button(text='0', on_press=self.add_num, background_color=[.6, .6, .6, 1], background_normal=''))
        gl_button.add_widget(Button(text='.', on_press=self.add_float))
        gl_button.add_widget(Button(text='=', on_press=self.calc_result, background_color=[.9, .4, .3, 1], background_normal=''))

        bl.add_widget(gl_button)

        return bl

    def add_num(self, instance):
        if self.formula == '0':
            self.formula = ''
        if self.temp == '0':
            if self.formula[-1:] == '0':
                self.formula = self.formula[0:-1]
                self.temp = ''
        self.formula += str(instance.text)
        self.temp += str(instance.text)
        self.update_label()

    def add_minus(self, instance):
        if self.lbl.text != '0':
            self.formula = self.lbl.text
            self.ver_sign()
            self.formula += str(instance.text)
            self.update_label()
            self.temp = ''
        else:
            self.formula = ''
            self.ver_sign()
            self.formula += str(instance.text)
            self.temp += str(instance.text)
            self.update_label()
        if self.lbl.text[-1:-3:-1] == "-(":
            self.temp += str(instance.text)

    def add_operation(self, instance):
        self.formula = self.lbl.text
        self.ver_sign()
        self.formula += str(instance.text)
        self.update_label()
        self.temp = ''

    def add_float(self, instance):
        if not '.' in self.temp:
            self.formula = self.lbl.text
            self.formula += str(instance.text)
            self.temp += str(instance.text)
            self.update_label()

    def add_par(self, instance):
        if self.formula == '0':
            self.formula = ''
            self.temp = ''
        self.formula += str(instance.text)
        self.update_label()

    def plus_minus(self, instance):
        if self.lbl.text != '0' and self.temp != '':
            self.formula = self.lbl.text
            self.formula = self.formula[0:-len(self.temp)]
            self.temp = str(-float(self.temp))
            self.float_zero()
            self.formula += self.temp
            self.update_label()
        elif self.formula != '0' and self.temp != '':
            self.formula = str(-float(self.formula))
            self.temp = str(-float(self.temp))
            self.float_zero()
            self.float_zero_formula()
            self.update_label()

    def del_one_symbol(self, instance):
        digit, p = self.formula[-1:], '0123456789'
        self.formula = self.lbl.text[0:-1] or '0'
        if digit in p:
            self.temp = self.temp[0:-1] or ''
        self.update_label()

    def del_all(self, instance):
        self.formula = '0'
        self.temp = ''
        self.update_label()

    def power(self, instance):
        if self.lbl.text != '0':
            self.formula = self.lbl.text
            self.ver_sign()
            self.formula += '^'
            self.update_label()
            self.temp = ''
        else:
            self.formula = '0'
            self.update_label()

    def sqrt_n(self, instance):
        if self.lbl.text != '0':
            self.formula = self.lbl.text
            self.formula += '^(1÷'
            self.update_label()
            self.temp = ''
        else:
            self.formula = '0'
            self.update_label()

    def sin(self, instance):
        if self.lbl.text != '0':
            self.formula = self.lbl.text
        try:
            cop = str(self.temp)
            self.temp = str(round(math.sin(math.radians(float(self.temp))), 15))
            self.float_zero()
            if self.formula[-1:] == ')':
                self.formula = self.formula[0:-1]
            self.formula = self.formula[0:-len(cop)] + self.temp
            self.update_label()
            self.parentheses()
        except ValueError:
            self.lbl.text = 'Неверно введены данные!'
            self.formula = '0'
            self.temp = ''
        except OverflowError:
            self.lbl.text = 'Слишком большие данные'
            self.formula = '0'
            self.temp = ''

    def cos(self, instance):
        if self.lbl.text != '0':
            self.formula = self.lbl.text
        try:
            cop = str(self.temp)
            self.temp = str(round(math.cos(math.radians(float(self.temp))), 15))
            self.float_zero()
            if self.formula[-1:] == ')':
                self.formula = self.formula[0:-1]
            self.formula = self.formula[0:-len(cop)] + self.temp
            self.update_label()
            self.parentheses()
        except ValueError:
            self.lbl.text = 'Неверно введены данные!'
            self.formula = '0'
            self.temp = ''
        except OverflowError:
            self.lbl.text = 'Слишком большие данные'
            self.formula = '0'
            self.temp = ''

    def tg(self, instance):
        if self.lbl.text != '0':
            self.formula = self.lbl.text
        try:
            cop = self.temp
            self.temp = str(round(math.tan(math.radians(float(self.temp))), 15))
            self.float_zero()
            if self.formula[-1:] == ')':
                self.formula = self.formula[0:-1]
            self.formula = self.formula[0:-len(cop)] + self.temp
            self.update_label()
            self.parentheses()
        except ValueError:
            self.lbl.text = 'Неверно введены данные!'
            self.formula = '0'
            self.temp = ''
        except OverflowError:
            self.lbl.text = 'Слишком большие данные'
            self.formula = '0'
            self.temp = ''

    def ctg(self, instance):
        if self.lbl.text != '0':
            self.formula = self.lbl.text
        try:
            cop = self.temp
            self.temp = str(round(math.cos(math.radians(float(self.temp))) / math.sin(math.radians(float(self.temp))), 15))
            self.float_zero()
            if self.formula[-1:] == ')':
                self.formula = self.formula[0:-1]
            self.formula = self.formula[0:-len(cop)] + self.temp
            self.update_label()
            self.parentheses()
        except ValueError:
            self.lbl.text = 'Неверно введены данные!'
            self.formula = '0'
            self.temp = ''
        except OverflowError:
            self.lbl.text = 'Слишком большие данные'
            self.formula = '0'
            self.temp = ''

    def sqrt(self, instance):
        if self.lbl.text != '0':
            self.formula = self.lbl.text
        try:
            cop = self.temp
            print(cop)
            if int(cop) > 0:
                self.temp = str(round(math.sqrt(float(self.temp)), 15))
            else:
                self.temp = str(cmath.sqrt(int(cop)))
                print(self.temp)
                self.is_complex = True

            self.float_zero()
            if self.formula[-1:] == ')':
                self.formula = self.formula[0:-1]
            self.formula = self.formula[0:-len(cop)] + self.temp
            self.update_label()
            self.parentheses()
        except ValueError:
            self.lbl.text = 'Неверно введены данные!'
            self.formula = '0'
            self.temp = ''
        except OverflowError:
            self.lbl.text = 'Слишком большие данные'
            self.formula = '0'
            self.temp = ''

    def fact(self, instance):
        if self.lbl.text != '0':
            self.formula = self.lbl.text
        try:
            cop = self.temp
            self.temp = str(round(math.factorial(float(self.temp)), 15))
            self.float_zero()
            if self.formula[-1:] == ')':
                self.formula = self.formula[0:-1]
            self.formula = self.formula[0:-len(cop)] + self.temp
            self.update_label()
            self.parentheses()
        except ValueError:
            self.lbl.text = 'Неверно введены данные!'
            self.formula = '0'
            self.temp = ''
        except OverflowError:
            self.lbl.text = 'Слишком большие данные'
            self.formula = '0'
            self.temp = ''

    def power_2(self, instance):
        if self.lbl.text != '0':
            self.formula = self.lbl.text
        try:
            cop = self.temp
            self.temp = str(round(float(self.temp)**2, 15))
            self.float_zero()
            if self.formula[-1:] == ')':
                self.formula = self.formula[0:-1]
            self.formula = self.formula[0:-len(cop)] + self.temp
            self.update_label()
            self.parentheses()
        except ValueError:
            self.lbl.text = 'Неверно введены данные!'
            self.formula = '0'
            self.temp = ''
        except OverflowError:
            self.lbl.text = 'Слишком большие данные'
            self.formula = '0'
            self.temp = ''

    def ver_sign(self):
        str_o = '+-×÷^.'
        if self.formula[-1:] in str_o:
            self.formula = self.formula[0:-1]
            self.temp = self.temp[0:-1]

    def parentheses(self):
        stack = []
        for i in range(len(self.lbl.text)):
            if self.lbl.text[i] == '(':
                stack.append((self.lbl.text[i]))

            if self.lbl.text[i] == ')':
                if stack:
                    temp = stack.pop()
                else:
                    break
                if temp == '(' and self.lbl.text[i] == ')':
                    continue
        if stack:
            self.formula += ')'
            self.update_label()

    def change_sign(self):
        for i in self.lbl.text:
            if i == '^':
                self.lbl.text = self.lbl.text.replace(i, '**')
            elif i == '÷':
                self.lbl.text = self.lbl.text.replace(i, '/')
            elif i == '×':
                self.lbl.text = self.lbl.text.replace(i, '*')

    def float_zero(self):
        if self.is_complex:
            pass
        else:
            if math.floor(float(self.temp)) == float(self.temp):
                self.temp = str("%.0f" % float(self.temp))

    def float_zero_formula(self):
        if self.is_complex:
            pass
        else:
            if math.floor(float(self.formula)) == float(self.formula):
                self.formula = str("%.0f" % float(self.formula))

    def update_label(self):
        self.lbl.text = self.formula

    def calc_result(self, instance):
        try:
            self.parentheses()
            self.change_sign()
            if self.is_complex != True:
                self.formula = str(round(eval(self.lbl.text), 12))
            else:
                self.temp = cmath.sqrt(eval(self.lbl.text))
                self.formula = str(self.temp)
            self.float_zero_formula()
            self.update_label()
            self.is_complex = False
            self.temp = self.formula
            self.formula = '0'
        except ZeroDivisionError:
            self.lbl.text = 'Делить на ноль нельзя!'
            self.formula = '0'
            self.temp = ''
        except ValueError:
            self.lbl.text = 'Неверно введены данные!'
            self.formula = '0'
            self.temp = ''
        except SyntaxError:
            self.lbl.text = 'Неверно введены данные!'
            self.formula = '0'
            self.temp = ''
        except TypeError:
            self.lbl.text = 'Неверно введены данные!'
            self.formula = '0'
            self.temp = ''
        except OverflowError:
            self.lbl.text = 'Слишком большие данные'
            self.formula = '0'
            self.temp = ''


if __name__ == '__main__':
    CalculatorApp().run()