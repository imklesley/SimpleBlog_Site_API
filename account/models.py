# Rest-Framework imports
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.db import models

# São usados para criar um novo modelo User, que possibilita a criação de usuários e super-usuários
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Caso meu Custom User Model possuir somente os campos que o modelo User padrão, poderia-se Usar o UserManager ao invés
# do BaseUserManager, mas como estamos fazendo esse modelo pra servir em qualquer aplicação vamos criar nosso próprio
# UserManager

# Essa classe irá fazer o controle de criação de contas e setar autorizações
class AccountManager(BaseUserManager):

    # Cria-se um usuário comum
    # Os parâmetros usados aqui são os campos requeridos na criação do usuário que estão descritos na classe Account
    def create_user(self, email, username, full_name, cpf, password=None):
        if not email:
            raise ValueError('Users must have an email adress')
        if not username:
            raise ValueError('Users must have an username')
        if not full_name:
            raise ValueError('Users must have full name')
        if not cpf:
            raise ValueError('Users must have an cpf')

        # Se todos os campos foram verificados e n possui erros, podemos criar o usuário

        user = self.model(
            # normalize_email faz com que todos os caracteres de email sejam convertidos para lower case, essa função só
            # está disponível dentro de BaseUserManager
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            cpf=cpf
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # Cria-se um usuário comum e então seta as caracteristicas de staff
    def create_staffuser(self, email, username, full_name, cpf, password=None):
        # Cria-se um usuário comum
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            cpf=cpf,
            password=password
        )

        # Agora aplica-se as caracteríticas de super usuário
        user.is_admin = False
        user.is_staff = True
        user.is_superuser = False

        user.save(using=self._db)

        return user

    # Cria-se um usuário comum e então seta as caracteristicas de super
    def create_superuser(self, email, username, full_name, cpf, password=None):
        # Cria-se um usuário comum
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            cpf=cpf,
            password=password
        )

        # Agora aplica-se as caracteríticas de super usuário
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class Account(AbstractBaseUser):
    # coloca-se todos os campos desejados aqui, como email, cpf, endereço, etc.
    email = models.EmailField(verbose_name='Email Adress', max_length=150, unique=True, null=False, blank=False, )
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=150, null=False, blank=False)
    cpf = models.CharField(max_length=11, null=False, blank=False)

    # NÃO SE CRIA O CAMPO PASSWORD, POIS O PRÓPRIO DJANGO QUE CUIDA DISSO

    # Os campos abaixo são obrigatórios na criação de um modelo de usuário personalizado
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Fala pro django qual campo vai ser usado pra fazer o login, o nome não é intuitivo, mas é o que temos kkk
    USERNAME_FIELD = 'email'

    # Fala pro django quais campos são obrigatórios, além do campo inserido em "USERNAME_FIELD" que é automaticamente obrigatório
    REQUIRED_FIELDS = ['username', 'full_name', 'cpf']

    def __str__(self):
        return self.username

    # Funções que é preciso criar, basta copiar e colar pois isso n vai fazer diferença no final

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def get_first_name(self):
        return self.full_name.split()[0]

    # É necessário falar pro django qual é o User Manager dessa classe account, para isso passamos a classe
    # AccountManages paa dentro da variável objects

    objects = AccountManager()


# Ao final da criação do Custom User Model, você DEVE lembrar de ir ao arquivo settings.py e falar pro django qual vai
# ser o modelo de criação de usuários, pois não queremos mais a classe default, para isso basta colocar o nome
# do app criado e o nome da classe dentro da variável AUTH_USER_MODEL. Neste caso ficaria: AUTH_USER_MODEL = 'account.Account'


# Vai receber um sinal do tipo pós o modelo que enviou, neste caso é Account(outra forma seria usar o arquivo settings
# e acessar AUTH_USER_MODEL), e vai executar a função create_auth_token
@receiver(post_save, sender=Account)
def create_auth_toke(sender, instance=None, created=False, **kwargs):
    # Verifica se o usuário foi criado, caso tenha sido cria um token vinculado a conta do usuário criado
    if created:
        Token.objects.create(user=instance)
