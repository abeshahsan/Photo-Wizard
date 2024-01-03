import os


class Filepaths:
    __MAIN_WINDOW = 'ui_files/main-window.ui'
    __ADJUST_WIDGET = 'ui_files/adjust-widget.ui'
    __TEMP = 'ui_files/untitled.ui'
    __VIEW_TOOLBAR = 'ui_files/view_toolbar.ui'
    __EDIT_TOOLBAR = 'ui_files/edit_toolbar.ui'
    __FILTER_WIDGET = 'ui_files/filter_widget.ui'
    __FILTER_INPUT_DIALOG = 'ui_files/filter_input_dialog.ui'
    __FILTER_FILE = 'Filters.json'
    __CROP_TOOLBAR = 'ui_files/crop_toolbar.ui'

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

    @staticmethod
    def EDIT_TOOLBAR():
        return os.path.abspath(Filepaths.__EDIT_TOOLBAR)

    @staticmethod
    def FILTER_WIDGET():
        return os.path.abspath(Filepaths.__FILTER_WIDGET)

    @staticmethod
    def FILTER_FILE():
        return os.path.abspath(Filepaths.__FILTER_FILE)

    @staticmethod
    def FILTER_INPUT_DIALOG():
        return os.path.abspath(Filepaths.__FILTER_INPUT_DIALOG)
    
    @staticmethod
    def CROP_TOOLBAR():
        return os.path.abspath(Filepaths.__CROP_TOOLBAR)


if __name__ == '__main__':
    print(Filepaths.EDIT_TOOLBAR())
