import os


class Filepaths:
    __MAIN_WINDOW = 'ui_files/main-window.ui'
    __ADJUST_WIDGET = 'ui_files/adjust-widget.ui'
    __TEMP = 'ui_files/untitled.ui'
    __VIEW_TOOLBAR = 'ui_files/view_toolbar.ui'

    @staticmethod
    def MAIN_WINDOW():
        return os.path.abspath(Filepaths.__MAIN_WINDOW)

    @staticmethod
    def ADJUST_WIDGET():
        return os.path.abspath(Filepaths.__ADJUST_WIDGET)

    @staticmethod
    def TEMP():
        return os.path.abspath(Filepaths.__TEMP)

    @staticmethod
    def VIEW_TOOLBAR():
        return os.path.abspath(Filepaths.__VIEW_TOOLBAR)


if __name__ == '__main__':
    print(Filepaths.ADJUST_WIDGET())
