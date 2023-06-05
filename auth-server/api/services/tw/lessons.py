from api.services.tw import tw_api_utils
import pickle


def get_lessons():
    """ Gets a list of all the lessons on Teachworks and saves them as a pickle. """
    # Kør kun denne x gange om dagen
    lessons_data = tw_api_utils.get_lessons()
    pickle.dump(lessons_data, open("pickles/lessons_raw.p", "wb"))


def calculate_tutor_lesson_hours():
    """
    From list of lessons count how many hours each tutor has taught.
    Results are saved as a pickle containing a dictionary with key being employee ID and value being the aggregated amount of minutes.
    """
    lessons_data = pickle.load(open("pickles/lessons_raw.p", "rb"))
    # lessons_list = []
    # tutor_total_duration = None
    tutor_hours = {}  # key being employee ID and value being the aggregated amount of minutes
    lesson_list = []

    for lesson in lessons_data:  # each item in list of lesson_data contains a dictionary with data of that specific lesson.
        # make sure that item is a dictionary.
        if isinstance(lesson, dict):
            lesson_status = lesson["status"]
            if lesson_status == "Attended":  # only count attended lessons.
                tutor_id = lesson["employee_id"]
                lesson_duration = int(lesson["duration_minutes"])
                if tutor_id in tutor_hours:  # if tutor already exists add the duration of this lesson too
                    # print(tutor_hours[tutor_id], "Tutor findes allerede")
                    tutor_hours[tutor_id] = tutor_hours[tutor_id] + lesson_duration
                else:  # else if tutor does not exist add this tutor to the dictionary.
                    tutor_hours[tutor_id] = lesson_duration
                    # print(tutor_hours[tutor_id], "Tutor findes ikke")
    sort_and_dump(tutor_hours, lesson_list)


def sort_and_dump(tutor_hours, lesson_list):
    """Sort the dictionary, and dump it in a pickle"""
    sorted(tutor_hours, key=tutor_hours.get, reverse=True)  # Sort the list, by amount of hours
    for tutor_id, hours in tutor_hours.items():  # Loop through every element in dict
        data = {
            "id": tutor_id,
            "hours": hours / 60
        }
        lesson_list.append(data)
        pickle.dump(lesson_list, open("pickles/lessons_filtered.p", "wb"))


def update_and_calculate_lesson_hours():
    """
    Updates and calculates lessons hours by getting a list of all lessons from TW and saves them as a picle.
    Then, goes through the pickle to calculate the total hours of lessons for each tutor, which is updated in lessons_filtered.p
    """
    get_lessons()
    calculate_tutor_lesson_hours()


if __name__ == "__main__":
    # get_lessons()
    calculate_tutor_lesson_hours()
