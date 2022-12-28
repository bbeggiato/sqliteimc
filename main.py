# Python 3.10.8
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from funcaoimc import calculaImc

import banco

# Pesquisa cadastro no banco academia do SQLite
def pesquisar():
  tv.delete(*tv.get_children())
  vquery = "SELECT * FROM clientes WHERE nome LIkE'%" + vnomepesquisar.get() + "%' order by idcliente"
  linhas = banco.dql(vquery)
  for i in linhas:
    tv.insert("", "end", values=i)

# Mostra os dados do Cadastro
def popular():
  tv.delete(*tv.get_children())  # Deleta todos os registros do Tree View
  vquery = "SELECT * FROM clientes order by nome asc"
  linhas = banco.dql(vquery)
  for i in linhas:
    tv.insert("", "end", values=i)

# Deleta um por um dos dados do Cadastro
def deletar():
  vid = -1
  itemSelecionado = tv.selection()[0]
  valores = tv.item(itemSelecionado, "values")
  vid = valores[0]
  try:
    vquery = f"DELETE FROM clientes WHERE idcliente={vid}"
    resp = messagebox.askyesno("Resetar", "Deseja Apagar esse Usuário do Cadastro? \n Só é possível apagar um de cada vez")
    if resp == True:
      banco.dml(vquery)
      tv.delete(itemSelecionado)
      messagebox.showinfo(title="DELETADO", message="Item Deletado com Sucesso!")
  except:
    messagebox.showinfo(title="ERRO", message="Erro ao Deletar")
    return


###################################################################################################
# Sai do sistema
def sair():
  resposta2 = messagebox.askyesno("Sair", "Deseja Sair?")
  if resposta2 == True:
     main.quit()


# Validação para não permitir string nos campos Peso e Altura
def valida(entrada):
  if entrada.replace('.', '', 1).isdigit():
    return True
  elif entrada == "":
    return True
  else:
    return False


# Executa comando da funcão ao clicar no botão Calcular
def analisaDados():
  # Recebe os valores com o get() e os atribui a variável
  if vnome.get() != "" and vnome.get() != "" and vendereco.get() != "" and valtura.get() != "" and vpeso.get() != "":
    alt = float(valtura.get())
    pes = float(vpeso.get())

    res = calculaImc(alt, pes)
    vimc = res[0]
    vestado = res[1]

    # Atribui a resposta a res
    resultado = f' O IMC  é: {vimc:.2f}\n\n {vestado}'

    # Escreve o conteúdo de res
    lb["text"] = resultado

    return res

  else:
    messagebox.showwarning(title="Aviso", message="Favor Preencher Todos os Campos!")


# Salva os dados no BD
def salvar():
  if lb["text"] != '' and vnome.get() != "" and vnome.get() != "" and vendereco.get() != "" and valtura.get() != "" and vpeso.get() != "":
    nom = vnome.get()
    end = vendereco.get()
    peso = float(vpeso.get())
    pes = f'{peso:.2f}'

    result = analisaDados()
    vimc = result[0]
    imc = f'{vimc:.2f}'
    estado = result[1]
    alturametros = result[2]
    altmetros = f'{alturametros:.2f}'


    print(altmetros)
    dataAtual = datetime.now().strftime('%d/%m/%Y')
    #print (dataAtual)
    querSalvar = messagebox.askyesno("Salvar", "Deseja Salvar os Dados no Cadastro?")
    if querSalvar == True:
      vquery = f"INSERT INTO clientes (data, nome, endereco, peso, altura, imc, status) VALUES('{dataAtual}', '{nom}','{end}','{pes}','{altmetros}','{imc}','{estado}')"
      banco.dml(vquery)
      # varnome.delete(0, END)
      # varendereco.delete(0, END)
      # varpeso.delete(0, END)
      # varaltura.delete(0, END)
      popular()
      print("Dados Gravados")
      messagebox.showinfo(title="Aviso", message="Dados Salvos com Sucesso!")
  else:
    messagebox.showwarning(title="Aviso", message="Não existem dados suficientes para Salvar!")


# Executa comando da funão ao clicar no botão Limpar
def reset():
  resposta = messagebox.askyesno("Resetar", "Deseja Limpar todos os Dados?")
  if resposta == True:
    # Limpa o campo Resultado
    res = ''
    lb["text"] = res

    # Limpa as Entry
    vnome.delete(0, END)
    vendereco.delete(0, END)
    valtura.delete(0, END)
    vpeso.delete(0, END)

# Nome e configs do Container
main = Tk()
main.title("Cálculo do IMC - Índice de Massa Corporal")
main.geometry("900x600")

nb=ttk.Notebook(main)
nb.place(x=0, y=0, width=900, height=600)

