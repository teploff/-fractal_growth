import math
from typing import List

from geometry.entity_2d import Segment, Point
from ontogeny.utils import engender_segment

CENTER = Point(0.0, 0.0)
BETA = 45.0


class Curve:
    """

    """

    def __init__(self, max_l_l: float, max_n_iter: int):
        """

        :param max_l_l:
        :param max_n_iter:
        """

        self._max_l_l = max_l_l
        self._max_n_iter = max_n_iter
        self._active_segments = []
        self.lines = []

        self._engender_segment()

    def _engender_segment(self):
        """

        :return:
        """

        segment = Segment(Point(CENTER.x - 0.001, CENTER.y), Point(CENTER.x + 0.001, CENTER.y))
        self.lines.append([segment])

        while segment.len() < self._max_l_l:
            segment = Segment(Point(segment.start.x, segment.start.y), Point(segment.finish.x, segment.finish.y))
            engender_segment(segment, self._max_l_l / self._max_n_iter)

            self.lines.append([segment])

        self._active_segments.append(segment)

    def _engender_primitive(self):
        """

        :return:
        """

        union_segments = []

        angle = self._active_segments[0].get_triangle_angle()
        union_segments.append(self._make_construction(
            self._max_n_iter, self._max_l_l, self._max_l_l / 2.0, self._active_segments[0].start, angle))

        for depth in range(len(union_segments[0])):
            depth_segments = [segment for segments in union_segments for segment in segments[depth]]

            dx = CENTER.x - depth_segments[len(depth_segments) // 2 - 1].finish.x
            dy = CENTER.y - depth_segments[len(depth_segments) // 2 - 1].finish.y
            depth_segments[len(depth_segments) // 2 - 1].start.x += dx
            depth_segments[len(depth_segments) // 2 - 1].start.y += dy
            depth_segments[len(depth_segments) // 2 - 1].finish.x += dx
            depth_segments[len(depth_segments) // 2 - 1].finish.y += dy
            reference_point = depth_segments[len(depth_segments) // 2 - 1].start
            left_side = depth_segments[:len(depth_segments) // 2 - 1]
            for line in left_side[::-1]:
                dx = reference_point.x - line.finish.x
                dy = reference_point.y - line.finish.y
                line.start.x += dx
                line.start.y += dy
                line.finish.x += dx
                line.finish.y += dy
                reference_point = line.start

            dx = CENTER.x - depth_segments[len(depth_segments) // 2].start.x
            dy = CENTER.y - depth_segments[len(depth_segments) // 2].start.y
            depth_segments[len(depth_segments) // 2].start.x += dx
            depth_segments[len(depth_segments) // 2].start.y += dy
            depth_segments[len(depth_segments) // 2].finish.x += dx
            depth_segments[len(depth_segments) // 2].finish.y += dy
            reference_point = depth_segments[len(depth_segments) // 2].finish
            right_side = depth_segments[len(depth_segments) // 2 + 1:]
            for line in right_side:
                dx = reference_point.x - line.start.x
                dy = reference_point.y - line.start.y
                line.start.x += dx
                line.start.y += dy
                line.finish.x += dx
                line.finish.y += dy
                reference_point = line.finish

            self.lines += [depth_segments]

        self._active_segments = self.lines[-1]

    @staticmethod
    def _make_construction(max_iter: int, max_length: float, start_length: float, point: Point, angle: float) -> \
            List[List[Segment]]:
        """
        Формирование списков промежуточных фаз роста фрактальной структуры.
        :param max_iter: Количество итераций роста фрактальной структуры.
        :param max_length: Предельное значение длины отрезка.
        :param start_length: Начальное знаение отрезка.
        :param point: Точка на основе которой просиходит рост.
        :param angle: Угол наклона фрактальной структуры.
        :return: Список промежуточных фаз фрактальной структуры.
        """
        
        segments = []
        length = start_length
        delta_length = (max_length - start_length) / max_iter

        for iteration in range(max_iter):
            height = ((iteration + 1) / max_iter) * max_length * math.sin(BETA * math.pi / 180.0)
            length += delta_length

            x_2 = point.x + length * math.cos(angle * math.pi / 180.0)
            y_2 = point.y + length * math.sin(angle * math.pi / 180.0)

            x_3 = x_2 + (height * math.cos((angle + BETA) * math.pi / 180.0)) / math.sin(BETA * math.pi / 180.0)
            y_3 = y_2 + (height * math.sin((angle + BETA) * math.pi / 180.0)) / math.sin(BETA * math.pi / 180.0)

            x_4 = x_3 + (height * math.cos((BETA - angle) * math.pi / 180.0)) / math.sin(BETA * math.pi / 180.0)
            y_4 = y_3 - (height * math.sin((BETA - angle) * math.pi / 180.0)) / math.sin(BETA * math.pi / 180.0)

            x_5 = x_4 + length * math.cos(angle * math.pi / 180.0)
            y_5 = y_4 + length * math.sin(angle * math.pi / 180.0)

            segment_1 = Segment(Point(point.x, point.y), Point(x_2, y_2))
            segment_2 = Segment(Point(x_2, y_2), Point(x_3, y_3))
            segment_3 = Segment(Point(x_3, y_3), Point(x_4, y_4))
            segment_4 = Segment(Point(x_4, y_4), Point(x_5, y_5))

            segments.append([segment_1, segment_2, segment_3, segment_4])
        
        return segments

    @staticmethod
    def _stick_segments_together_relative_the_point(segments: List[Segment], point: Point) -> List[Segment]:
        """

        :param segments:
        :param point:
        :return:
        """

        # TODO: make it pretty!!!
        dx = point.x - segments[len(segments) // 2 - 1].finish.x
        dy = point.y - segments[len(segments) // 2 - 1].finish.y
        segments[len(segments) // 2 - 1].start.x += dx
        segments[len(segments) // 2 - 1].start.y += dy
        segments[len(segments) // 2 - 1].finish.x += dx
        segments[len(segments) // 2 - 1].finish.y += dy
        reference_point = segments[len(segments) // 2 - 1].start
        left_side = segments[:len(segments) // 2 - 1]
        for line in left_side[::-1]:
            dx = reference_point.x - line.finish.x
            dy = reference_point.y - line.finish.y
            line.start.x += dx
            line.start.y += dy
            line.finish.x += dx
            line.finish.y += dy
            reference_point = line.start

        dx = point.x - segments[len(segments) // 2].start.x
        dy = point.y - segments[len(segments) // 2].start.y
        segments[len(segments) // 2].start.x += dx
        segments[len(segments) // 2].start.y += dy
        segments[len(segments) // 2].finish.x += dx
        segments[len(segments) // 2].finish.y += dy
        reference_point = segments[len(segments) // 2].finish
        right_side = segments[len(segments) // 2 + 1:]
        for line in right_side:
            dx = reference_point.x - line.start.x
            dy = reference_point.y - line.start.y
            line.start.x += dx
            line.start.y += dy
            line.finish.x += dx
            line.finish.y += dy
            reference_point = line.finish

        return segments

    def build(self, n_cycles: int):
        """

        :param n_cycles:
        :return:
        """

        if n_cycles == 1:
            return

        self._engender_primitive()

        if n_cycles == 2:
            return

        min_iter = 0
        growths = [60, 120]
        union_segments = []
        while min_iter < max(growths) * (n_cycles - 2):
            depths = [[] for _ in range(len(self._active_segments))]

            for index in range(len(self._active_segments) // 2):
                angle = self._active_segments[index].get_triangle_angle()
                depths[index] = self._make_construction(
                    growths[index % len(growths)], self._max_l_l, self._max_l_l / 2.0,
                    self._active_segments[index].start, angle)

                angle = self._active_segments[len(self._active_segments) - 1 - index].get_triangle_angle()
                depths[len(self._active_segments) - 1 - index] = self._make_construction(
                    growths[index % len(growths)], self._max_l_l, self._max_l_l / 2.0,
                    self._active_segments[len(self._active_segments) - 1 - index].start, angle)

            # ...
            union_segments.append(depths)

            # Заносим в список активных отрезков последние вычисленные отрезки
            self._active_segments = [segment for segments in depths for segment in segments[-1]]

            # max_iter = sum(max(len(lines) for lines in depth) for depth in union_segments)
            min_iter = sum(min(len(lines) for lines in depth) for depth in union_segments)

        counter = 0
        buffer = union_segments[0][:]
        for index_depth, depth in enumerate(union_segments):
            iterr = min(len(lines) for lines in buffer)
            counter += iterr
            aa = []
            for _ in range(iterr):
                segments = []
                for lines in buffer:
                    segments += lines[0]
                    del lines[0]
                aa.append(segments)

            empty_list_index = [index for index in range(len(buffer)) if buffer[index] == []]
            for index in empty_list_index:
                if index_depth + 1 != len(union_segments):
                    del buffer[index]
                    buffer.insert(index, union_segments[index_depth + 1][4 * index: 4 * index + 4])
                for i in range(4):
                    union_segments[index_depth + 1][4 * index + i] = []

            for index in empty_list_index[::-1]:
                temp = buffer[index]
                del buffer[index]
                for i in range(len(temp)):
                    buffer.insert(i + index, temp[i])
            ###########################################################################################################
            self.lines += [self._stick_segments_together_relative_the_point(depth_segments, CENTER) for depth_segments in aa]
            ############################################################################################################
            break
            if counter == min_iter:
                break
            # for i in range(len(union_segments[index_depth + 1][4 * index: 4 * index + 4])):
            #     depth.insert(i + index, union_segments[index_depth + 1][4 * index: 4 * index + 4][i])
            pass
            # for index_lines, lines in enumerate(depth):
            #     if len(lines) < max_iter:

        # pass
        # lolo = []
        # for iteration in range(min_iter):
        #     lolo[iteration] =
        # for depth in range(min(len(union_segment) for union_segment in union_segments)):
        #     depth_segments = [segment for segments in union_segments for segment in segments[depth]]
        #
        #     dx = CENTER.x - depth_segments[len(depth_segments)//2 - 1].finish.x
        #     dy = CENTER.y - depth_segments[len(depth_segments)//2 - 1].finish.y
        #     depth_segments[len(depth_segments)//2 - 1].start.x += dx
        #     depth_segments[len(depth_segments)//2 - 1].start.y += dy
        #     depth_segments[len(depth_segments)//2 - 1].finish.x += dx
        #     depth_segments[len(depth_segments)//2 - 1].finish.y += dy
        #     reference_point = depth_segments[len(depth_segments)//2 - 1].start
        #     left_side = depth_segments[:len(depth_segments) // 2 - 1]
        #     for line in left_side[::-1]:
        #         dx = reference_point.x - line.finish.x
        #         dy = reference_point.y - line.finish.y
        #         line.start.x += dx
        #         line.start.y += dy
        #         line.finish.x += dx
        #         line.finish.y += dy
        #         reference_point = line.start
        #
        #     dx = CENTER.x - depth_segments[len(depth_segments) // 2].start.x
        #     dy = CENTER.y - depth_segments[len(depth_segments) // 2].start.y
        #     depth_segments[len(depth_segments) // 2].start.x += dx
        #     depth_segments[len(depth_segments) // 2].start.y += dy
        #     depth_segments[len(depth_segments) // 2].finish.x += dx
        #     depth_segments[len(depth_segments) // 2].finish.y += dy
        #     reference_point = depth_segments[len(depth_segments) // 2].finish
        #     right_side = depth_segments[len(depth_segments) // 2 + 1:]
        #     for line in right_side:
        #         dx = reference_point.x - line.start.x
        #         dy = reference_point.y - line.start.y
        #         line.start.x += dx
        #         line.start.y += dy
        #         line.finish.x += dx
        #         line.finish.y += dy
        #         reference_point = line.finish
        #
        #     self.lines += [depth_segments]
        #
        # self._active_segments = self.lines[-1]
