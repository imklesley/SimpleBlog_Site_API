from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from account.forms import RegistrationUserForm, AuthenticationUserForm, UpdateAccountForm


def registration_view(request):
    context = {}

    # Se o usuário já estiver logado, n permite que ele acesse a página o redirecionando para a home
    if request.user.is_authenticated:
        return redirect('home')

    # Se a requisição for do tipo POST
    if request.POST:
        # Passamos os dados inseridos pelo usuário pra dentro do RegistrationUserForm e "criamos" um form com dados
        form = RegistrationUserForm(request.POST)
        # Verifica-se se o usuário inseriu tudo corretamente
        if form.is_valid():
            # Se tudo okay, para criar o usuário basta dar um form.save() isso equivale a Account.objects.create_user
            form.save()

            # Agora pode-se, por exemplo, realizar o login
            # Coleta-se email e senha
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Valida o email e senha passsados, caso os dados sejam válidos retorna um objeto User
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                # Após login, redireciona para home
                return redirect('home')
            else:
                return redirect('home')
        else:
            context['form'] = form
    else:
        form = RegistrationUserForm()
        context['form'] = form

    return render(request, 'account/registration.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    # Se o usuário já estiver logado, n permite que ele acesse a página o redirecionando para a home
    if request.user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AuthenticationUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')

        else:
            context['form'] = form
    else:
        form = AuthenticationUserForm()
        context['form'] = form

    return render(request, 'account/login.html', context)


def account_view(request):
    user = request.user

    # Caso o usuário não esteja logado, redireciona para a página de login
    if not user.is_authenticated:
        return redirect('login')

    context = {}

    if request.POST:
        # É necessário passar o parâmetro instance pro django entender que se trata de uma atualização, caso contrário
        # vai ser criado outro usuário
        form = UpdateAccountForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            context['success_message'] = 'Your Account Was Updated!'
            return render(request, 'account/account.html', context)
        else:
            context['form'] = form
    else:
        form = UpdateAccountForm(initial={'full_name': user.full_name, 'email': user.email, 'username': user.username,
                                          'cpf': user.cpf})
        context['form'] = form

    return render(request, 'account/account.html', context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})
