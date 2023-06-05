import pytest
from api.app import db
from api.utils.utils import datetime
from tests.base_test_case import BaseTestCase
from models.lesson import Lesson, LessonStatus
from models.teacher import Teacher


class LessonModelTestCase(BaseTestCase):
    def test_create_lesson(self):
        args_for_lesson = {
            "teacher_id": 1,
            "student_id": 1,
            "from_time": datetime.datetime(2023, 4, 12, 15, 00),
            "to_time": datetime.datetime(2023, 4, 12, 17, 00),
            "space": "qevrvrever",
            "title": "Test Lesson"
        }
        lesson = Lesson.add_new_lesson(**args_for_lesson)
        lessons = Teacher.get_teacher_by_id(1).lessons_teacher
        assert lesson
        assert lessons[0] == lesson
        assert len(lessons) == 1

    def test_get_lesson_by_id(self):
        # Making sure that a lesson exists
        args_for_lesson = {
            "teacher_id": 1,
            "student_id": 1,
            "from_time": datetime.datetime(2023, 4, 13, 15, 00),
            "to_time": datetime.datetime(2023, 4, 13, 17, 00),
            "space": "qevrvrever",
            "title": "Test Lesson"
        }
        lesson = Lesson.add_new_lesson(**args_for_lesson)
        lesson = Lesson.get_lesson_by_id(1)
        assert lesson is not None
        assert lesson.id == 1

    def test_get_all_lessons_for_student(self):
        student_id = 1
        lessons = Lesson.get_all_lessons_for_student(student_id)
        assert len(lessons) > 0
        assert all([lesson.id == student_id for lesson in lessons])

    def test_get_all_lessons_for_teacher(self):
        teacher_id = 1
        lessons = Lesson.get_all_lessons_for_teacher(teacher_id)
        assert len(lessons) > 0
        assert all([lesson.teacher_id == teacher_id for lesson in lessons])

    def test_update_lesson(self):
        lesson_id = 1
        new_title = "Updated Lesson Title"
        new_description = "Updated Lesson Description"
        Lesson.update_lesson(lesson_id, title=new_title,
                             description=new_description)

        updated_lesson = Lesson.get_lesson_by_id(lesson_id)
        assert updated_lesson.title == new_title
        assert updated_lesson.description == new_description

    def test_delete_lesson(self):
        args_for_lesson = {
            "teacher_id": 1,
            "student_id": 1,
            "from_time": datetime.datetime(2023, 4, 13, 15, 00),
            "to_time": datetime.datetime(2023, 4, 13, 17, 00),
            "space": "qevrvrever",
            "title": "Test Lesson"
        }

        lesson = Lesson.add_new_lesson(**args_for_lesson)

        Lesson.delete_lesson(lesson.id)
        deleted_lesson = Lesson.get_lesson_by_id(lesson.id)
        assert deleted_lesson is None

    # def test_reschedule_lesson(self): # TODO
    #     lesson_id = 1
    #     original_lesson = Lesson.get_lesson_by_id(lesson_id)

    #     from_time = original_lesson.from_time + datetime.timedelta(hours=1)
    #     to_time = original_lesson.to_time + datetime.timedelta(hours=1)

    #     Lesson.reschedule_lesson(lesson_id, from_time, to_time)

    #     rescheduled_lesson = Lesson.get_lesson_by_id(lesson_id)
    #     assert rescheduled_lesson.from_time == from_time
    #     assert rescheduled_lesson.to_time == to_time
    #     assert rescheduled_lesson.status == LessonStatus.SCHEDULED
