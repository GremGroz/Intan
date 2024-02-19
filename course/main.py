import openpyxl as xl
import os
from interval import Interval
from draw import drawModa, drawMultyModa

save_path = 'docs/course/img/'

def dataBuilder():

    workbook = xl.load_workbook(os.path.abspath('course') + '\data\Rev_Tables_&_charts_for_isotope_abundance_var_&_at_wt_of_sel_elements_2016 (1).xlsx')
    carbon_data = workbook['Carbon']

    def find_intervals(data) -> tuple:
        count = 0
        header_row = data[2]
        for cell in header_row:
            if count == 2:
                break
            if cell.value == 'Atomic weight':
                count += 1
                if count > 1:
                    upper_bound_coord = cell.coordinate
                else:
                    lower_bound_coord = cell.coordinate 
        return (xl.utils.cell.coordinate_from_string(lower_bound_coord), xl.utils.cell.coordinate_from_string(upper_bound_coord))

    atomic_weights_coord = find_intervals(carbon_data)

    def intervals() -> list: 
        lower_bound = []
        upper_bound = []
        for cell in range(2,33):
            lower_bound.append(carbon_data[atomic_weights_coord[0][0]][cell].value)
            upper_bound.append(carbon_data[atomic_weights_coord[1][0]][cell].value)
        return [lower_bound, upper_bound]

    weights_datas = intervals()

    counter = -1
    for weight in weights_datas[1]:
        counter += 1
        if weight == None:
            if weights_datas[0][counter] == None:
                weights_datas[0].pop(counter)
                weights_datas[1].pop(counter)
                counter -= 1
            weights_datas[1][counter] = weights_datas[0][counter]

    counter = -1
    for weight in weights_datas[0]:
        counter += 1
        if weight == None:
            if weights_datas[1][counter] == None:
                weights_datas[0].pop(counter)
                weights_datas[1].pop(counter)
                counter -= 1
            weights_datas[0][counter] = weights_datas[1][counter]
            
            
    return [list(x) for x in zip(weights_datas[0], weights_datas[1])]


def main():    
    intervals_data = dataBuilder()
    intervals = [Interval(start, end) for start, end in intervals_data]
    # for interval in intervals:
    #     print(interval.to_str())

    # intervals_in_moda, moda_hist, moda_bar_intervals, moda = Interval.find_moda(intervals)

    # print(moda_hist)
    # for moda_bar_interval in moda_bar_intervals:
    #     print(moda_bar_interval.to_str())

    _, moda_hist, _, moda = Interval.find_moda(intervals)
        
    multimoda, max_index = Interval.find_multimodal_frequency(intervals)

    print(multimoda)
    print(max_index)
    drawModa(moda_hist, save_path)
    drawMultyModa(moda_hist, multimoda, max_index, save_path)

if __name__ == '__main__':
    main()





    