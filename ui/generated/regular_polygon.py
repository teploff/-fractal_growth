# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/static/regular_polygon.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(380, 310)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.sb_fractal_depth = QtWidgets.QSpinBox(self.centralWidget)
        self.sb_fractal_depth.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_fractal_depth.setMinimum(1)
        self.sb_fractal_depth.setMaximum(10)
        self.sb_fractal_depth.setObjectName("sb_fractal_depth")
        self.horizontalLayout_3.addWidget(self.sb_fractal_depth)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(18, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.dsb_max_line_legth = QtWidgets.QDoubleSpinBox(self.centralWidget)
        self.dsb_max_line_legth.setMinimum(0.01)
        self.dsb_max_line_legth.setMaximum(1.0)
        self.dsb_max_line_legth.setSingleStep(0.01)
        self.dsb_max_line_legth.setProperty("value", 0.05)
        self.dsb_max_line_legth.setObjectName("dsb_max_line_legth")
        self.horizontalLayout_4.addWidget(self.dsb_max_line_legth)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setSpacing(6)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.l_count_iterations = QtWidgets.QLabel(self.centralWidget)
        self.l_count_iterations.setTextFormat(QtCore.Qt.AutoText)
        self.l_count_iterations.setAlignment(QtCore.Qt.AlignCenter)
        self.l_count_iterations.setObjectName("l_count_iterations")
        self.horizontalLayout_12.addWidget(self.l_count_iterations)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem2)
        self.sb_count_iterations = QtWidgets.QSpinBox(self.centralWidget)
        self.sb_count_iterations.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_count_iterations.setMinimum(1)
        self.sb_count_iterations.setMaximum(200)
        self.sb_count_iterations.setSingleStep(5)
        self.sb_count_iterations.setProperty("value", 40)
        self.sb_count_iterations.setObjectName("sb_count_iterations")
        self.horizontalLayout_12.addWidget(self.sb_count_iterations)
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_9 = QtWidgets.QLabel(self.centralWidget)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_6.addWidget(self.label_9)
        spacerItem3 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.dsb_angle = QtWidgets.QDoubleSpinBox(self.centralWidget)
        self.dsb_angle.setMinimum(1.0)
        self.dsb_angle.setMaximum(89.0)
        self.dsb_angle.setSingleStep(0.1)
        self.dsb_angle.setProperty("value", 45.0)
        self.dsb_angle.setObjectName("dsb_angle")
        self.horizontalLayout_6.addWidget(self.dsb_angle)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.lb_image = QtWidgets.QLabel(self.centralWidget)
        self.lb_image.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_image.setObjectName("lb_image")
        self.verticalLayout.addWidget(self.lb_image)
        self.layout_regular_poygon = QtWidgets.QVBoxLayout()
        self.layout_regular_poygon.setSpacing(6)
        self.layout_regular_poygon.setObjectName("layout_regular_poygon")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setSpacing(6)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.lb_regular_polygon_count_angle = QtWidgets.QLabel(self.centralWidget)
        self.lb_regular_polygon_count_angle.setTextFormat(QtCore.Qt.AutoText)
        self.lb_regular_polygon_count_angle.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_regular_polygon_count_angle.setObjectName("lb_regular_polygon_count_angle")
        self.horizontalLayout_13.addWidget(self.lb_regular_polygon_count_angle)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem4)
        self.sb_regular_polygon_count_angle = QtWidgets.QSpinBox(self.centralWidget)
        self.sb_regular_polygon_count_angle.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_regular_polygon_count_angle.setMinimum(3)
        self.sb_regular_polygon_count_angle.setMaximum(40)
        self.sb_regular_polygon_count_angle.setSingleStep(1)
        self.sb_regular_polygon_count_angle.setProperty("value", 3)
        self.sb_regular_polygon_count_angle.setObjectName("sb_regular_polygon_count_angle")
        self.horizontalLayout_13.addWidget(self.sb_regular_polygon_count_angle)
        self.layout_regular_poygon.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setSpacing(6)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.rb_regular_polygon_build_outside = QtWidgets.QRadioButton(self.centralWidget)
        self.rb_regular_polygon_build_outside.setChecked(True)
        self.rb_regular_polygon_build_outside.setObjectName("rb_regular_polygon_build_outside")
        self.horizontalLayout_14.addWidget(self.rb_regular_polygon_build_outside)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem5)
        self.rb_regular_polygon_build_inside = QtWidgets.QRadioButton(self.centralWidget)
        self.rb_regular_polygon_build_inside.setObjectName("rb_regular_polygon_build_inside")
        self.horizontalLayout_14.addWidget(self.rb_regular_polygon_build_inside)
        self.layout_regular_poygon.addLayout(self.horizontalLayout_14)
        self.verticalLayout.addLayout(self.layout_regular_poygon)
        self.pb_calculate_fractal = QtWidgets.QPushButton(self.centralWidget)
        self.pb_calculate_fractal.setObjectName("pb_calculate_fractal")
        self.verticalLayout.addWidget(self.pb_calculate_fractal)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 380, 22))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Фрактальная структура - Кривая Коха"))
        self.label.setText(_translate("MainWindow", "Глубина фрактала"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p>Max значение длины отрезка <span style=\" font-style:italic;\">a</span></p></body></html>"))
        self.l_count_iterations.setText(_translate("MainWindow", "<html><head/><body><p>Количество итераций роста отрезка <span style=\" font-style:italic;\">a</span></p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "Значение угла треугольника"))
        self.lb_image.setText(_translate("MainWindow", "Image"))
        self.lb_regular_polygon_count_angle.setText(_translate("MainWindow", "<html><head/><body><p>Количество углов правильной фигуры</p></body></html>"))
        self.rb_regular_polygon_build_outside.setText(_translate("MainWindow", "Строить снаружи"))
        self.rb_regular_polygon_build_inside.setText(_translate("MainWindow", "Строить внутрь"))
        self.pb_calculate_fractal.setText(_translate("MainWindow", "Вычислить"))