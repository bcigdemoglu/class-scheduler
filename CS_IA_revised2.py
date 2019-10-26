import numpy as np    
from tqdm import tqdm
import xlrd
from copy import deepcopy


valid_schedules = []
all_valid_schedules = []
class_name_to_class_ID = {}
class_ID_to_class_name = {}
class_names = set() 
class_name_combos = []
class_ID_combos = []

def get_class_name_ID_dicts(excel_data):
    
    global class_names, class_name_to_class_ID, class_ID_to_class_name
    
    class_combos = excel_data.split('\n')
    for class_combo in class_combos:
        classes = class_combo.split('\t')
        for c in classes:
            class_names.add(c)
            
    class_ID = 0
    for class_name in class_names:
        class_name_to_class_ID[str(class_name)] = class_ID
        class_ID += 1

    class_ID_to_class_name = {v: k for k, v in class_name_to_class_ID.items()}
    
def get_class_name_combos_class_ID_combos(excel_data):

    global class_name_combos, class_ID_combos
    
    class_combos = excel_data.split('\n')
    for class_combo in class_combos:
        classes = class_combo.split('\t')
        class_name_combo = []
        class_ID_combo = []
        for c in classes:
            class_name_combo.append(c)
            class_ID_combo.append(class_name_to_class_ID[c])
            
        class_name_combos.append(class_name_combo)
        class_ID_combos.append(class_ID_combo)

def get_class_combo_matrix(num_combos, num_classes):
    
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

def each_exam_is_in(x1, x2, x3, x4, x5, num_classes):
    exam_is_in = True
    for i in range(num_classes):
        if x1[i] + x2[i] + x3[i] + x4[i] + x5[i] != 1:
            exam_is_in = False
            break
    return exam_is_in

def get_valid_schedules(x_list, num_classes):
    
    x_list_final = []
    for x1 in tqdm(x_list):
        for x2 in x_list:
            for x3 in x_list:
                for x4 in x_list:
                    for x5 in x_list:
                        exam_is_in = each_exam_is_in(x1, x2, x3, x4, x5, num_classes)
                        if exam_is_in:
                            x = (x1,x2,x3,x4,x5)
                            x_list_final.append(x)
    
    return x_list_final

def load_classes(excel_data, slot_count_):
    """
    Load classes for a given excel_data string,
    containing 3 columns on each line separated by tabs.
    Load the schedule to a global variable for later access.
    E.g:
    Classname1 <tab> ClassName2 <tab> ClassName3
    Classname4 <tab> ClassName5 <tab> ClassName6
    """
    
    global slot_count, valid_schedules, all_valid_schedules
    slot_count = slot_count_
    
    get_class_name_ID_dicts(excel_data)
    get_class_name_combos_class_ID_combos(excel_data)
    
    num_combos = len(class_name_combos)
    num_class_per_combo = len(class_name_combos[0]) #which is always 3
    num_classes = len(class_name_to_class_ID)
    
    class_combo_matrix = get_class_combo_matrix(num_combos, num_classes)
    
    valid_schedule_per_slot = get_valid_schedule_per_slot(class_combo_matrix, num_combos, num_classes)
    
    valid_schedules = get_valid_schedules(valid_schedule_per_slot, num_classes)
    all_valid_schedules = deepcopy(valid_schedules)
    
    return

def get_potential_classes_for_slot(slot_number):
    """
    Get the names of exams available to pick for a given slot_number
    Returns list of names of exams.
    """
    
    potential_classes = set()
    for valid_schedule in valid_schedules:
        slot = valid_schedule[slot_number]
        for i in range(len(slot)):
            if slot[i] == 1:
                class_name = class_ID_to_class_name[i]
                potential_classes.add(class_name)
                
    return list(potential_classes)

def select_class_for_slot(class_name, slot_number):
    """
    Select a class_name for a certain slot_number.
    Class name is selected from one of get_potential_classes_for_slot(slot_number)
    Do the necessary manipulation
    """
    global valid_schedules
    valid_schedules_new = []
    
    class_ID = class_name_to_class_ID[class_name]
    for valid_schedule in valid_schedules:
        slot = valid_schedule[slot_number]
        if slot[class_ID] == 1:
            valid_schedules_new.append(valid_schedule)
    
    valid_schedules = deepcopy(valid_schedules_new)
    
    return 

def reset_selections():
    """
    Resets all made selection, returning to initial state
    """
    
    global valid_schedules
    
    valid_schedules = deepcopy(all_valid_schedules)
    
    return

def get_all_potential_classes():
    """
    Returns a dictonary of potential classes for all slots
    {
        [slot_number]: [...classes_available]
        ...
    }
    """

    return
    

# excel_data = 'Physics\tChemistry\tBusiness\nPhysics\tChemistry\tEcon\nPhysics\tCS\tEcon\nChemistry\tBiology\tEcon'
# slot_count_ = 5

