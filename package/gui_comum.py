import tkinter as tk
from tkinter import ttk, messagebox
from .user import Aluno, Professor

class SignupWindow(tk.Toplevel):
    def __init__(self, parent, user_type, persistence):
        super().__init__(parent)
        self.persistence = persistence
        self.user_type = user_type
        self.title(f"Cadastro de {user_type}")
        self.geometry("400x300")
        
        ttk.Label(self, text="Nome completo:").pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack()
        
        ttk.Label(self, text="Email:").pack(pady=5)
        self.email_entry = ttk.Entry(self)
        self.email_entry.pack()
        
        ttk.Label(self, text="Senha:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()
        
        ttk.Button(self, text="Cadastrar", command=self.register).pack(pady=15)
        
    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not all([name, email, password]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
            
        if self.persistence.email_exists(email):
            messagebox.showerror("Erro", "Email já cadastrado!")
            return
            
        if len(password) < 3:
            messagebox.showerror("Erro", "Senha deve ter pelo menos 3 caracteres!")
            return
            
        new_user = {
            'user_id': self.persistence.get_next_user_id(),
            'name': name,
            'email': email,
            'password': password
        }
        
        users = self.persistence.load_users()
        if self.user_type == 'Aluno':
            users.append(Aluno(**new_user))
        else:
            users.append(Professor(**new_user))
            
        self.persistence.save_users(users)
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        self.destroy()