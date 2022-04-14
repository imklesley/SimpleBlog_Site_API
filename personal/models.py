from django.db import models

# Exemplo de model com choices
# PRIORITY = [
#     ('L', 'Low'),
#     ('M', 'Medium'),
#     ('H', 'High')
# ]
#
#
# class Task(models.Model):
#     title = models.CharField(max_length=100, null=False)
#     description = models.TextField(max_length=500, null=False)  # TextField não precisa de max_length
#     priority = models.CharField(max_length=1, choices=PRIORITY)
#
#     def __str__(self):
#         return self.title
#
#     # As alterações aqui são para a tabela
#     class Meta:
#         verbose_name = 'Tarefinha'
#         verbose_name_plural = 'Tarefinhas'
