from tkinter import *
from tkinter import messagebox
import Class_File
import Calculator

#
# Author: Andrew H. Rohn
# Date: 4 May 2020
# File: Main.py
# Desc: This module constructs the GUI, handles input validation, and passes valid inputs
#       to the Calculator.py module to calculate either a final or current grade. The
#       results are then returned to this module for formatting and displaying. Finally,
#       this module interacts with the Class_File.py module to save and open class configs.
#

# Initial GUI Window Parameters
window = Tk()
window.resizable(False, False)
window.title("Grade Calculator")
window.iconbitmap('img/A+.ico')
main_frame = Frame(window)
initial_frame = Frame(window)
initial_window_width = 0
initial_window_height = 0

# Global Variables
class_name = ""
category_names = []
category_grade_weights = []
category_num_items = []
table_columns = []
grades = []
file_is_loading = False
y_coordinate = 0

# Creates Menu Bar
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=lambda: open_initial_window())
filemenu.add_command(label="Open", command=lambda: load_class_file())
filemenu.add_command(label="Save", state="disabled", command=lambda: Class_File.save_file(class_name, category_names, category_grade_weights, category_num_items, get_grades(False)))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)
window.config(menu=menubar)


# Centers Window on Screen
def center_window(is_initial_window):

    global y_coordinate

    window.update()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window.winfo_width() / 2)
    if is_initial_window:
        y_coordinate = (screen_height / 3.5) - (window.winfo_height() / 2)
    window.geometry("%dx%d+%d+%d" % (window.winfo_width(), window.winfo_height(), x_coordinate, y_coordinate))


# Opens Initial Window
def open_initial_window():

    # Removes Old Widgets if New Window
    is_new_window = False
    if len(main_frame.winfo_children()) != 0:
        is_new_window = True
        for widget in main_frame.winfo_children():
            widget.destroy()
    if len(initial_frame.winfo_children()) != 0:
        is_new_window = True
        for widget in initial_frame.winfo_children():
            widget.destroy()

    # Initial Window Widgets
    upper_frame = Frame(initial_frame)
    class_name_label = Label(upper_frame, text="Name of Class: ", font="Verdana 13").grid(row=0, column=0)
    num_categories_label = Label(upper_frame, text="Number of Grading Categories: ", font="Verdana 13").grid(row=1, column=0)
    class_name_entry = Entry(upper_frame, justify="center", font="Verdana 13")
    num_categories_entry = Entry(upper_frame, justify="center", font="Verdana 13")
    if file_is_loading:
        class_name_entry.insert(0, class_name)
        num_categories_entry.insert(0, str(len(category_names)))
    class_name_entry.grid(row=0, column=1)
    num_categories_entry.grid(row=1, column=1)
    upper_frame.pack(padx=10, pady=10)
    submit = Button(initial_frame, text="Create Categories", bg="SteelBlue3", fg="white", font="Verdana 13", command=lambda: check_initial_entries(class_name_entry.get(), num_categories_entry.get())).pack(pady=10)
    initial_frame.pack()
    center_window(True)

    # Resize and Center if New Window
    global initial_window_width
    global initial_window_height
    if not is_new_window:
        initial_window_width = window.winfo_width()
        initial_window_height = window.winfo_height()
    else:
        window.geometry("%dx%d" % (initial_window_width, initial_window_height))
        center_window(True)

    # Disables Save Option in Menu Bar
    filemenu.entryconfig(2, state=DISABLED)


open_initial_window()


# Validates Input for Class Name & Number of Categories
def check_initial_entries(class_name_entry, num_categories_entry):

    class_name_is_valid = False
    num_categories_is_valid = False

    entry = class_name_entry.strip()
    if len(entry) == 0:
        messagebox.showerror(title="ERROR", message="No class name is specified")
        class_name_is_valid = False
    else:
        global class_name
        class_name = entry
        class_name_is_valid = True

    entry = num_categories_entry.strip()
    if len(entry) == 0:
        messagebox.showerror(title="ERROR", message="No number of assignment categories is specified")
        num_categories_is_valid = False
    else:
        try:
            num_categories = int(entry)
            if num_categories > 0:
                if num_categories <= 9:
                    num_categories_is_valid = True
                else:
                    messagebox.showerror(title="ERROR", message="Number of assignment categories cannot exceed 9")
                    num_categories_is_valid = False
            else:
                messagebox.showerror(title="ERROR", message="Number of assignment categories must be larger than 0")
                num_categories_is_valid = False
        except ValueError:
            messagebox.showerror(title="ERROR", message="'" + entry + "' is not a valid integer")
            num_categories_is_valid = False

    if class_name_is_valid and num_categories_is_valid:
        open_category_window(num_categories)


