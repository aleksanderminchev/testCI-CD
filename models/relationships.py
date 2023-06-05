from api.app import db

tutor_subject = db.Table(
    "tutor_subject",
    db.Column("Tutor", db.Integer, db.ForeignKey("tutor.uid")),
    db.Column("Subjects", db.Integer, db.ForeignKey("subjects.uid"))
)
