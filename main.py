import random

from kivy.app import App
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from colors import allcolors, favcolors #, somecolors

class MainApp(App):

    def build(self):
        self.title = 'Adaptive UI'
        self.shift_padding = 20
        self.root = BoxLayout(orientation="vertical", padding=10)  #,size_hint_y=None)
        hor = BoxLayout(orientation="horizontal", padding=10, spacing=10,size_hint_y=None)  # ,size_hint=(None, None))
        text = ["left","right","top","bottom"]
        for i in range(4):
            hor.add_widget(ToggleButton(size_hint_y=None, height='48dp', text=text[i], state="down" if i % 2 != 0 else "normal", group="g1" if i < 2 else "g2",on_release=self.on_toggle_click))
        self.root.add_widget(hor)
        self.hor_shift = "right"; self.ver_shift = "bottom"
        self.topcol = 0; self.toprow = 0
        self.rows = 5; self.cols = 5
        for i in range(self.rows):
            hor = BoxLayout(orientation="horizontal", padding=10, spacing=10) #,size_hint=(None, None))
            for i in range(self.cols):
                btn = Button(
                    text="0",background_color=random.choice(allcolors)) #size=(200, 50),size_hint=(None, None))
                btn.bind(on_press=self.on_btn_click)
                hor.add_widget(btn)
            self.root.add_widget(hor)
        return self.root

    def on_toggle_click(self, instance):
        if instance.group == 'g1': self.hor_shift = instance.text
        else: self.ver_shift = instance.text
        instance.state="down"
        self.topcol = 0 if self.hor_shift == "right" else self.cols - 1
        self.toprow = 0 if self.ver_shift == "bottom" else self.rows - 1
        #self.show_popup((instance.text).upper(), "Shift adapt")

    def on_btn_click(self, instance):
        freq = int(instance.text) + 1
        if freq % 3 == 0:
            self.adapt_ui(instance, freq)
        instance.text = str(freq)

    def swap_top_col(self, freq):
        maxfreq = 0;
        for r in range(self.rows):
            f = int(self.root.children[r].children[self.topcol].text)
            if f>maxfreq: maxfreq=f
        return True if freq>maxfreq else False

    def swap_top_row(self, freq, row):
        maxfreq = 0;
        for c in range(self.cols):
            f = int(self.root.children[row].children[c].text)
            if f>maxfreq: maxfreq = f
        return True if freq > maxfreq else False

    def swap_row(self, freq, row):
        if self.hor_shift == "left":
            col_start = self.cols - 1
            col_end = 0
            step = -1
        else:
            col_start = 0
            col_end = self.cols - 1
            step = 1
        for c in range(col_start, col_end, step):
            f = int(self.root.children[row].children[c].text)
            if freq > f: break
        return c

    def adapt_ui(self, instance, freq):
        adapt = False
        row, col = self.get_idx_children(instance)
        pos_x = instance.x; pos_y = instance.y
        anim = Animation(pos=(instance.x, instance.y), t='out_bounce')
        if row >= 0 and col >= 0:
            # Row adapt
            if self.swap_top_row(freq,row):
                adapt = True
                self.root.children[row].children[col] = self.root.children[row].children[self.topcol]
                self.root.children[row].children[self.topcol] = instance
                pos_x = self.animate_row(instance,anim)

            # Column adapt
            if self.swap_top_col(freq):
                adapt = True
                self.root.children[row].children[self.topcol] = self.root.children[self.toprow].children[self.topcol]
                self.root.children[self.toprow].children[self.topcol] = instance
                pos_y = self.animate_col(instance, anim)

            if not(adapt) and col != self.topcol:
                to_pos_col = self.swap_row(freq,row)
                if col != to_pos_col:
                    self.root.children[row].children[col] = self.root.children[row].children[to_pos_col]
                    self.root.children[row].children[to_pos_col] = instance

        if adapt:
            anim += Animation(pos=(pos_x, pos_y), t='out_bounce', d=1)
            anim.start(instance)
            #instance.background_color = random.choice(favcolors)

    def get_idx_children(self, instance):
        row = -1; col = -1
        for child in self.root.children:
            row += 1
            if len(child.children)>0:
                try: col = child.children.index(instance)
                except: col = -1
                if col >= 0:
                    break
        return row, col

    def animate_row(self, instance, anim):
        if self.hor_shift == "right":
            pos_x = Window.width - instance.width - self.shift_padding
        else:
            pos_x = self.shift_padding
        return pos_x

    def animate_col(self, instance, anim):
        if self.ver_shift == "bottom":
            pos_y = self.shift_padding
        else:
            pos_y = instance.height*(self.rows-1)+self.shift_padding*self.rows
        return pos_y

    def show_popup(self, text="", title="Popup Window"):
        popup = Popup(title=title, size_hint=(None, None),
                      size=(Window.width / 2, Window.height / 4))
        layout = BoxLayout(orientation="vertical", padding=10)
        layout.add_widget(Label(text=text))
        layout.add_widget(Button(text="OK",on_press=popup.dismiss))
        popup.content = layout
        popup.open()

if __name__ == "__main__":
    app = MainApp()
    #app.show_popup("The frequency of clicks adapts the interface", "Info")
    app.run()
