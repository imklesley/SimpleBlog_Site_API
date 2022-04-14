from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate

from account.models import Account


class RegistrationUserForm(UserCreationForm):
    # email = forms.EmailField(max_length=150, help_text='Add a valid email', )

    class Meta:
        model = Account
        fields = ('full_name', 'cpf', 'email', 'username', 'password1', 'password2')


# Cria um formulário baseado em um modelo
class AuthenticationUserForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')  # Quais campos desse modelo serão usados na criação do formulário

    def clean(self):
        # Caso o formulário sejá válido, ou seja o usuário inseriu email e senha corretamente -- Caso não faça essa
        # verificação irá dar erro, pois authenticate precisa dos campos já validados
        if self.is_valid():
            # Coleta-se os dados de email e senha
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            # Tenta-se autenticar, caso não retorne um objeto User, caso retorne None levanta um error
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid email or password! Try Again')


class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('full_name', 'email', 'username',)

    # Existe o método clean que opera em todos os campos, e podemos operar em cima de apenas um campo, basta usar
    # clean_nomefield
    def clean_email(self):
        # Formulário foi inserido corretamente
        #  Pega-se o valor de email
        email = self.cleaned_data['email']
        if self.instance.email == email:
            return email
        else:
            #  Verifica se é possível pegar uma conta pelo email passado, caso consiga significa que o usuário já existe
            try:
                Account.objects.get(email=email)
                raise forms.ValidationError('Email already used by another user')
            # Caso não exista retorna-se o email
            except Account.DoesNotExist:
                return email

    def clean_username(self):
        #  Pega-se o valor de username
        username = self.cleaned_data['username']

        if self.instance.username == username:
            return username

        else:
            #  Verifica se é possível pegar uma conta pelo email passado, caso consiga significa que o usuário já existe
            try:
                Account.objects.get(username=username)
                raise forms.ValidationError('Username already used by another user')
            # Caso não exista retorna-se o email
            except Account.DoesNotExist:
                return username
