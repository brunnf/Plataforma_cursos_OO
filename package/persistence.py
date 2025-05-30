import json
import os
from .user import Aluno, Professor 
from .course import Course, Aula, Exercise 

class PersistenceManager:
    def __init__(self):
        self.data_dir = 'data'
        self.users_file = os.path.join(self.data_dir, 'users.json')
        self.courses_file = os.path.join(self.data_dir, 'courses.json')
        self._initialize_data()

    def _initialize_data(self):
        os.makedirs(self.data_dir, exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump([], f)
        if not os.path.exists(self.courses_file):
            with open(self.courses_file, 'w') as f:
                json.dump([], f)

    def load_users(self):
        with open(self.users_file, 'r') as f:
            data = json.load(f)
    
        users = []
        for user_data in data:
        # Cria uma cópia para não modificar o original
            user_data_copy = user_data.copy()
        
            user_type = user_data_copy.pop('type', None)
        
            if user_type == 'Aluno':
                users.append(Aluno(**user_data_copy))
            elif user_type == 'Professor':
                users.append(Professor(**user_data_copy))
            else:
                raise ValueError(f"Tipo de usuário inválido: {user_type}")
        return users

    def save_users(self, users):
        with open(self.users_file, 'w') as f:
            json.dump([user.to_dict() for user in users], f, indent=2)

    def load_courses(self):
        with open(self.courses_file, 'r') as f:
            data = json.load(f)
    
        courses = []
        for course_data in data:
            course = Course(
                course_id=course_data['course_id'],
                title=course_data['title'],
                professor_id=course_data['professor_id']
            )
            
            for aula_data in course_data['aulas']:
                course.aulas.append(Aula(**aula_data))
            
            for exercise_data in course_data['exercises']:
                exercise = Exercise(
                    exercise_id=exercise_data['exercise_id'],
                    title=exercise_data['title'],
                    question=exercise_data['question'],
                    submissions=exercise_data.get('submissions', {}),
                    corrections=exercise_data.get('corrections', {})
                )
                course.exercises.append(exercise)
            
            courses.append(course)
        return courses

    def save_courses(self, courses):
        with open(self.courses_file, 'w') as f:
            json.dump([course.to_dict() for course in courses], f, indent=2)

    def get_next_user_id(self):
        users = self.load_users()
        if not users:
            return 1
        return max(user.user_id for user in users) + 1

    def email_exists(self, email):
        users = self.load_users()
        return any(user.email == email for user in users)