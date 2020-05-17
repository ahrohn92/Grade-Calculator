import os
import csv
from tkinter import filedialog

#
# Author: Andrew H. Rohn
# Date: 17 May 2020
# File: Class_File.py
# Desc: This module writes and reads class information to and from
#       CSV files. The results are returned to the Main.py module.
#

# Determines Current Directory for File Dialog Box
dir_path = os.path.dirname(os.path.realpath(__file__))

# Create a 'Classes' folder if One Doesn't Exist
if not os.path.exists('Classes'):
    os.makedirs('Classes')


# Retrieves Class Information from a CSV File and Returns it to Main Module
def open_file():

    class_name = ""
    category_names = []
    category_grade_weights = []
    category_num_items = []
    grades = []

    # Opens Open File Dialog Box
    file = filedialog.askopenfilename(initialdir=dir_path+"/Classes", title="Select A File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))

    # Parses CSV Class File
    try:
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row_index = 0
            for row in csv_reader:
                if row_index == 0:
                    class_name = row
                if row_index == 1:
                    category_names = row
                if row_index == 2:
                    category_grade_weights = row
                if row_index == 3:
                    category_num_items = row
                if row_index == 4:
                    grades = row
                row_index += 1
    except FileNotFoundError:
        pass

    return class_name, category_names, category_grade_weights, category_num_items, grades


# Saves Class Information to a CSV File
def save_file(class_name, category_names, category_grade_weights, category_num_items, grades):

    # Opens Save File Dialog Box
    file = filedialog.asksaveasfilename(initialdir=dir_path+"/Classes", initialfile=class_name, title="Select A File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")), defaultextension=".csv")

    # Writes Class Data to CSV File
    try:
        with open(file, mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([class_name])
            csv_writer.writerow(category_names)
            csv_writer.writerow(category_grade_weights)
            csv_writer.writerow(category_num_items)
            csv_writer.writerow(grades)
    except FileNotFoundError:
        pass
