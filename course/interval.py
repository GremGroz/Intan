from __future__ import annotations
from typing import List, Tuple
import numpy as np

class Interval:
    @staticmethod
    def min_max_union(intervals: List[Interval]) -> Interval:
        union_interval = intervals[0]

        for interval in intervals:
            union_interval = Interval(
                min(union_interval.left, interval.left),
                max(union_interval.right, interval.right)
            )

        return union_interval
    
    @staticmethod
    def min_max_intersection(intervals: List[Interval]) -> Interval:
        intersection_interval = intervals[0]

        for interval in intervals:
            intersection_interval = Interval(
                max(intersection_interval.left, interval.left),
                min(intersection_interval.right, interval.right)
            )

        return intersection_interval
    
    @staticmethod
    def jaccard_index(intervals: List[Interval]) -> float:
        return Interval.min_max_intersection(intervals).wid() / Interval.min_max_union(intervals).wid() * 0.5 + 0.5

    
    @staticmethod
    def scale_intervals(intervals: List[Interval], multiplier: float) -> List[Interval]:
        return [interval.scale(multiplier) for interval in intervals]
    
    @staticmethod
    def expand_intervals(intervals: List[Interval], eps: float) -> List[Interval]:
        return [interval.expand(eps) for interval in intervals]
    
    @staticmethod
    def combine_intervals(intervals1 : List[Interval], intervals2: List[Interval]) -> List[Interval]:
        return [j for i in [intervals1, intervals2] for j in i]
    
    @staticmethod
    def find_moda(intervals: List[Interval]) -> Tuple[int, List[int], List[Interval], Interval]:
        intervals_edges = []
        for interval in intervals:
            intervals_edges.append(interval.left)
            intervals_edges.append(interval.right)

        intervals_edges = list(set(intervals_edges))
        intervals_edges.sort()
        moda_hist = [0 for _ in range(len(intervals_edges) - 1)]
        moda_bar_intervals = [Interval(0, 0) for _ in range(len(intervals_edges) - 1)]

        moda = Interval(0, 0)
        intervals_in_moda = 0
        for i, point in enumerate(intervals_edges):
            if i == len(intervals_edges) - 1:
                break

            current_interval = Interval(point, intervals_edges[i + 1])
            current_interval_in_moda = 0

            for interval in intervals:
                current_interval_in_moda += interval.contains(current_interval.mid())

            if current_interval_in_moda > intervals_in_moda:
                moda = current_interval
                intervals_in_moda = current_interval_in_moda

            moda_hist[i] = current_interval_in_moda
            moda_bar_intervals[i] = current_interval
        
        #print(f'moda = {moda.to_str()}, intervals = {intervals_in_moda}')
        return intervals_in_moda, moda_hist, moda_bar_intervals, moda
    
    
    @staticmethod
    def find_multimodal_frequency(intervals: List[Interval]) -> List[Interval]:
        _, frequencies, _, _ = Interval.find_moda(intervals)  # Находим интервалы мод
        noise = 0  
        max_in_segment = []

        # Инициализация переменной для хранения расширенных интервалов
        expanded_intervals = []
        # Расширение границ интервалов
        while True:

            # step_backward = 0
            # step_forward = 0
            step = 0
            max_moda = max(frequencies)
            cur_index = frequencies.index(max_moda)
            max_in_segment.append(cur_index)
            wide_moda = Interval(max_moda, max_moda)


            if max_moda < 2:
                break
            

            while True:
                step += 1
                if (cur_index - step) < 0:
                    step -= 1
                    break      
                
                if frequencies[cur_index - step] == 0:
                    step += 1
                    break    
                if (frequencies[cur_index - step] <= max_moda):
                    wide_moda.left = frequencies[cur_index - step]
                else:
                    break
                if max_moda < wide_moda.left:
                    break
                max_moda = wide_moda.left
            step -= 1
            left_border = cur_index - step            
            
            step = 0
            max_moda = max(frequencies)
            
            while True:
                step += 1
                if (cur_index + step) > (len(frequencies) - 1):
                    step -= 1
                    break      
                
                if frequencies[cur_index + step] == 0:
                    step += 1
                    break              
                if (frequencies[cur_index + step] <= max_moda):
                    wide_moda.right = frequencies[cur_index + step]
                else:
                    break
                if max_moda < wide_moda.right:
                    break
                max_moda = wide_moda.right
            step -= 1
            right_border = cur_index + step
            
            for i in range(left_border, right_border + 1):
                frequencies[i] = 0
            
            expanded_intervals.append([left_border, right_border])
            # while True:
            #     if (cur_index + step_forward) > (len(frequencies) - 1):
            #         step_forward -= 1
            #         break
            #     if (cur_index + step_backward) < 0:
            #         step_backward += 1
            #         break
                

            #     if (frequencies[cur_index + step_backward] <= max_moda)\
            #     and (wide_moda.left != 0):
            #         step_backward -= 1
            #     else:
            #         frequencies[cur_index + step_backward] = 0
            #     if (frequencies[cur_index + step_forward] <= max_moda)\
            #     and (wide_moda.right != 0):   
            #         step_forward += 1
            #     else:
            #         frequencies[cur_index + step_forward] = 0
                
            #     wide_moda.left = frequencies[cur_index + step_backward]
            #     wide_moda.right = frequencies[cur_index + step_forward]              
                    
            #     if (max_moda < max(wide_moda.left, wide_moda.right) + noise)\
            #         or ((wide_moda.left == 0) and (wide_moda.right == 0)):
            #         break

            #     max_moda = max(wide_moda.left, wide_moda.right)
                
             
            # if (cur_index + step_forward + 1) > (len(frequencies) - 1):
            #     step_forward -= 1
            # if (cur_index + step_backward - 1) < 0:
            #     step_backward += 1
                   
            # for i in range(cur_index + step_backward, cur_index + step_forward + 1):
            #     frequencies[i] = 0
            # expanded_intervals.append([cur_index + step_backward, cur_index + step_forward])

        return expanded_intervals, max_in_segment[0:-1]

    def __init__(self, x: float, y: float, force_right: bool = False) -> None:
        self.left =  min(x, y) if force_right else x
        self.right = max(x, y) if force_right else y

    def wid(self) -> float:
        return self.right - self.left
    
    def rad(self) -> float:
        return self.wid() * 0.5
    
    def mid(self) -> float:
         return (self.left + self.right) * 0.5
    
    def pro(self) -> Interval:
        return Interval(self.left, self.right, True)
    
    def scale(self, multiplier: float) -> Interval:
        return Interval(self.left * multiplier, self.right * multiplier, True)
    
    def expand(self, eps: float) -> Interval:
        return Interval(self.left - eps, self.right + eps)

    def to_str(self, round_num: int = 6, use_math_note: bool = False) -> str:
        if use_math_note:
            return f'[{self.left:.{round_num}e}, {self.right:.{round_num}e}]'
        else:
            return f'[{round(self.left, round_num)}, {round(self.right, round_num)}]'
    
    def contains(self, val: float) -> bool:
        return self.left <= val <= self.right;