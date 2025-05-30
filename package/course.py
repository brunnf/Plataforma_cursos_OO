class Aula:
    def __init__(self, aula_id, title, content):
        self.aula_id = aula_id
        self.title = title
        self.content = content

    def to_dict(self):
        return {
            'aula_id': self.aula_id,
            'title': self.title,
            'content': self.content
        }

class Exercise:
    def __init__(self, exercise_id, title, question, submissions=None, corrections=None):
        self.exercise_id = exercise_id
        self.title = title
        self.question = question
        self.submissions = submissions or {} 
        self.corrections = corrections or {}  

    def to_dict(self):
        return {
            'exercise_id': self.exercise_id,
            'title': self.title,
            'question': self.question,
            'submissions': self.submissions,
            'corrections': self.corrections
        }
class Course:
    def __init__(self, course_id, title, professor_id):
        self.course_id = course_id
        self.title = title
        self.professor_id = professor_id
        self.aulas = []
        self.exercises = []

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'title': self.title,
            'professor_id': self.professor_id,
            'aulas': [aula.to_dict() for aula in self.aulas],
            'exercises': [exercise.to_dict() for exercise in self.exercises]
        }