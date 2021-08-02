import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

import covid_map as cov_map


class CovMapGrid(Widget):

    def __init__(self, backend, *args, **kwargs):
        super(CovMapGrid, self).__init__(*args, **kwargs)
        self._backend = backend

    def request(self, pick):
        self.pick = pick
        self._backend.gui_communication(self.pick)

class CovMapApp(App):

    def __init__(self, backend):
        super(CovMapApp, self).__init__()
        self._backend = backend

    def build(self):
        return CovMapGrid(self._backend)

    def start_app(self):
        CovMapApp(self._backend).run()                

if __name__ == '__main__':
    program = cov_map.GuiCommunication()
    app = CovMapApp(program)
    app.start_app()
