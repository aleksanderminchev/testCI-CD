from api.services.tw import tw_api_utils
import pickle
from collections import Counter


def get_matching_tutor_by_student():
    """
    Gets all the tutors from a students and counts the active tutors.
    """
    students = tw_api_utils.get_tutor_students()  # gets list of all active students with a dict of their data.
    active_tutor_ids = []

    # Check all active students and find their tutors.
    for student in students:
        if student["default_teachers"] is not []:
            # For each tutor that the student has append the tutor's ID
            for tutor in student["default_teachers"]:
                active_tutor_ids.append(tutor["id"])

    # Get all the tutor IDs that currently is teaching a student
    unique_keys = Counter(active_tutor_ids).keys()
    # Count the times the tutor appears.
    count_unique_keys = Counter(active_tutor_ids).values()

    # Zip the unique tutor IDs and the counter into a dict with the ID as key and counter as value.
    active_tutor_ids_counter = dict(zip(unique_keys, count_unique_keys))
    pickle.dump(active_tutor_ids_counter, open("pickles/tutors_with_students.p", "wb"))

    return active_tutor_ids_counter


def get_tutor_students():
    """
    Saves a pickle with the amount of students that each tutor has.
    """
    tutor_amount_of_students = []
    students = get_matching_tutor_by_student()

    for k, v in students.items():
        data = {
            "id": k,
            "students": v
        }
        tutor_amount_of_students.append(data)

        tutor_amount_of_students = sorted(tutor_amount_of_students, key=lambda i: i["students"])

        pickle.dump(tutor_amount_of_students, open("pickles/sorted_amount_of_students.p", "wb"))


if __name__ == "__main__":
    get_matching_tutor_by_student()
