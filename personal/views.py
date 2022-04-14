from django.shortcuts import render
from operator import attrgetter

# Para a paginação
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage

# Importamos a função criada anteriormente
from post.views import get_post_queryset

POSTS_PER_PAGE = 2  # Pode ser qualquer valor acima de 0, coloquei 1 pois não tenho muitas postagens cadastradas
LIMIT_OF_PAGES = 10


def home_view(request):
    context = {}

    # inicialmente inicializamos a query com texto vazio
    query = ''

    # Caso no request.GET não sejá vazio, no caso seja diferente de <QueryDict: {}>
    # Lembre que qualquer ideia de vazio é considerado falso pelo Django
    if request.GET:
        # Coleta-se a query
        query = request.GET.get('q', '')  # Tenta pegar valor de 'q' caso não tenha retorna ''
        # Envia o valor da query para o template, para se manter a query da busca no search bar
        context['query'] = query

    # Faz a busca dos posts usando a query pra filtrar
    posts = get_post_queryset(query)
    # Ordena as postagens
    posts = sorted(posts, key=attrgetter('date_published'), reverse=True)

    # Pagination
    # Tenta pegar o valor de page do template, caso não encontre retorna o valor 1 que representa a primeira página
    page = request.GET.get('page', 1)
    # Cria-se um paginator, para isso se passa uma lista de objetos e a quantidade de páginas
    posts_paginator = Paginator(posts, POSTS_PER_PAGE)

    # Vai fazer toda a lógica de separação e navegação entre páginas, e já fazendo o tratamento das exceptions
    try:
        # Tenta acessar a página que foi passada pelo template, caso dê erro vai para as exceptions
        posts = posts_paginator.page(page)
    except InvalidPage:
        posts = posts_paginator.page(1)

    # Passa as postagens para o context do template
    context['posts'] = posts
    context['limit_of_pages'] = LIMIT_OF_PAGES
    return render(request, 'personal/home_view.html', context)
