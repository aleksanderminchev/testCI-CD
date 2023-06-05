from models.teacher import Teacher


def get_matching_tutors(hard_filters, soft_filters):
    """
    Gets the matching tutors and formats the output.
    Starts off by filtering off everything in hard filters.

    Then sorts the soft filters in the following order:
    1. Fluent language
    2. Type of high school
    3. Age
    4. Math program
    5. Extra subjects
    6. Grade average
    7. Special needs / qualifications
    8. Number of students tutor already has
    9. Number of total hours tutor has taught
    10. Interests
    11. Gender
    """

    # Apply the hard filters.
    matching_tutors = Teacher.get_tutors_by_filters(hard_filters)

    # import pprint
    # pprint.pprint(matching_tutors)

    # ALGORITHM PRIORITY
    # 11. GENDER
    if "gender" in soft_filters.keys():
        matching_tutors_positive = [
            tutor for tutor in matching_tutors if tutor["gender"] == soft_filters["gender"]]
        matching_tutors_false = [
            tutor for tutor in matching_tutors if tutor["gender"] != soft_filters["gender"]]
        matching_tutors = matching_tutors_positive + matching_tutors_false

    # 10. INTERESTS
    if "interests" in soft_filters.keys():
        matching_tutors_positive = [tutor for tutor in matching_tutors if all(
            x in tutor["interests"] for x in soft_filters["interests"])]
        if len(matching_tutors_positive) == 0:
            matching_tutors_positive = [tutor for tutor in matching_tutors if all(
                x in tutor["interests"] for x in soft_filters["interests"][0:1])]
            matching_tutors_false = [tutor for tutor in matching_tutors if all(
                x not in tutor["interests"] for x in soft_filters["interests"][0:1])]
        else:
            matching_tutors_false = [tutor for tutor in matching_tutors if all(
                x not in tutor["interests"] for x in soft_filters["interests"])]
        matching_tutors = matching_tutors_positive + matching_tutors_false

    # 9 AMOUNT OF TOTAL HOURS THAT THE TUTOR HAS
    # matching_tutors = sorted(matching_tutors, key=lambda i: i['hours'])

    # # 8 AMOUNT OF STUDENTS THE TUTOR HAS
    # matching_tutors = sorted(matching_tutors, key=lambda i: len(i['students']))

    # 7 SPECIAL NEEDS/QUALIFICATIONS
    if "qualifications" in soft_filters.keys():
        matching_tutors_positive = [tutor for tutor in matching_tutors if all(
            x in tutor["qualifications"] for x in soft_filters["qualifications"])]
        if len(matching_tutors_positive) == 0:
            matching_tutors_positive = [tutor for tutor in matching_tutors if all(
                x in tutor["qualifications"] for x in soft_filters["qualifications"][0:1])]
            matching_tutors_false = [tutor for tutor in matching_tutors if all(
                x not in tutor["qualifications"] for x in soft_filters["qualifications"][0:1])]
        else:
            matching_tutors_false = [tutor for tutor in matching_tutors if all(
                x not in tutor["qualifications"] for x in soft_filters["qualifications"])]
        matching_tutors = matching_tutors_positive + matching_tutors_false

    # 6. grade average
    if "grade_average" in soft_filters.keys():
        matching_tutors_positive = [
            tutor for tutor in matching_tutors if tutor["grade_average"] == soft_filters["grade_average"]]
        matching_tutors_false = [
            tutor for tutor in matching_tutors if tutor["grade_average"] != soft_filters["grade_average"]]
        matching_tutors = matching_tutors_positive + matching_tutors_false

    # 5. EXTRA SUBJECTS
    if "extra_subjects" in soft_filters.keys():
        matching_tutors_positive = [tutor for tutor in matching_tutors if all(
            x in tutor["subjects"] for x in soft_filters["subjects"])]
        if len(matching_tutors_positive) == 0:
            matching_tutors_positive = [tutor for tutor in matching_tutors if all(
                x in tutor["subjects"] for x in soft_filters["subjects"][0:1])]
            matching_tutors_false = [tutor for tutor in matching_tutors if all(
                x not in tutor["subjects"] for x in soft_filters["subjects"][0:1])]
        else:
            matching_tutors_false = [tutor for tutor in matching_tutors if all(
                x not in tutor["subjects"] for x in soft_filters["subjects"][0:1])]
        matching_tutors = matching_tutors_positive + matching_tutors_false

    # 4. MATH PROGRAM
    if "programs" in soft_filters.keys():
        matching_tutors_positive = [tutor for tutor in matching_tutors if all(
            x in tutor["programs"] for x in soft_filters["programs"])]
        # If no one matches the program criteria it might be that there are many programs, so let's at least find a tutor that knows the first program.
        if len(matching_tutors_positive) == 0:
            matching_tutors_positive = [tutor for tutor in matching_tutors if all(
                x in tutor["programs"] for x in soft_filters["programs"][0:1])]
            matching_tutors_false = [tutor for tutor in matching_tutors if all(
                x not in tutor["programs"] for x in soft_filters["programs"][0:1])]
        else:
            matching_tutors_false = [tutor for tutor in matching_tutors if all(
                x not in tutor["programs"] for x in soft_filters["programs"])]
        matching_tutors = matching_tutors_positive + matching_tutors_false

    # 3. AGE
    if "age" in soft_filters.keys():
        matching_tutors_positive = [
            tutor for tutor in matching_tutors if tutor["age"] == soft_filters["age"].split(" ")[-1]]
        matching_tutors_false = [
            tutor for tutor in matching_tutors if tutor["age"] != soft_filters["age"].split(" ")[-1]]
        matching_tutors = matching_tutors_positive + matching_tutors_false

    # 2. TYPE GYM
    if "high_school" in soft_filters.keys():
        matching_tutors_positive = [
            tutor for tutor in matching_tutors if tutor["high_school"] == soft_filters["high_school"]]
        matching_tutors_false = [
            tutor for tutor in matching_tutors if tutor["high_school"] != soft_filters["high_school"]]
        matching_tutors = matching_tutors_positive + matching_tutors_false

        # matching_tutors = sorted(matching_tutors, key = lambda i: i.get("high_school", soft_filters["high_school"]), reverse=True)

    # 1. FLUENT LANGUAGE
    if "languages" in soft_filters.keys():
        matching_tutors_positive = [tutor for tutor in matching_tutors if all(
            x in tutor["languages"] for x in soft_filters["languages"])]
        if len(matching_tutors_positive) == 0:
            matching_tutors_positive = [tutor for tutor in matching_tutors if all(
                x in tutor["languages"] for x in soft_filters["languages"][0:1])]
            matching_tutors_false = [tutor for tutor in matching_tutors if all(
                x not in tutor["languages"] for x in soft_filters["languages"][0:1])]
        else:
            matching_tutors_false = [tutor for tutor in matching_tutors if all(
                x not in tutor["languages"] for x in soft_filters["languages"])]
        matching_tutors = matching_tutors_positive + matching_tutors_false

    return matching_tutors
