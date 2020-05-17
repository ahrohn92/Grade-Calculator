#
# Author: Andrew H. Rohn
# Date: 4 May 2020
# File: Calculator.py
# Desc: This module calculates either a final or current grade for a class.
#       The results are returned to the Main.py module for output.
#


# Calculates Grade
def calculate_grade(grades, category_grade_weights, category_num_items):

    weights_achieved = []
    category_averages = []
    index = 0

    for x in range(0, len(category_num_items)):
        weight_achieved = 0.0
        for y in range(0, int(category_num_items[x])):
            weight_achieved += ((float(grades[index]) * (float(category_grade_weights[x]) / 100.0)) / float(category_num_items[x]))
            index += 1
        if len(category_grade_weights) != 0 and category_grade_weights[x] != 0:
            category_averages.append((float(weight_achieved)/float(category_grade_weights[x])) * 100.0)
        weights_achieved.append(weight_achieved)

    grade = 0.0

    for weight_achieved in weights_achieved:
        grade += weight_achieved

    return grade, assign_letter_grade(grade), category_averages


# Calculates Current Grade & Determines Needed Grade Avg for Desired Grade
def calculate_current_grade(grades, category_grade_weights, category_num_items):

    current_grades = []
    current_category_num_items = []
    percentage_graded = 0.0
    index = 0

    # Calculates Percent of Points that are Graded & not Graded
    for x in range(0, len(category_num_items)):
        num_items_graded = 0
        for y in range(0, int(category_num_items[x])):
            if grades[index] != '':
                num_items_graded += 1
                current_grades.append(grades[index])
            index += 1

        percentage_graded += (float(num_items_graded) * (float(category_grade_weights[x]) / float(category_num_items[x])))
        current_category_num_items.append(num_items_graded)

    percentage_graded = percentage_graded / 100.0
    percentage_not_graded = 1.0 - percentage_graded

    # Calculate Adjusted Grade Weights for each category
    adjusted_grade_weights = []

    if percentage_graded != 0:
        for x in range(0, len(category_num_items)):
            adjusted_grade_weights.append((((float(current_category_num_items[x]) / float(category_num_items[x])) * float(category_grade_weights[x])) / percentage_graded))

    # calculate current grade based on only graded assignments, passes altered copies of lists
    current_grade, current_letter_grade, current_category_averages = calculate_grade(current_grades, adjusted_grade_weights, current_category_num_items)

    desired_grade_list = [90.0, 80.0, 70.0, 60.0]
    new_desired_grade_list = []
    unachievable_grade_list = []
    needed_grade_avgs = []

    for desired_grade in desired_grade_list:

        needed_grade_avg = ((desired_grade - (current_grade * percentage_graded)) / percentage_not_graded)

        if needed_grade_avg > 100:
            unachievable_grade_list.append(desired_grade)
        elif 100.0 > needed_grade_avg > 0:
            new_desired_grade_list.append(desired_grade)
            needed_grade_avgs.append(needed_grade_avg)

    # If No Grades Are Entered, Letter Grade is 'N/A'
    if not current_grades:
        current_letter_grade = "N/A"

    return current_grade, current_letter_grade, new_desired_grade_list, unachievable_grade_list, percentage_graded, percentage_not_graded, needed_grade_avgs


# Assigns Letter Grade to Numerical Grade
def assign_letter_grade(grade):
    grade = float("{:.2f}".format(grade))
    if grade >= 90.0:
        return 'A'
    elif grade >= 80.0:
        return 'B'
    elif grade >= 70.0:
        return 'C'
    elif grade >= 60.0:
        return 'D'
    else:
        return 'F'
