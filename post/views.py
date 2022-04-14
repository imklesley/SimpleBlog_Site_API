from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from .forms import BlogPostForm
from .models import BlogPost


def create_post_view(request):
    context = {}

    # Caso tenha request do tipo Post cria com os dados caso contrário cria um vazio, e caso possua na request FILES
    # passa os arquivos e caso contrário manda Vazio
    # Caso o formulário seja válido
    form = BlogPostForm(request.POST or None, request.FILES or None)

    #  Só vamos permitir o usuário criar um post se ele estiver autenticado
    user = request.user
    if user.is_authenticated:
        if form.is_valid():
            # Vai criar o formulário, porém não vai salvar no banco de dados. Para isso é usado o parâmetro "commit=False".
            # Pq fazer isso? Pq como podemos observar é necessário colocar o author da postagem na postagem e ainda n temos
            form_obj = form.save(commit=False)
            # Agora basta acessar o campo de author e passar o user do request
            form_obj.author = user
            # Salva-se o formulário no banco
            form_obj.save()
            # E reseta o formulário para uma nova postagem
            form = BlogPostForm()
            context['form'] = form
            context['success_message'] = 'Post Successfully Created. <a href="/">Go to feed</a>'

    else:
        # Caso não esteja autenticado, redireciona para a página de must_authenticate
        return redirect('must_authenticate')

    context['form'] = form
    return render(request, 'post/create_post.html', context)


def user_posts_view(request):
    context = {}

    # Coleta-se o user
    user = request.user

    # Verifica-se se está autenticado
    if user.is_authenticated:
        # Filtra-se os post's do usuário
        posts = BlogPost.objects.filter(author=user)

        # Coloca-se os post's no context
        context['author_posts'] = posts
    else:
        # Caso não esteja redireciona para a página must_authenticate
        return redirect('must_authenticate')

    return render(request, 'post/user_posts.html', context)


def detail_post_view(request, slug):
    context = {}
    post = get_object_or_404(BlogPost, slug=slug)
    context['post'] = post

    return render(request, 'post/detail_post.html', context)


def edit_post_view(request, slug):
    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect('must_authenticate')

    else:
        post = get_object_or_404(BlogPost, slug=slug)

        if post.author == request.user:
            if request.POST:

                form = BlogPostForm(request.POST, request.FILES, instance=post, )

                if form.is_valid():
                    form.save()
                    context['success_message'] = 'Post Successfully Updated!'
                    context['form'] = form
                    return redirect('post:user_posts')

            else:
                form = BlogPostForm(initial={'title': post.title, 'body': post.body, 'image': post.image})
                context['form'] = form
        else:
            raise PermissionDenied

        return render(request, 'post/edit_post.html', context)


def delete_post_view(request, slug):
    blog = BlogPost.objects.get(slug=slug)
    blog.delete()
    return redirect('post:user_posts')


def get_post_queryset(query: str = None) -> list:
    # Lista que irá guardar toda lista de postagens filtradas
    queryset = []

    # Pega a query(o que o usuário inseriu na barra de pesquisa), e "parte" aonde tiver um espaço em branco
    # e forma uma lista de palavras que será utilizado para buscar por postagens. .split faz isso pra gente forma
    # facilitada a query "Curso de Python" iria retornar ["Curso","de", "Python"]

    if query:
        queries = query.split()

        # O método Q é para buscas mais complexas, seria possível buscar somente fazendo um filter com os atributos como
        # ...filter(title__icontains=q.body__icontains=q) só que isso iria fazer uma condicional do tipo and, para retornar
        # um objeto seria necessário o valor está nas duas opções title e body, mas como o intúito é buscar os elementos
        # relacionados pela pesquisa independentemente de onde encontre a query, então usamos o método Q
        # Método contains precisa só retorna se encontrar o valor certinho, já o icontains ignora isso e trás todos os
        # objetos que contenha q pelo menos parte deles. Como não importa que a palavra chave esteja no title E no body
        # utilizamos o Q pra permitir fazer filtros mais complexos
        for q in queries:
            # Para cada query faz-se uma filtragem utilizando o método Q pra conseguir usar conectores de dados como AND, OR
            posts = BlogPost.objects.filter(
                # podemos fazer quantas comparações quisermos com o Q, com diferente tipos de conectores
                Q(title__icontains=q, body__icontains=q, _connector='or')
            ).distinct()  # retorna somente as postagens distintas

            # Faz-se o cast do tipo queryset para lista e faz um cópia dessa lista e a soma com a lista de queryset
            queryset += list(posts).copy()

        # Faz um cast para o tipo set, isso para eliminar os posts repetidos. Transforma-se em lista e retorna-se
        return list(set(queryset))

    return BlogPost.objects.all()