# Opens Category Window
def open_category_window(num_categories):

    window.geometry("")

    # clears widgets
    num_frames = 0
    for widget in main_frame.winfo_children():
        widget.destroy()

    # initial_frame.pack_forget()  # frame is saved for later but not used (back button?)
    main_frame.pack()
    category_main_frame = Frame(main_frame)

    category_frames = []
    category_row_frames = []

    # Determines How Many Rows are Needed for Category Frames
    num_frame_rows = 0
    if num_categories < 4:
        num_frame_rows = 1
    elif 4 <= num_categories < 7:
        num_frame_rows = 2
    elif 7 <= num_categories < 10:
        num_frame_rows = 3

    # Creation of category row frames
    for x in range(0, num_frame_rows):
        category_row_frame = Frame(category_main_frame)
        category_row_frames.append(category_row_frame)

    # Creates the Category Frames & Assigns them to Category Rows
    row_index = 0
    for x in range(0, num_categories):
        if x == 2 and num_categories == 4:
            row_index += 1
        if x == 5 and num_categories == 7:
            row_index += 1
        if x != 0 and x % 3 == 0:
            if num_categories != 4 and not (x == 6 and num_categories == 7):
                row_index += 1

        category_frame = Frame(category_row_frames[row_index], bg="gainsboro")
        category_frames.append(category_frame)

    # then creates widgets for each category frame in list
    category_font = "Verdana 13"
    i = 0
    for category_frame in category_frames:
        Label(category_frame, text="Category " + str(i + 1), width=50, bg="SteelBlue3", fg="white", font=category_font +" bold").grid(row=0, column=0, columnspan=2)
        Label(category_frame, text="Name of Category: ", bg="gainsboro", font=category_font).grid(row=1, column=0)
        category_name_entry = Entry(category_frame, justify="center", font=category_font)
        Label(category_frame, text="Grade Weight (%): ", bg="gainsboro", font=category_font).grid(row=2, column=0)
        category_grade_weight_entry = Entry(category_frame, justify="center", font=category_font)
        Label(category_frame, text="Number of Assignments: ", bg="gainsboro", font=category_font).grid(row=3, column=0)
        category_num_items_entry = Entry(category_frame, justify="center", font=category_font)
        if file_is_loading:
            category_name_entry.insert(0, category_names[i])
            category_grade_weight_entry.insert(0, category_grade_weights[i])
            category_num_items_entry.insert(0, category_num_items[i])
        category_name_entry.grid(row=1, column=1)
        category_grade_weight_entry.grid(row=2, column=1)
        category_num_items_entry.grid(row=3, column=1)

        i += 1

    # Add category rows to screen
    for x in range(0, num_frame_rows):
        category_row_frames[x].pack(pady=10)

    # Add all category frames
    for category_frame in category_frames:
        category_frame.pack(side=LEFT, padx=10)

    category_main_frame.pack()
    Button(main_frame, text="Create Input Table", bg="SteelBlue3", fg="white", font="Verdana 13", command=lambda: define_categories(category_frames)).pack(pady=10)

    center_window(False)

    # Disables Save Option in Menu Bar
    filemenu.entryconfig(2, state=DISABLED)