tb1=Frame(nb, background="lightblue")
tb2=Frame(nb, background="lightblue")

nb.add(tb1,text="Cálculo IMC")
nb.add(tb2, text="Cadastro")

vnum_cstexto = StringVar()

frame1=Frame(tb1, borderwidth=3, background="#cecece")
frame1.place(x=400, y=257, width=330, height=200)

# Campo Nome
nome = Label(tb1, text="Nome do Paciente: ", font="14", bg='lightblue', anchor=W)
nome.place(x=120, y=80, width=180, height=35)
vnome=Entry(tb1, font=14)
vnome.place(x=280, y=80, width=450, height=35)

# Campo Endereço
endereco = Label(tb1, text="Endereço Completo: ", font=14, bg='lightblue', anchor=W)
endereco.place(x=120, y=170, width=180, height=35)
vendereco=Entry(tb1)
vendereco.place(x=280, y=170, width=450, height=35)

# Campo Altura
altura = Label(tb1, text="Altura(cm)", font=14, bg='lightblue', anchor=W)
altura.place(x=120, y=260, width=100, height=35)
valtura = Entry(tb1, font=14)
valtura.place(x=280, y=260, width=100, height=35)
registro = tb1.register(valida)
valtura.config(validate="key", validatecommand=(registro,'%P'))

# Campo Peso
peso = Label(tb1, text="Peso (Kg)", font=14, bg='lightblue', anchor=W)
peso.place(x=120, y=330, width=100, height=35)
vpeso = Entry(tb1, font=14)
vpeso.place(x=280, y=330, width=100, height=35)
registro = tb1.register(valida)
vpeso.config(validate="key", validatecommand=(registro, '%P'))

# Botão Calcular
btnCalcular = Button(tb1, text="Calcular", command=analisaDados)
btnCalcular.place(x=280, y=490, width=70, height=25)

# Botão Reiniciar
btnReiniciar = Button(tb1,text="Reiniciar", command=reset)
btnReiniciar.place(x=363, y=490, width=70, height=25)

# Salva no banco de dados
btnSalvar = Button(tb1, text="Salvar", command=salvar)
btnSalvar.place(x=581, y=490, width=70, height=25)

# Botão Sair
btnSair = Button(tb1, text="Sair", command=sair)
btnSair.place(x=661, y=490, width=70, height=25)

#Resultado
lb = Label(frame1,text="",fg="#696969", background="#fafdff", font=('arial', 16, 'bold'))
lb.place(x=0, y=0, width=330, height=200)

####################################################################################################################
# Cria Esqueleto do retorno do Banco de dados
quadroGrid = LabelFrame(tb2, text="Cadastro")
quadroGrid.pack(fill='both', expand=TRUE, padx=10, pady=10)

tv = ttk.Treeview(quadroGrid, height=20, columns=('id', 'data', 'nome', 'endereco', 'peso', 'altura', 'imc', 'status'), show='headings')
tv.column('id', minwidth=0, width=30)
tv.column('data', minwidth=0, width=65)
tv.column('nome', minwidth=0, width=207)
tv.column('endereco', minwidth=0, width=303)
tv.column('peso', minwidth=0, width=54)
tv.column('altura', minwidth=0, width=58)
tv.column('imc', minwidth=0, width=35)
tv.column('status', minwidth=0, width=135)
tv.heading('id', text='Id')
tv.heading('data', text='Data')
tv.heading('nome', text='Nome')
tv.heading('endereco', text='Endereço')
tv.heading('peso', text='Peso(Kg)')
tv.heading('altura', text='Altura(M)')
tv.heading('imc', text='IMC')
tv.heading('status', text='Status')
tv.pack()
popular()


quadroPesquisar=LabelFrame(tb2, text="Pesquisar Contatos", bg="lightblue")
quadroPesquisar.pack(fill="both", padx=107, ipady=20, pady=7)

lbid = Label(quadroPesquisar, text="Nome: ")
lbid.pack(side="left", padx=20, ipadx=10, ipady=6)
vnomepesquisar = Entry(quadroPesquisar)
vnomepesquisar.pack(side="left", ipadx=90, ipady=6)
btn_pesquisar = Button(quadroPesquisar, text="  Pesquisar  ", command=pesquisar)
btn_pesquisar.pack(side="left", padx=5, ipady=1)
btn_todos = Button(quadroPesquisar, text="Mostrar Todos", command=popular)
btn_todos.pack(side="left", padx=5, ipady=1)
btn_deletar = Button(quadroPesquisar, text="  Deletar  ", command=deletar)
btn_deletar.pack(side="left", padx=5, ipady=1)
main.mainloop()


