from package.gui_professor import ProfessorGUI
from package.persistence import PersistenceManager
from package.user import Professor
from package.gui_comum import SignupWindow  
import tkinter as tk
from tkinter import ttk

class LoginWindow(tk.Tk):
    def __init__(self, persistence):
        super().__init__()
        self.persistence = persistence
        self.title("Login Professor")
        self.geometry("300x200")
        
        ttk.Label(self, text="Email:").pack(pady=5)
        self.email_entry = ttk.Entry(self)
        self.email_entry.pack()
        
        ttk.Label(self, text="Senha:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()
        
        ttk.Button(self, text="Entrar", command=self.authenticate).pack(pady=10)
        ttk.Button(self, text="Cadastrar", command=self.open_signup).pack(pady=5)
    
    def open_signup(self):
        SignupWindow(self, 'Professor', self.persistence)


    def authenticate(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        users = self.persistence.load_users()
        for user in users:
            if isinstance(user, Professor) and user.email == email and user.password == password:
                self.destroy()
                ProfessorGUI(user, self.persistence).mainloop()
                return
        
        tk.messagebox.showerror("Erro", "Credenciais inválidas")

if __name__ == "__main__":
    persistence = PersistenceManager()
    LoginWindow(persistence).mainloop()