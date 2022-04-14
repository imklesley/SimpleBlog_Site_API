import os
from datetime import datetime
from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify

# Permite acessar outras variáveis instanciadas no arquivo settings.py, neste caso está sendo utilizado para ter acesso
# à classe de User definida em AUTH_USER_MODEL, outra forma de fazer isso seria usando a própria CustomUser criada
# anteriormente
from django.conf import settings


# Função que retorna aonde a imagem que será uppada ficará localizada e qual nome essa imagem terá
def upload_location(instance, filename):
    timestamp = datetime.now().timestamp()
    file_path = f'posts/{instance.author.id}/{instance.title}-{timestamp}-{filename}'
    return file_path




class BlogPost(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published = models.DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name='Date Published')
    date_updated = models.DateTimeField(auto_now=True, blank=False, null=False, verbose_name='Date Updated')
    slug = models.SlugField(blank=True, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Post's"





@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(save=False)


# Uma outra forma de realizar a criação de um receiver, ou seja "alguém" receberá um sinal antes, no momento,
# ou após algo acontecer e a seguinte:

def pre_save_blog_post_receiver(sender, instance: BlogPost, **kwargs):
    timestamp = datetime.now().timestamp()
    if not instance.slug:
        # slugfy retira tudo que n pode haver em uma url, espaços viram hinfem e acentuações viram caracteres especiais
        instance.slug = slugify(f'{instance.author.username}-{timestamp}-{instance.title}')


# Isso vai fazer a conexão entre o receiver e a classe BlogPost que está enviando os signals antes de salvar no db
pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)


# Da linha 46 à 54 é a mesma coisa que:

# @receiver(pre_save, sender=BlogPost)
# def pre_save_blog_post_receiver(sender, instance: BlogPost, **kwargs):
#     timestamp = datetime.now().timestamp()
#     if not instance.slug:
#         # slugfy retira tudo que n pode haver em uma url, espaços viram hinfem e acentuações viram caracteres especiais
#         instance.slug = slugify(f'{instance.author.username}-{timestamp}-{instance.title}')

# A diferença é que o primeiro método usa decorators e o segundo não


# @receiver(models.signals.pre_save, sender=BlogPost)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#
#     if not instance.pk:
#         return False
#
#     try:
#         old_image = BlogPost.objects.get(pk=instance.pk).image
#     except BlogPost.DoesNotExist:
#         return False
#
#     new_image = instance.image
#     if old_image != new_image:
#         if os.path.isfile(old_image.path):
#             os.remove(old_image.path)
