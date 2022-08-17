from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def cadastro(request):
    """ Cadastra uma nova pessoas no sistema """

    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'O nome não pode ficar em branco')
            return redirect('cadastro')
        if campo_vazio(email):  
            messages.error(request, 'O email não pode ficar em branco')
            return redirect('cadastro')
        if senhas_nao_batem(senha, senha2):
            messages.error(request, 'As senhas não batem')
            return redirect('cadastro') 
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso')
        return redirect('login')        
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    """ Realiza o login de uma pessoas no sistema """

    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos email e senha não podem ficar em branco')
            return redirect('login')
        print(email, senha)
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso')
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')

def logout(request):
    """ Faz o usuário se desconectar da aplicação """

    auth.logout(request)
    return redirect('index')

def dashboard(request):
    """ Leva o usuário a dashboard após efetuar o login """

    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-date_receita').filter(pessoas=id)
        dados = {
            'receitas' : receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')

def campo_vazio(campo):
    """ Reação para quando o usuário deixa campos vazios no formulário """

    return not campo.strip()

def senhas_nao_batem(senha, senha2):
    """ Reação de quando as senhas digitadas não são iguais """

    return senha != senha2
