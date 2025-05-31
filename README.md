
# Plataforma de Cursos em Python

## Descrição do Projeto

Esta aplicação desktop desenvolvida em Python oferece uma plataforma completa para gerenciamento de cursos educacionais, atendendo a dois perfis de usuário:

- Alunos: Visualizam cursos, acessam aulas, respondem exercícios e veem correções

- Professores: Criam e gerenciam cursos, aulas e exercícios, e corrigem respostas dos alunos

O sistema resolve o problema de organização e gestão de conteúdo educacional em ambiente desktop, proporcionando uma experiência intuitiva para ambos os perfis.

---

## Casos de Uso

###  Cadastro de Usuário

Acesse a tela de login

Clique em "Cadastrar"

Preencha nome, email e senha

Selecione perfil (Aluno ou Professor)

Sistema valida e cria nova conta

---

###  Login

Insira email e senha

Sistema verifica credenciais

Redireciona para interface correspondente

---

###  Aluno Visualiza Curso

Faça login como aluno

Selecione curso na lista

Sistema exibe conteúdo organizado em aulas e exercícios

---

###  Aluno Responde Exercício

Selecione exercício

Digite resposta na área de texto

Clique em "Enviar Resposta"

Sistema armazena a resposta

---

###  Professor Cria Curso

Faça login como professor

Clique em "Novo Curso"

Insira título do curso

Sistema cria curso e adiciona à lista

---

###  Professor Adiciona Aula

Selecione curso

Clique em "+ Nova Aula"

Insira título e conteúdo

Sistema adiciona aula ao curso

---

###  Professor Corrige Exercício

Selecione exercício

Clique em "Corrigir"

Para cada aluno:

Visualize resposta

Atribua nota

Escreva feedback

Clique em "Salvar Correção"

---

##  Funcionalidades

### 👨‍🎓 Para Alunos

| Funcionalidade             | Descrição                                      |
|---------------------------|------------------------------------------------|
| **Listagem de cursos**    | Visualização de todos os cursos disponíveis   |
| **Conteúdo de aulas**     | Acesso ao material textual das aulas          |
| **Resposta a exercícios** | Envio de respostas para exercícios propostos  |
| **Status de exercícios**  | Indicação visual (Enviado/Corrigido)          |

### 👨‍🏫 Para Professores

| Funcionalidade              | Descrição                                        |
|----------------------------|--------------------------------------------------|
| **Gestão de cursos**        | Criação, edição e exclusão de cursos            |
| **Gestão de aulas**         | Adição, edição e remoção de aulas               |
| **Gestão de exercícios**    | Criação, edição e exclusão de exercícios        |
| **Correção de respostas**   | Atribuição de notas e feedbacks                 |
| **Visualização de submissões** | Acesso a todas as respostas dos alunos     |

---

## Diagram de Classes

![Diagrama_de_classes](https://github.com/user-attachments/assets/12c11ae3-3f27-41c7-84ea-6cfa103f1ab1)

---

### Tecnologias Utilizadas

- Python 3.x: Linguagem principal

- Tkinter: Framework para interface gráfica

- JSON: Sistema de persistência de dados

---

## COMO EXECUTAR

### PRÉ-REQUISITOS:

- Python 3.x instalado

### INSTRUÇÕES:

1. Clone o repositório:
   
   git clone https://github.com/brunnf/Plataforma_cursos_OO
   cd Plataforma_cursos_OO

3. Execute a aplicação:
   
- Para aluno:
  
     python main_aluno.py

- Para professor:
  
     python main_professor.py

## DADOS INICIAIS:

- Os arquivos de dados são criados automaticamente na pasta data/
- Crie pelo menos um usuário professor e um aluno via interface
  
### Para o caso de apenas vizualização do funcionamneto da plataforma, pode-se usar os seguintes logins:

#### Para o aluno:

- Email: admin_aluno
- Senha: admin

#### Para o professor:

- Email: admin_professor
- Senha: admin

## ESTRUTURA DE DIRETÓRIOS

projeto-curso/

├── data/

│  ├── usuarios.json

│  └── cursos.json

├── package/

│  ├── __init__.py

│  ├── user.py

│  ├── course.py

│  ├── persistence.py

│  ├── gui_aluno.py

│  ├── gui_professor.py

│  └── gui_comum.py

├── main_aluno.py

├── main_professor.py

└── README.md

##  Autor

Bruno Ferreira Dornelas

Projeto acadêmico para a disciplina de Orientação a Objetos – UnB Gama – 2025/1
