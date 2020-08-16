from typing import List, Tuple
import pygame
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui
from ui.design import Ui_MainWindow
from OpenGL.GL import *
# from OpenGL.GLU import *
from geometry.entity_2d import Segment
from fractals.koch.curve import Curve
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import scipy

SCROLL_UP = 4
SCROLL_DOWN = 5
HEIGHT = 1000
WIDTH = 1000

display = (WIDTH, HEIGHT)

MAX_LINE_LENGTH = 0.05
N_ITER = 20
BLACK = (0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)

DIRECTORY = './pictures/'


class Application(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # initialize components from generated design.py
        super().__init__()
        self.setupUi(self)

        # make default settings
        self.koch_curve = None
        self.error_dialog = QtWidgets.QErrorMessage()
        self.rgb_lines = BLACK
        self.rgb_background = WHITE
        self.l_image.setPixmap(QtGui.QPixmap("./static/single_phase_model.png"))
        self.lb_regular_polygon_count_angle.setHidden(True)
        self.sb_regular_polygon_count_angle.setHidden(True)
        self.rb_regular_polygon_build_inside.setHidden(True)
        self.rb_regular_polygon_build_outside.setHidden(True)
        self.l_several_phase_coefficient_a.setHidden(True)
        self.dsb_several_phase_coefficient_a.setHidden(True)
        self.l_several_phase_coefficient_h.setHidden(True)
        self.dsb_several_phase_coefficient_h.setHidden(True)
        self.l_several_phase_count_iterations.setHidden(True)
        self.sb_several_phase_count_iterations.setHidden(True)

        pygame.init()

        # callbacks
        self.pb_calculate_fractal.clicked.connect(self._calculation_fractal)
        self.pb_visualize.clicked.connect(self._visualize_fractal_growth)
        self.pb_build_point_path.clicked.connect(self._visualize_point_path_growth)
        self.pb_thin_out.clicked.connect(self._visualize_thin_out_fractal_growth)
        self.pb_line_color.clicked.connect(self._pick_lines_color)
        self.pb_background_color.clicked.connect(self._pick_background_color)
        self.rb_single_phase.clicked.connect(self._enable_single_phase)
        self.rb_several_phases.clicked.connect(self._enable_several_phases)
        self.rb_irregular_phases.clicked.connect(self._irregular_several_phases)
        self.rb_regular_polygon.clicked.connect(self._enable_regular_polygon)
        self.pb_graph_line_len.clicked.connect(self._plot_graph_line_len)
        self.pb_graph_scale.clicked.connect(self._plot_graph_scale)
        self.pb_graph_angle.clicked.connect(self._plot_graph_angle)

    def _calculation_fractal(self):
        """
        Вычислить фрактальную структуру.
        :return:
        """
        settings = dict()
        if self.rb_single_phase.isChecked():
            settings["model"] = "single"
            settings["count_iterations"] = self.sb_single_phase_count_iterations.value()
        elif self.rb_several_phases.isChecked():
            settings["model"] = "several"
            settings["coefficient_a"] = self.dsb_several_phase_coefficient_a.value()
            settings["coefficient_h"] = self.dsb_several_phase_coefficient_h.value()
            settings["count_iterations"] = int(self.sb_several_phase_count_iterations.value())
        elif self.rb_irregular_phases.isChecked():
            settings["model"] = "irregular"
            settings["coefficient_a"] = self.dsb_several_phase_coefficient_a.value()
            settings["coefficient_h"] = self.dsb_several_phase_coefficient_h.value()
            settings["count_iterations"] = int(self.sb_several_phase_count_iterations.value())
        else:
            settings["model"] = "regular_polygon"
            settings["count_iterations"] = self.sb_single_phase_count_iterations.value()
            settings["count_angles"] = self.sb_regular_polygon_count_angle.value()
            settings["building_way"] = "inside" if self.rb_regular_polygon_build_inside.isChecked() else "outside"

        self.koch_curve = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(), self.dsb_angle.value(),
                                **settings)
        self.koch_curve.build()

    def _is_calculations_absent(self):
        """
        Вычисления фрактальной структуры отсутствуют?
        :return:
        """
        if self.koch_curve is None:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText('Ошибка')
            msg.setInformativeText('Вычисления отсутсвуют. Необходимо вычислить фрактал!')
            msg.setWindowTitle('Error')
            msg.exec_()
            return True
        return False

    def _visualize_fractal_growth(self):
        """
        Визуализировать вычисленную фрактальную структуру.
        :return:
        """

        # TODO: make decorator
        if self._is_calculations_absent():
            return

        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

        index = 0
        quit_mode = False
        while not quit_mode:
            self.draw(self.koch_curve.lines[index % len(self.koch_curve.lines)], self.rgb_lines, self.rgb_background,
                      self.sb_draw_latency.value())
            # # TODO: make save image
            if index != 0 and index < len(self.koch_curve.lines):
                self.save_image(DIRECTORY, str(index) + '.png')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_mode = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit_mode = True

            index += 1

    def _visualize_point_path_growth(self):
        """
        Визуализировать траекторию точек роста вычисленной фрактальной структуры.
        :return:
        """
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

        index = 0
        quit_mode = False
        while not quit_mode:
            a = []
            for i in range(index % len(self.koch_curve.lines)):
                a += self.koch_curve.lines[i]
            self.draw_points(a, self.rgb_lines, self.rgb_background, self.sb_draw_latency.value())

            # TODO: make save image
            if index != 0 and index < len(self.koch_curve.lines):
                self.save_image(DIRECTORY, str(index) + '.png')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_mode = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit_mode = True

            index += 1

    def _visualize_thin_out_fractal_growth(self) -> None:
        """
        Прорядить фазы построения фрактальной структуры.
        :return:
        """
        # TODO: make decorator
        if self._is_calculations_absent():
            return

        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

        index = 0
        quit_mode = False
        lines = []

        # TODO: move to separate module
        if self.sb_thinning_percentage.value() > 0:
            percent = self.sb_thinning_percentage.value() * 0.01
            kz = len(self.koch_curve.lines) * percent
            kio = int(len(self.koch_curve.lines) / kz)
            lyly = [i for i in range(0, len(self.koch_curve.lines), kio)]
            lines = [lines for index, lines in enumerate(self.koch_curve.lines) if index % 40 == 0]

        while not quit_mode:
            a = []
            for i in range(index % len(lines)):
                a += lines[i]
            self.draw(a, self.rgb_lines, self.rgb_background, self.sb_draw_latency.value())

            # TODO: make save image
            if index != 0 and index < len(self.koch_curve.lines):
                self.save_image(DIRECTORY, str(index) + '.png')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_mode = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit_mode = True

            index += 1

    def _pick_lines_color(self) -> None:
        """
        Выбор паитры для отрисовки отрезков.
        :return:
        """
        color = QtWidgets.QColorDialog.getColor()

        self.rgb_lines = (color.redF(), color.greenF(), color.blueF())
        self.pb_line_color.setStyleSheet(f"QWidget {{ background-color: {color.name()} }}")

    def _pick_background_color(self) -> None:
        """
        Выбор палитры для заливки фона.
        :return:
        """
        color = QtWidgets.QColorDialog.getColor()

        self.rgb_background = (color.redF(), color.greenF(), color.blueF())
        self.pb_background_color.setStyleSheet(f"QWidget {{ background-color: {color.name()} }}")

    def _enable_single_phase(self) -> None:
        """
        Выбор построения однофазной модели.
        :return:
        """
        self.l_image.setPixmap(QtGui.QPixmap("./static/single_phase_model.png"))
        self.l_single_phase_count_iterations.setHidden(False)
        self.sb_single_phase_count_iterations.setHidden(False)
        self.lb_regular_polygon_count_angle.setHidden(True)
        self.sb_regular_polygon_count_angle.setHidden(True)
        self.rb_regular_polygon_build_inside.setHidden(True)
        self.rb_regular_polygon_build_outside.setHidden(True)
        self.l_several_phase_coefficient_a.setHidden(True)
        self.dsb_several_phase_coefficient_a.setHidden(True)
        self.l_several_phase_coefficient_h.setHidden(True)
        self.dsb_several_phase_coefficient_h.setHidden(True)
        self.l_several_phase_count_iterations.setHidden(True)
        self.sb_several_phase_count_iterations.setHidden(True)

    def _enable_several_phases(self) -> None:
        """
        Выбор построения многофазной модели.
        :return:
        """
        self.l_image.setPixmap(QtGui.QPixmap("./static/several_phases_model.png"))
        self.l_single_phase_count_iterations.setHidden(True)
        self.sb_single_phase_count_iterations.setHidden(True)
        self.lb_regular_polygon_count_angle.setHidden(True)
        self.sb_regular_polygon_count_angle.setHidden(True)
        self.rb_regular_polygon_build_inside.setHidden(True)
        self.rb_regular_polygon_build_outside.setHidden(True)
        self.l_several_phase_coefficient_a.setHidden(False)
        self.dsb_several_phase_coefficient_a.setHidden(False)
        self.l_several_phase_coefficient_h.setHidden(False)
        self.dsb_several_phase_coefficient_h.setHidden(False)
        self.l_several_phase_count_iterations.setHidden(False)
        self.sb_several_phase_count_iterations.setHidden(False)

    def _irregular_several_phases(self) -> None:
        """
        Выбор построения нерегулярной модели.
        :return:
        """
        self.l_image.setPixmap(QtGui.QPixmap("./static/single_phase_model.png"))
        self.l_single_phase_count_iterations.setHidden(False)
        self.sb_single_phase_count_iterations.setHidden(False)
        self.lb_regular_polygon_count_angle.setHidden(True)
        self.sb_regular_polygon_count_angle.setHidden(True)
        self.rb_regular_polygon_build_inside.setHidden(True)
        self.rb_regular_polygon_build_outside.setHidden(True)
        self.l_several_phase_coefficient_a.setHidden(False)
        self.dsb_several_phase_coefficient_a.setHidden(False)
        self.l_several_phase_coefficient_h.setHidden(False)
        self.dsb_several_phase_coefficient_h.setHidden(False)
        self.l_several_phase_count_iterations.setHidden(True)
        self.sb_several_phase_count_iterations.setHidden(True)

    def _enable_regular_polygon(self) -> None:
        """
        Выбор построения правильной фигуры.
        :return:
        """
        self.l_image.setPixmap(QtGui.QPixmap("./static/single_phase_model.png"))
        self.l_single_phase_count_iterations.setHidden(False)
        self.sb_single_phase_count_iterations.setHidden(False)
        self.lb_regular_polygon_count_angle.setHidden(False)
        self.sb_regular_polygon_count_angle.setHidden(False)
        self.rb_regular_polygon_build_inside.setHidden(False)
        self.rb_regular_polygon_build_outside.setHidden(False)
        self.l_several_phase_coefficient_a.setHidden(True)
        self.dsb_several_phase_coefficient_a.setHidden(True)
        self.l_several_phase_coefficient_h.setHidden(True)
        self.dsb_several_phase_coefficient_h.setHidden(True)
        self.l_several_phase_count_iterations.setHidden(True)
        self.sb_several_phase_count_iterations.setHidden(True)

    # TODO: approximation
    def _plot_graph_line_len(self) -> None:
        """
        # TODO: docstring
        :return:
        """
        # TODO: make decorator
        if self._is_calculations_absent():
            return

        # TODO: to name this shirt
        t = [sum(line.len() for line in lines) for lines in self.koch_curve.lines]
        s = [i for i in range(len(self.koch_curve.lines))]

        # TODO: wtf
        def mnkGP(x, y):
            d = 4  # степень полинома
            fp, residuals, rank, sv, rcond = scipy.polyfit(x, y, d, full=True)  # Модель
            f = scipy.poly1d(fp)  # аппроксимирующая функция
            print('Коэффициент -- a %s  ' % round(fp[0], 4))
            print('Коэффициент-- b %s  ' % round(fp[1], 4))
            print('Коэффициент -- c %s  ' % round(fp[2], 4))
            y1 = [fp[0] * x[i] ** 2 + fp[1] * x[i] + fp[2] for i in range(0, len(x))]  # значения функции a*x**2+b*x+c
            so = round(sum([abs(y[i] - y1[i]) for i in range(0, len(x))]) / (len(x) * sum(y)) * 100,
                       4)  # средняя ошибка
            print('Average quadratic deviation ' + str(so))
            fx = scipy.linspace(x[0], x[-1] + 1, len(x))  # можно установить вместо len(x) большее число для интерполяции
            fig, ax = plt.subplots()
            ax.plot(x, y, 'o', label='Original data', markersize=1)
            ax.plot(fx, f(fx), linewidth=2)
            ax.set(xlabel='Количество фаз (ед.)', ylabel='Длина фрактала (ед.)',
                   title='Зависимость длины фрактала от количества фаз')
            ax.grid(True)
            plt.show()
        # https://habr.com/ru/post/322954/
        mnkGP(s, t)

    # TODO: approximation
    def _plot_graph_scale(self):
        """
        # TODO: docstring
        :return:
        """
        # TODO: make decorator
        if self._is_calculations_absent():
            return

        # TODO: to name this shirt
        x = [abs(max(max(line.start.x, line.finish.x) for line in lines) -
                 min(min(line.start.x, line.finish.x) for line in lines)) for lines in self.koch_curve.lines]
        y = [abs(max(max(line.start.y, line.finish.y) for line in lines) -
                 min(min(line.start.y, line.finish.y) for line in lines)) for lines in self.koch_curve.lines]
        s = [i for i in range(len(self.koch_curve.lines))]

        # TODO: wtf
        def mnkGP(x, y1, y2):
            d = 4  # степень полинома
            fp1, residuals1, rank1, sv1, rcond1 = scipy.polyfit(x, y1, d, full=True)  # Модель
            fp2, residuals2, rank2, sv2, rcond2 = scipy.polyfit(x, y2, d, full=True)  # Модель
            f1 = scipy.poly1d(fp1)  # аппроксимирующая функция
            f2 = scipy.poly1d(fp2)  # аппроксимирующая функция
            print('Коэффициент -- a %s  ' % round(fp1[0], 4))
            print('Коэффициент -- a %s  ' % round(fp2[0], 4))
            print('Коэффициент-- b %s  ' % round(fp1[1], 4))
            print('Коэффициент-- b %s  ' % round(fp2[1], 4))
            print('Коэффициент -- c %s  ' % round(fp1[2], 4))
            print('Коэффициент -- c %s  ' % round(fp2[2], 4))
            y_1 = [f1[0] * x[i] ** 2 + fp1[1] * x[i] + fp1[2] for i in range(0, len(x))]  # значения функции a*x**2+b*x+c
            y_2 = [f2[0] * x[i] ** 2 + fp2[1] * x[i] + fp2[2] for i in range(0, len(x))]  # значения функции a*x**2+b*x+c
            so1 = round(sum([abs(y1[i] - y_1[i]) for i in range(0, len(x))]) / (len(x) * sum(y1)) * 100, 4)  # средняя ошибка
            so2 = round(sum([abs(y2[i] - y_2[i]) for i in range(0, len(x))]) / (len(x) * sum(y2)) * 100, 4)  # средняя ошибка
            print('Average quadratic deviation ' + str(so1))
            print('Average quadratic deviation ' + str(so2))
            fx = scipy.linspace(x[0], x[-1] + 1, len(x))  # можно установить вместо len(x) большее число для интерполяции

            fig, axs = plt.subplots(2, 1)
            fig.suptitle('Зависимость масштаба фрактала от количества фаз', fontsize=12)

            axs[0].plot(s, y1, '-o', ms=1, alpha=0.7, mfc='orange')
            axs[0].set(xlabel='Количество фаз (ед.)', ylabel='Величина по оси абсцисс (ед.)')
            axs[0].plot(fx, f1(fx), linewidth=2)
            axs[0].grid(True)

            axs[1].plot(s, y2, '-o', ms=1, alpha=0.7, mfc='orange')
            axs[1].set(xlabel='Количество фаз (ед.)', ylabel='Величина по оси ординат (ед.)')
            axs[1].plot(fx, f2(fx), linewidth=2)
            axs[1].grid(True)

            fig.tight_layout()
            plt.show()

        # https://habr.com/ru/post/322954/
        mnkGP(s, x, y)

    def _plot_graph_angle(self):
        """
        # TODO: docstring
        :return:
        """
        # TODO: make decorator
        if self._is_calculations_absent():
            return

        fig, ax = plt.subplots()
        # TODO: to name this shirt
        t = [line.get_triangle_angle() for lines in self.koch_curve.lines for line in lines]
        s = [phase for phase, lines in enumerate(self.koch_curve.lines) for _ in lines]

        ax.plot(s, t, 'o', ms=10, alpha=0.7, mfc='orange')
        ax.set(xlabel='Количество фаз (ед.)', ylabel='Величина угла (градусы)',
               title='Зависимость величин углов каждого из отрезков фрактала от количества фаз')
        ax.grid()
        plt.show()

    @staticmethod
    # TODO: make common method with draw points
    # TODO: move to another package
    def draw(lines: List[Segment], rgb_lines: Tuple[float, float, float], rgb_background: Tuple[float, float, float],
             draw_latency: int) -> None:
        """
        Прорисовка на канвасе OpenGL.
        :param lines: Список отрезков, которые необходимо отобразить.
        :param rgb_lines: RGB пера, которым будут отрисованы отрезки.
        :param rgb_background: RGB фона.
        :param draw_latency: задержка при отрисовке.
        :return:
        """
        glColor3f(*rgb_lines)
        glLineWidth(2)
        glClearColor(*rgb_background, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBegin(GL_LINES)
        for line in lines:
            glVertex2f(line.start.x, line.start.y)
            glVertex2f(line.finish.x, line.finish.y)
        glEnd()

        pygame.display.flip()
        pygame.time.wait(draw_latency)

    @staticmethod
    # TODO: make common method with draw lines
    # TODO: move to another package
    def draw_points(lines: List[Segment], rgb_lines: Tuple[float, float, float],
                    rgb_background: Tuple[float, float, float], draw_latency: int) -> None:
        """
        Прорисовка на канвасе OpenGL.
        :param lines: Список отрезков, которые необходимо отобразить.
        :param rgb_lines: RGB пера, которым будут отрисованы отрезки.
        :param rgb_background: RGB фона.
        :param draw_latency: задержка при отрисовке.
        :return:
        """
        glColor3f(*rgb_lines)
        glPointSize(2)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*rgb_background, 1)

        glBegin(GL_POINTS)
        for line in lines:
            glVertex2f(line.start.x, line.start.y)
            glVertex2f(line.finish.x, line.finish.y)
        glEnd()

        pygame.display.flip()
        pygame.time.wait(draw_latency)

    @staticmethod
    # TODO: make full file path
    # TODO: choose color to transparency
    # TODO: move to another package
    def save_image(directory: str, file_name: str) -> None:
        """
        Сохранение текущего состояния канваса OpenGL в виде PNG файла на диск с прозрачным фоном, заменив при этом все
        белые пиксели.
        :param directory: Полный или относительный путь дирректории, куда будет производиться сохранение.
        :param file_name: Наименование файла.
        :return:
        """
        glPixelStorei(GL_PACK_ALIGNMENT, 1)

        rough_data = glReadPixels(0, 0, WIDTH, HEIGHT, GL_RGBA, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (WIDTH, HEIGHT), rough_data)
        image = ImageOps.flip(image)  # in my case image is flipped top-bottom for some reason
        data = image.getdata()
        new_data = []
        for item in data:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        image.putdata(new_data)

        image.save(directory + file_name, 'PNG')


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = Application()
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
