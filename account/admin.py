# Permite colocar models no Django Admin
from django.contrib import admin
# Permite criar uma classe que vai alterar como o modelo se comporta no Django Admin, como Incersão de filtros, colunas,
# , barras de pesquisas, como os campos podem ser alterados e outros
from django.contrib.auth.admin import UserAdmin
# Custom User Model criado
from .models import Account


class AccountAdmin(UserAdmin):
    # Colunas que serão exibidas no painel admin, não somente o campo que é retornado do método __str__
    list_display = ('full_name', 'email', 'is_staff', 'is_admin', 'last_login', 'date_joined')
    # Cria-se um uma barra de pesquisa que irá buscar os valores inseridos nas colunas abaixo
    search_fields = ('full_name', 'email', 'cpf')

    # Campos que não podem ser alterados, somente vizualizados
    readonly_fields = ('cpf', 'date_joined', 'last_login')

    # Vai ordenar pelo nome completo dos usuários
    ordering = ('full_name',) # caso queira na ordem decrescente basta usar o sinal "-" antes do campode ordering, neste caso ficaria: "-full_name"

    # Filtragem explícita na lateral direita
    list_filter = ('last_login',)

    # Filtragem entre Modelos muitos pra muitos
    filter_horizontal = ()

    #  Fieldsets permite organizar o que é exibido ao abrir um objeto no painel admin
    fieldsets = (
        ('Personal Data',{'fields':('full_name','cpf','email','password')}),
        ('Permisions',{'fields':('is_active','is_admin','is_staff','is_superuser',)}),
    )


admin.site.register(Account, AccountAdmin)
