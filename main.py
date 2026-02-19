import threading
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

def start_server():
    import sys
    sys.path.insert(0, '.')
    from server import run
    run()

class VervainApp(App):
    def build(self):
        Window.clearcolor = (0.01, 0.04, 0.03, 1)
        threading.Thread(target=start_server, daemon=True).start()
        layout = AnchorLayout()
        self.lbl = Label(
            text='[b]VERVAIN[/b]\nBaslatiliyor...',
            markup=True,
            color=(0.18, 1, 0.48, 1),
            font_size='22sp',
            halign='center'
        )
        layout.add_widget(self.lbl)
        Clock.schedule_once(self.open_browser, 3)
        return layout

    def open_browser(self, dt):
        import webbrowser
        webbrowser.open('http://localhost:5000')
        self.lbl.text = '[b]VERVAIN[/b]\nTarayici aciliyor...'

if __name__ == '__main__':
    VervainApp().run()
import threading
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

def start_server():
    import sys
    sys.path.insert(0, '.')
    from server import run
    run()

class VervainApp(App):
    def build(self):
        Window.clearcolor = (0.01, 0.04, 0.03, 1)
        threading.Thread(target=start_server, daemon=True).start()
        layout = AnchorLayout()
        self.lbl = Label(
            text='[b]VERVAIN[/b]\nBaslatiliyor...',
            markup=True,
            color=(0.18, 1, 0.48, 1),
            font_size='22sp',
            halign='center'
        )
        layout.add_widget(self.lbl)
        Clock.schedule_once(self.open_browser, 3)
        return layout

    def open_browser(self, dt):
        import webbrowser
        webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    VervainApp().run()