# Sorts User Category Inputs into Various Lists
def define_categories(category_frames):

    category_names.clear()
    category_grade_weights.clear()
    category_num_items.clear()

    entry_count = 0

    for frame in category_frames:
        for child in frame.winfo_children():
            if child.winfo_class() == 'Entry':
                if entry_count == 0:
                    category_names.append(child.get().strip())
                if entry_count == 1:
                    category_grade_weights.append(child.get().strip())
                if entry_count == 2:
                    category_num_items.append(child.get().strip())
                entry_count += 1
                if entry_count > 2:
                    entry_count = 0

    # Validate Category Names
    category_names_are_valid = True

    duplicate_string = ""
    index = 0
    for category_name in category_names:
        if len(category_name) == 0:
            messagebox.showerror(title="ERROR", message="Category "+str(index+1)+" does not have a name")
            category_names_are_valid = False
            break
        if len(category_name) > 20:
            messagebox.showerror(title="ERROR", message="'"+category_name+"'\nexceeds the 20 character limit for names")
            category_names_are_valid = False
            break

        # Compare each name to other names for duplicates
        for x in range(0, len(category_names)):
            if x != index:
                if category_name == category_names[x] and duplicate_string == "":
                    messagebox.showerror(title="ERROR", message="Category "+str(x+1)+" cannot have the same name as Category "+str(index+1))
                    duplicate_string = category_name
                    category_names_are_valid = False
        index += 1

    # Validate Grade Weights
    grade_weights_are_valid = True
    grade_weight_sum = 0

    index = 0
    for gradeWeight in category_grade_weights:
        if len(gradeWeight) == 0:
            messagebox.showerror(title="ERROR", message="Category "+str(index+1)+" does not have a grade weight")
            grade_weights_are_valid = False
            break
        try:
            temp = float(gradeWeight)
            if temp <= 0:
                messagebox.showerror(title="ERROR", message="A grade's weight must be larger than 0")
                grade_weights_are_valid = False
                break
            if temp > 100:
                messagebox.showerror(title="ERROR", message="A grade's weight cannot exceed 100 %")
                grade_weights_are_valid = False
                break
            grade_weight_sum += temp
        except ValueError:
            messagebox.showerror(title="ERROR", message="'" + gradeWeight + "' is not a valid number")
            grade_weights_are_valid = False
            break
        index += 1

    if grade_weights_are_valid:
        if grade_weight_sum != 100.0:
            messagebox.showerror(title="ERROR", message="The sum of the grade weights is "+str(grade_weight_sum)+" %\nThey must add up to 100 %")
            grade_weights_are_valid = False

    # Validate Number of Items
    num_items_are_valid = True

    index = 0
    for itemQuantity in category_num_items:
        if len(itemQuantity) == 0:
            messagebox.showerror(title="ERROR", message="Category "+str(index+1)+" does not have the number of assignments")
            num_items_are_valid = False
            break
        try:
            temp = int(itemQuantity)
            if temp <= 0:
                messagebox.showerror(title="ERROR", message="Number of items must be larger than 0")
                num_items_are_valid = False
                break
            if temp > 20:
                messagebox.showerror(title="ERROR", message="Number of items cannot exceed 20")
                num_items_are_valid = False
                break
        except ValueError:
            messagebox.showerror(title="ERROR", message="'" + itemQuantity + "' is not a valid integer")
            num_items_are_valid = False
            break
        index += 1

    # If All Inputs are Valid, Move onto Grade Insertion
    if category_names_are_valid and grade_weights_are_valid and num_items_are_valid:
        open_grade_input_window()


# Opens Grade Input Window
def open_grade_input_window():

    window.geometry("")

    num_frames = 0

    # clears widgets
    for widget in main_frame.winfo_children():
        if widget.winfo_class() == 'Frame':
            if num_frames >= 1:
                widget.destroy()
            else:
                num_frames += 1

    grade_input_frame = Frame(main_frame)

    # Label(grade_input_frame, text="Enter Grades").pack()
    table_frame = Frame(grade_input_frame)

    # determines number of rows by maximum value of number of assignments
    num_rows = 1
    for item_quantity in category_num_items:
        if int(item_quantity) > num_rows:
            num_rows = int(item_quantity)

    # insert initial assignment number frame
    table_columns.clear()
    table_columns.append(Frame(table_frame))

    # add category frames
    for x in range(0, len(category_names)):
        table_columns.append(Frame(table_frame))

    # places all frames in a single row
    for x in range(0, len(table_columns)):
        table_columns[x].grid(row=0, column=x, sticky=W + N)

    # create widgets for item num frame
    Label(table_columns[0], text="Assignment\nNumber", height=2, font="Verdana 13", bg="dim gray", fg="white").grid(row=0, column=0)
    for x in range(0, num_rows):
        Label(table_columns[0], text=str(x + 1), height=1).grid(row=(x + 1), column=0, pady=(3, 0))

    # then creates widgets for each frame in list
    grade_index = 0
    entry_font = ('Verdana', 13)
    for x in range(1, len(table_columns)):
        Label(table_columns[x], text=category_names[x - 1]+"\n("+'{:.2f}'.format(float(category_grade_weights[x-1])/float(category_num_items[x-1])).rstrip('0').rstrip('.')+"% ea)",
              height=2, width=20, font=entry_font, bg="SteelBlue3", fg="white").grid(row=0, column=0)
        for y in range(0, num_rows):
            if y < int(category_num_items[x - 1]):
                grade_entry = Entry(table_columns[x], font=entry_font, justify="center")
                if file_is_loading:
                    grade_entry.insert(0, grades[grade_index])
                    grade_index += 1
                grade_entry.grid(row=(y + 1), column=0)
            else:
                Entry(table_columns[x], state="disabled", bg="gainsboro", font=entry_font).grid(row=(y + 1), column=0)

    table_frame.pack(padx=20, pady=10)
    Button(grade_input_frame, text="Calculate Grade", bg="SteelBlue3", fg="white", font="Verdana 13", command=lambda: get_grades(True)).pack(pady=10)
    grade_input_frame.pack()

    if len(category_num_items) > 7:
        center_window(False)

    # Enables Save Option in Menu Bar
    filemenu.entryconfig(2, state=ACTIVE)


