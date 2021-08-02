import covid_map as cov_map
import kivy_map as kivy


if __name__ == '__main__':
    program = cov_map.GuiCommunication()
    app = kivy.CovMapApp(program)
    app.start_app()
