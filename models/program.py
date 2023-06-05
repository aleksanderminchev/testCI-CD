from api.app import db
from api.utils.utils import Updateable
from models.user import User
from flask import abort


teachers_programs = db.Table('teacher_programs',
                             db.Column('program_id', db.Integer, db.ForeignKey(
                                 'program.uid'), primary_key=True, index=True),
                             db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'),
                              primary_key=True, index=True))


class Program(Updateable, db.Model):  # type:ignore

    __tablename__ = "program"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    teachers = db.relationship("Teacher", secondary=teachers_programs, primaryjoin=(
        teachers_programs.c.program_id == uid), backref='programs')

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.uid
        }

    @staticmethod
    def get_program_by_id(id):
        return Program.query.get(id)

    @staticmethod
    def update_program(id=int, **kwargs):
        """Updates a program by the User id from the DB"""
        program_query = Program.query.get(id)
        Program.update(program_query, kwargs)
        db.session.commit()
        return program_query

    @staticmethod
    def add_new_program(**kwargs):
        """ Adds a new program to the DB. TODO """
        program = Program(**kwargs)
        db.session.add(program)
        db.session.commit()
        return program.to_dict()

    @staticmethod
    def delete_program(id=str):
        """Deletes a program from the DB"""
        program = Program.query.get(id) or abort(404)
        db.session.delete(program)
        db.session.commit()
        return program

    @staticmethod
    def add_program_to_teacher(teacher, program_id):
        program = Program.get_program_by_id(program_id)
        programs = teacher.programs
        if program not in programs:
            programs.append(program)
            db.session.commit()
            return program

    @staticmethod
    def remove_program_from_teacher(teacher_email, program_id):
        teacher_user = User.find_by_email(teacher_email)
        program = Program.get_program_by_id(program_id)
        programs = teacher_user.teacher.programs
        if program not in programs:
            abort(500)
        programs.remove(program)
        db.session.add(teacher_user)
        db.session.commit()
        return program