# Gets Grades from Entries
def get_grades(isCalculation):
    grades.clear()
    grades_are_valid = True
    all_grades_are_present = True

    for frame in table_columns:
        for child in frame.winfo_children():
            if child.winfo_class() == 'Entry' and child.cget('state') == 'normal':
                grade = child.get().strip()
                grades.append(grade)

                if not grade:
                    all_grades_are_present = False
                else:
                    try:
                        temp = float(grade)
                        if temp < 0:
                            messagebox.showerror(title="ERROR", message="An assignment score cannot be less than 0")
                            child.delete(0, END)
                            grades_are_valid = False
                            break
                    except ValueError:
                        messagebox.showerror(title="ERROR", message="'" + grade + "' is not a valid number")
                        child.delete(0, END)
                        grades_are_valid = False
                        break

    # Directs Grades for Either Calculation or Save File
    if isCalculation:
        validate_grades(grades, grades_are_valid, all_grades_are_present)
    else:
        return grades


# Validate Grade Entries
def validate_grades(grades, grades_are_valid, all_grades_are_present):

    # Calculate Grades & Output Results (IF VALID)
    if grades_are_valid:
        if all_grades_are_present:
            final_grade, final_letter_grade, category_averages = Calculator.calculate_grade(grades, category_grade_weights, category_num_items)

            # Formats Final Grade Output
            message = "Percentage: {:.2f}".format(final_grade).rstrip('0').rstrip('.')
            message += " %\nLetter Grade: "+final_letter_grade+"\n\n"
            for x in range(0, len(category_averages)):
                message += "Average '"+category_names[x]+"' score was {:.2f}".format(category_averages[x]).rstrip('0').rstrip('.')
                message += " %\n"
            messagebox.showinfo(title="Final Grade", message=message)
        else:
            current_grade, current_letter_grade, new_desired_grade_list, unachievable_grade_list, percentage_graded, percentage_not_graded, needed_grade_avgs \
                = Calculator.calculate_current_grade(grades, category_grade_weights, category_num_items)

            # Formats Current Grade Output
            message = "Percentage: {:.2f}".format(current_grade).rstrip('0').rstrip('.')
            message += " %\nLetter Grade: "+current_letter_grade+"\n\n"
            for x in range(0, len(unachievable_grade_list)):
                message += "Not enough remaining points to get a '"+Calculator.assign_letter_grade(unachievable_grade_list[x])+"' ({:.2f}".format(unachievable_grade_list[x]).rstrip('0').rstrip('.')
                message += " %)\n"
            for x in range(0, len(needed_grade_avgs)):
                message += "Need avg of {:.2f}".format(needed_grade_avgs[x]).rstrip('0').rstrip('.')
                message += " % on remaining items to get a '"+Calculator.assign_letter_grade(new_desired_grade_list[x])+"' ({:.2f}".format(new_desired_grade_list[x]).rstrip('0').rstrip('.')
                message += " %)\n"
            if len(unachievable_grade_list) == 0 and len(needed_grade_avgs) == 0:
                message += "Congratulations!\nYou will receive an 'A' whether you complete the remaining assignments or not\n"
            message += "\nPercent of points allotted: {:.2f}".format(percentage_graded*100).rstrip('0').rstrip('.')
            message += " %\nPercent of points remaining: {:.2f}".format(percentage_not_graded*100).rstrip('0').rstrip('.')
            message += " %\n"
            messagebox.showinfo(title="Current Grade", message=message)


# Takes Data from Class File and Assigns to Global Variables
def load_class_file():

    temp_class_name, temp_category_names, temp_category_grade_weights, temp_category_num_items, temp_grades = Class_File.open_file()

    global class_name
    global category_names
    global category_grade_weights
    global category_num_items
    global grades
    global file_is_loading

    class_name = temp_class_name[0]
    category_names = temp_category_names
    category_grade_weights = temp_category_grade_weights
    category_num_items = temp_category_num_items
    grades = temp_grades
    file_is_loading = True

    open_initial_window()
    open_category_window(len(category_names))
    open_grade_input_window()

    file_is_loading = False


# main loop of the program
window.mainloop()
