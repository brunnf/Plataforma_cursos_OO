import tkinter as tk
from tkinter import ttk, messagebox
from .course import Aula, Exercise

class AlunoGUI(tk.Tk):
    def __init__(self, Aluno, persistence):
        super().__init__()
        self.aluno = Aluno
        self.persistence = persistence
        self.courses = persistence.load_courses()
        self.current_course = None
        self._setup_ui()

    def _setup_ui(self):
        self.title(f"Aluno: {self.aluno.name}")
        self.geometry("1000x600")
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista de Cursos
        course_frame = ttk.LabelFrame(main_frame, text="Cursos Disponíveis")
        course_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        self.course_listbox = tk.Listbox(course_frame, width=30, height=20)
        self.course_listbox.pack(fill=tk.Y, padx=5, pady=5)
        
        # Carregar cursos
        for course in self.courses:
            self.course_listbox.insert(tk.END, course.title)
        
        # Frame de Conteúdo
        self.content_frame = ttk.LabelFrame(main_frame, text="Conteúdo do Curso")
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Mensagem inicial
        self.status_label = ttk.Label(
            self.content_frame, 
            text="Selecione um curso para ver o conteúdo",
            font=('Arial', 12)
        )
        self.status_label.pack(expand=True)
        
        self.course_listbox.bind('<<ListboxSelect>>', self._load_course_content)

    def _load_course_content(self, event):
        selection = self.course_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.current_course = self.courses[index]
        
        # Limpar frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Criar abas para aulas e exercícios
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Aba de Aulas
        aulas_tab = ttk.Frame(notebook)
        self._build_aulas_tab(aulas_tab)
        
        # Aba de Exercícios
        exercises_tab = ttk.Frame(notebook)
        self._build_exercises_tab(exercises_tab)
        
        notebook.add(aulas_tab, text="Aulas")
        notebook.add(exercises_tab, text="Exercícios")

    def _build_aulas_tab(self, parent):
        if not self.current_course.aulas:
            ttk.Label(parent, text="Nenhuma aula disponível").pack(pady=20)
            return
            
        # Frame com scrollbar
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container)  # Definir canvas aqui
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Botões para cada aula
        for aula in self.current_course.aulas:
            btn = ttk.Button(
                scrollable_frame,
                text=aula.title,
                command=lambda l=aula: self._show_aula(l),
                width=40
            )
            btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Empacotar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_exercises_tab(self, parent):
        if not self.current_course.exercises:
            ttk.Label(parent, text="Nenhum exercício disponível").pack(pady=20)
            return
            
        # Frame com scrollbar
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container)  # Definir canvas aqui
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Botões para cada exercício
        for exercise in self.current_course.exercises:
            # Verificar se já foi respondido
            status = " (Respondido)" if self.aluno.user_id in exercise.submissions else ""
            if self.aluno.user_id in exercise.corrections:
                status = " (Corrigido)"
            
            btn = ttk.Button(
                scrollable_frame,
                text=exercise.title + status,
                command=lambda e=exercise: self._show_exercise(e),
                width=40
            )
            btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Empacotar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _show_aula(self, aula):
        top = tk.Toplevel(self)
        top.title(aula.title)
        top.geometry("800x600")
        
        # Frame com scrollbar
        container = ttk.Frame(top)
        container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(container)  # Definir canvas aqui
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        content_frame = ttk.Frame(canvas)
        
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Exibir conteúdo
        tk.Label(
            content_frame, 
            text=aula.content, 
            wraplength=700, 
            justify=tk.LEFT,
            font=('Arial', 12)
        ).pack(padx=20, pady=20)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _show_exercise(self, exercise):
        
        self.exercise_window = tk.Toplevel(self)
        self.exercise_window.title(exercise.title)
        self.exercise_window.geometry("700x600")
        
        # Criar abas
        notebook = ttk.Notebook(self.exercise_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Aba de Resposta
        answer_tab = ttk.Frame(notebook)
        self._build_answer_tab(answer_tab, exercise)
        
        # Aba de Correção (se existir)
        if self.aluno.user_id in exercise.corrections:
            correction_tab = ttk.Frame(notebook)
            self._build_correction_tab(correction_tab, exercise)
            notebook.add(correction_tab, text="Correção")
        
        notebook.add(answer_tab, text="Exercício")

    def _build_answer_tab(self, parent, exercise):
        # Frame principal
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Enunciado
        ttk.Label(
            main_frame, 
            text="Enunciado:",
            font=('Arial', 10, 'bold')
        ).pack(anchor=tk.W)
        
        question_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, borderwidth=1)
        question_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            question_frame, 
            text=exercise.question, 
            wraplength=650, 
            justify=tk.LEFT,
            font=('Arial', 11)
        ).pack(padx=10, pady=10)
        
        # Resposta
        ttk.Label(
            main_frame, 
            text="Sua Resposta:",
            font=('Arial', 10, 'bold')
        ).pack(anchor=tk.W, pady=(10, 0))
        
        answer_entry = tk.Text(main_frame, height=10, font=('Arial', 11))
        answer_entry.pack(fill=tk.X, pady=5)
        
        # Preencher resposta existente
        if self.aluno.user_id in exercise.submissions:
            answer_entry.insert(tk.END, exercise.submissions[self.aluno.user_id])
        
        # Botão de envio
        def submit():
            answer = answer_entry.get("1.0", tk.END).strip()
            exercise.submissions[self.aluno.user_id] = answer
            self.persistence.save_courses(self.courses)
            messagebox.showinfo("Sucesso", "Resposta enviada com sucesso!")
            self.exercise_window.destroy()  # Fechar a janela usando o atributo
            self._load_course_content(None)  # Atualizar a lista de exercícios
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Enviar Resposta", 
            command=submit
        ).pack(side=tk.RIGHT)

    def _build_correction_tab(self, parent, exercise):
        correction = exercise.corrections[self.aluno.user_id]
        
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Nota
        grade_frame = ttk.Frame(main_frame)
        grade_frame.pack(fill=tk.X, pady=10)
        ttk.Label(grade_frame, text="Nota:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        ttk.Label(grade_frame, text=correction["grade"], font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        
        # Feedback
        feedback_frame = ttk.LabelFrame(main_frame, text="Feedback do Professor")
        feedback_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        feedback_text = tk.Text(feedback_frame, wrap=tk.WORD, font=('Arial', 11))
        feedback_text.insert(tk.END, correction["feedback"])
        feedback_text.config(state=tk.DISABLED)
        feedback_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)