# Form implementation generated from reading ui file 'f:\UNI_STUFF\5th Sem\Photo-Wizard\ui_files\view_toolbar.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_view_toolbar_widget(object):
    def setupUi(self, view_toolbar_widget):
        view_toolbar_widget.setObjectName("view_toolbar_widget")
        view_toolbar_widget.resize(905, 280)
        self.gridLayout = QtWidgets.QGridLayout(view_toolbar_widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.main_widget = QtWidgets.QWidget(parent=view_toolbar_widget)
        self.main_widget.setObjectName("main_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.main_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edit_button = QtWidgets.QPushButton(parent=self.main_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_button.sizePolicy().hasHeightForWidth())
        self.edit_button.setSizePolicy(sizePolicy)
        self.edit_button.setObjectName("edit_button")
        self.horizontalLayout.addWidget(self.edit_button)
        self.gridLayout.addWidget(self.main_widget, 0, 0, 1, 1)

        self.retranslateUi(view_toolbar_widget)
        QtCore.QMetaObject.connectSlotsByName(view_toolbar_widget)

    def retranslateUi(self, view_toolbar_widget):
        _translate = QtCore.QCoreApplication.translate
        view_toolbar_widget.setWindowTitle(_translate("view_toolbar_widget", "Form"))
        self.edit_button.setText(_translate("view_toolbar_widget", "Edit"))