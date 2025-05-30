import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from .course import Course, Aula, Exercise
from .user import Aluno, Professor

class ProfessorGUI(tk.Tk):
    def __init__(self, professor, persistence):
        super().__init__()
        self.professor = professor
        self.persistence = persistence
        self.courses = [c for c in persistence.load_courses() if c.professor_id == professor.user_id]
        self.current_course = None  
        self._setup_ui()

    def _setup_ui(self):
        self.title(f"Professor: {self.professor.name}")
        self.geometry("1200x800")
        
        # Toolbar
        toolbar = ttk.Frame(self)
        ttk.Button(toolbar, text="Novo Curso", command=self._create_course).pack(side=tk.LEFT, padx=5)
        self.delete_course_btn = ttk.Button(
            toolbar, 
            text="Excluir Curso", 
            command=self._delete_course,
            state=tk.DISABLED
        )
        self.delete_course_btn.pack(side=tk.LEFT, padx=5)
        toolbar.pack(fill=tk.X, pady=5)
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista de Cursos
        course_frame = ttk.LabelFrame(main_frame, text="Cursos")
        course_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.course_listbox = tk.Listbox(course_frame, width=30, height=20)
        self.course_listbox.pack(fill=tk.Y, padx=5, pady=5)
        
        # Carregar cursos
        for course in self.courses:
            self.course_listbox.insert(tk.END, course.title)
        
        # Frame de Edição
        self.editor_frame = ttk.Frame(main_frame)
        self.editor_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.course_listbox.bind('<<ListboxSelect>>', self._load_course_editor)

    def _create_course(self):
        title = simpledialog.askstring("Novo Curso", "Nome do Curso:")
        if title:
            course_id = max(c.course_id for c in self.courses) + 1 if self.courses else 1
            new_course = Course(
                course_id=course_id,
                title=title,
                professor_id=self.professor.user_id
            )
            self.courses.append(new_course)
            self.course_listbox.insert(tk.END, title)
            self.persistence.save_courses(self.courses)
            messagebox.showinfo("Sucesso", "Curso criado com sucesso!")

    def _delete_course(self):
        if not self.current_course:
            return
            
        if messagebox.askyesno(
            "Confirmar Exclusão", 
            f"Tem certeza que deseja excluir o curso '{self.current_course.title}'?"
        ):
            # Remove o curso da lista
            index = self.course_listbox.curselection()[0]
            self.course_listbox.delete(index)
            self.courses.remove(self.current_course)
            
            # Limpa o editor
            for widget in self.editor_frame.winfo_children():
                widget.destroy()
                
            self.current_course = None
            self.delete_course_btn.config(state=tk.DISABLED)
            self.persistence.save_courses(self.courses)
            messagebox.showinfo("Sucesso", "Curso excluído com sucesso!")

    def _load_course_editor(self, event):
        selection = self.course_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        self.current_course = self.courses[index]
        self.delete_course_btn.config(state=tk.NORMAL)
       
        for widget in self.editor_frame.winfo_children():
            widget.destroy()
        
        editor_label = ttk.Label(
            self.editor_frame, 
            text=f"Editando: {self.current_course.title}", 
            font=('Arial', 14)
        )
        editor_label.pack(pady=10)
        
        # Abas para Aulas/Exercícios
        notebook = ttk.Notebook(self.editor_frame)
        notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Aba de Aulas
        aulas_tab = ttk.Frame(notebook)
        self._build_aulas_editor(aulas_tab, self.current_course)
        
        # Aba de Exercícios
        exercises_tab = ttk.Frame(notebook)
        self._build_exercises_editor(exercises_tab, self.current_course)
        
        notebook.add(aulas_tab, text="Aulas")
        notebook.add(exercises_tab, text="Exercícios")

    def _build_aulas_editor(self, parent, course):
        ttk.Button(
            parent, 
            text="+ Nova Aula", 
            command=lambda: self._add_aula(course)
        ).pack(pady=5)
        
        if not course.aulas:
            ttk.Label(parent, text="Nenhuma aula cadastrada").pack(pady=10)
            return
            
        for aula in course.aulas:
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=aula.title, width=30).pack(side=tk.LEFT, padx=5)
            ttk.Button(
                frame, 
                text="Editar", 
                command=lambda l=aula: self._edit_aula(l)
            ).pack(side=tk.LEFT, padx=2)
            ttk.Button(
                frame, 
                text="Excluir", 
                command=lambda l=aula: self._delete_aula(course, l)
            ).pack(side=tk.LEFT, padx=2)

    def _add_aula(self, course):
        title = simpledialog.askstring("Nova Aula", "Título da Aula:")
        content = simpledialog.askstring("Conteúdo", "Conteúdo da Aula:")
        if title and content:
            aula_id = max(l.aula_id for l in course.aulas) + 1 if course.aulas else 1
            course.aulas.append(Aula(aula_id, title, content))
            self.persistence.save_courses(self.courses)
            self._load_course_editor(None)
            messagebox.showinfo("Sucesso", "Aula adicionada com sucesso!")

    def _edit_aula(self, aula):
        new_content = simpledialog.askstring("Editar Aula", "Novo Conteúdo:", initialvalue=aula.content)
        if new_content:
            aula.content = new_content
            self.persistence.save_courses(self.courses)
            self._load_course_editor(None)
            messagebox.showinfo("Sucesso", "Aula atualizada com sucesso!")

    def _delete_aula(self, course, aula):
        if messagebox.askyesno(
            "Confirmar Exclusão", 
            f"Tem certeza que deseja excluir a aula '{aula.title}'?"
        ):
            course.aulas.remove(aula)
            self.persistence.save_courses(self.courses)
            self._load_course_editor(None)
            messagebox.showinfo("Sucesso", "Aula excluída com sucesso!")

    def _build_exercises_editor(self, parent, course):
        ttk.Button(
            parent, 
            text="+ Novo Exercício", 
            command=lambda: self._add_exercise(course)
        ).pack(pady=5)
        
        if not course.exercises:
            ttk.Label(parent, text="Nenhum exercício cadastrado").pack(pady=10)
            return
            
        for exercise in course.exercises:
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=exercise.title, width=30).pack(side=tk.LEFT, padx=5)
            ttk.Button(
                frame, 
                text="Editar", 
                command=lambda e=exercise: self._edit_exercise(e)
            ).pack(side=tk.LEFT, padx=2)
            ttk.Button(
                frame, 
                text="Corrigir", 
                command=lambda e=exercise: self._correct_exercise(e)
            ).pack(side=tk.LEFT, padx=2)
            ttk.Button(
                frame, 
                text="Excluir", 
                command=lambda e=exercise: self._delete_exercise(course, e)
            ).pack(side=tk.LEFT, padx=2)
    
    def _correct_exercise(self, exercise):
        top = tk.Toplevel(self)
        top.title(f"Corrigir: {exercise.title}")
        top.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(top)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        users = self.persistence.load_users()
        alunos = {a.user_id: a.name for a in users if isinstance(a, Aluno)}
        
        # Lista de respostas
        ttk.Label(
            main_frame, 
            text="Respostas dos Alunos",
            font=('Arial', 12, 'bold')
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Container com scroll
        container = ttk.Frame(main_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for aluno_id, answer in exercise.submissions.items():
            aluno_name = alunos.get(aluno_id, f"Aluno {aluno_id}")
            correction = exercise.corrections.get(aluno_id, {"grade": "", "feedback": ""})
            
            frame = ttk.LabelFrame(scrollable_frame, text=aluno_name)
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Resposta do aluno
            ttk.Label(frame, text="Resposta:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
            answer_text = tk.Text(frame, height=4, width=80)
            answer_text.insert(tk.END, answer)
            answer_text.config(state=tk.DISABLED)
            answer_text.pack(fill=tk.X, padx=5, pady=5)
            
            # Nota
            grade_frame = ttk.Frame(frame)
            grade_frame.pack(fill=tk.X, padx=5, pady=5)
            ttk.Label(grade_frame, text="Nota:").pack(side=tk.LEFT)
            grade_var = tk.StringVar(value=correction["grade"])
            grade_entry = ttk.Entry(grade_frame, textvariable=grade_var, width=10)
            grade_entry.pack(side=tk.LEFT, padx=5)
            
            # Feedback
            feedback_frame = ttk.Frame(frame)
            feedback_frame.pack(fill=tk.X, padx=5, pady=5)
            ttk.Label(feedback_frame, text="Feedback:").pack(anchor=tk.W)
            feedback_entry = tk.Text(feedback_frame, height=4, width=80)
            feedback_entry.insert(tk.END, correction["feedback"])
            feedback_entry.pack(fill=tk.X, padx=5, pady=5)
            
            # Botão para salvar correção
            def save_correction(aluno_id=aluno_id, grade_var=grade_var, feedback_entry=feedback_entry):
                exercise.corrections[aluno_id] = {
                    "grade": grade_var.get(),
                    "feedback": feedback_entry.get("1.0", tk.END).strip()
                }
                self.persistence.save_courses(self.persistence.load_courses())  # Forçar recarregar e salvar
                messagebox.showinfo("Sucesso", "Correção salva!")
            
            ttk.Button(
                frame,
                text="Salvar Correção",
                command=save_correction
            ).pack(pady=10)
    
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _add_exercise(self, course):
        title = simpledialog.askstring("Novo Exercício", "Título:")
        question = simpledialog.askstring("Pergunta", "Enunciado:")
        if title and question:
            exercise_id = max(e.exercise_id for e in course.exercises) + 1 if course.exercises else 1
            course.exercises.append(Exercise(exercise_id, title, question))
            self.persistence.save_courses(self.courses)
            self._load_course_editor(None)
            messagebox.showinfo("Sucesso", "Exercício adicionado com sucesso!")

    def _edit_exercise(self, exercise):
        new_question = simpledialog.askstring("Editar Exercício", "Novo Enunciado:", initialvalue=exercise.question)
        if new_question:
            exercise.question = new_question
            self.persistence.save_courses(self.courses)
            self._load_course_editor(None)
            messagebox.showinfo("Sucesso", "Exercício atualizado com sucesso!")

    def _delete_exercise(self, course, exercise):
        if messagebox.askyesno(
            "Confirmar Exclusão", 
            f"Tem certeza que deseja excluir o exercício '{exercise.title}'?"
        ):
            course.exercises.remove(exercise)
            self.persistence.save_courses(self.courses)
            self._load_course_editor(None)
            messagebox.showinfo("Sucesso", "Exercício excluído com sucesso!")