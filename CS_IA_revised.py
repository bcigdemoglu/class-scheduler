import numpy as np    
from tqdm import tqdm
import xlrd

def load_excel_sheet(path):
    
    path = '/Users/erelpapo/Desktop/ERIK/class_combs.xlsx'
    wb = xlrd.open_workbook(path) 
    sheet = wb.sheet_by_index(0)
    
    return sheet

def get_class_name_ID_dicts(sheet):
    
    num_combos = sheet.nrows 
    num_class_per_combo = sheet.ncols

    class_names = set()
    for i in range(num_combos):
        for j in range(num_class_per_combo):
            class_names.add(sheet.cell_value(i, j))

    class_name_to_class_ID = {}
    class_ID = 0
    for class_name in class_names:
        class_name_to_class_ID[str(class_name)] = class_ID
        class_ID += 1

    class_ID_to_class_name = {v: k for k, v in class_name_to_class_ID.items()}
    return class_name_to_class_ID, class_ID_to_class_name

def get_class_name_combos_class_ID_combos(sheet, class_name_to_class_ID):
    
    num_combos = sheet.nrows 
    num_class_per_combo = sheet.ncols

    class_name_combos = []
    class_ID_combos = []

    for i in range(num_combos):
        class_name_combo = []
        class_ID_combo = []

        for j in range(num_class_per_combo):
            # class_name = sheet.cell_value(i, j)
            class_name_combo.append(sheet.cell_value(i, j))
            class_ID_combo.append(class_name_to_class_ID[sheet.cell_value(i, j)])

        class_name_combos.append(class_name_combo)
        class_ID_combos.append(class_ID_combo)

    return class_name_combos, class_ID_combos

def get_class_combo_matrix(class_ID_combos, num_combos, num_classes):
    
    A = np.zeros((num_combos, num_classes))
    
    for i in range(len(class_ID_combos)):
        class_ID_combo = class_ID_combos[i]
        for c in class_ID_combo: 
            A[i, c] = 1
            
    return A
    
def get_valid_schedule_per_slot(A, num_combos, num_classes):
    
    x_list = []
    for i in range(2**num_classes):
        small_x = list("{0:b}".format(i))
        small_x = np.array([float(m) for m in small_x])
        x = np.zeros(num_classes)
        for j in range(len(small_x)):
            x[len(x) - 1 - j] = small_x[len(small_x) - 1 - j]
        if sum(np.matmul(A, x) <= 1) == num_combos:
            x_list.append(x)
            
    return x_list

def each_exam_is_in(x1, x2, x3, x4, x5, num_classes, num_slots):
    exam_is_in = True
    for i in range(num_classes):
        if x1[i] + x2[i] + x3[i] + x4[i] + x5[i] != 1:
            exam_is_in = False
            break
    return exam_is_in

def get_valid_schedules(x_list, num_classes, num_slots):
    
    x_list_final = []
    for x1 in tqdm(x_list):
        for x2 in x_list:
            for x3 in x_list:
                for x4 in x_list:
                    for x5 in x_list:
                        exam_is_in = each_exam_is_in(x1, x2, x3, x4, x5, num_classes, num_slots)
                        if exam_is_in:
                            x = (x1,x2,x3,x4,x5)
                            x_list_final.append(x)
    
    return x_list_final
    
def main(path, num_slots):
    
    sheet = load_excel_sheet(path)
    num_combos = sheet.nrows 
    # num_class_per_combo = sheet.ncols
    
    class_name_to_class_ID, class_ID_to_class_name = get_class_name_ID_dicts(sheet)
    
    class_name_combos, class_ID_combos = get_class_name_combos_class_ID_combos(sheet, class_name_to_class_ID)
    
    num_combos = sheet.nrows 
    num_class_per_combo = sheet.ncols #which is always 3
    num_classes = len(class_name_to_class_ID)
    
    class_combo_matrix = get_class_combo_matrix(class_ID_combos, num_combos, num_classes)
    
    valid_schedule_per_slot = get_valid_schedule_per_slot(class_combo_matrix, num_combos, num_classes)
    
    valid_schedules = get_valid_schedules(valid_schedule_per_slot, num_classes, num_slots)
    
    return valid_schedules

wb = xlrd.open_workbook(path) 
sheet = wb.sheet_by_index(0)
path = '/Users/erelpapo/Desktop/ERIK/class_combs.xlsx'
num_slots = 5

valid_schedules = main(path, num_slots)
