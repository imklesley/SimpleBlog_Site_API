from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from .serializers import RegisterAccountSerializer, LoginAccountSerializer


@api_view(['POST'])
def api_register_account_view(request):
    """
        This endpoint will create an user
    """
    if request.method == 'POST':
        data = {}

        serializer = RegisterAccountSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            data['token'] = Token.objects.get(user=user).key
            data['detail'] = "User registered successfully"
            data['data'] = serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data['detail'] = "User registered failed"
            data['errors'] = serializer.errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def api_login_account_view(request):
    data = {}

    if request.method == 'POST':
        serializer = LoginAccountSerializer(data=request.data)

        # Caso o email ou a senha sejam nulos devolve a response 400
        if serializer.is_valid():
            # Caso os campos estejam okay tenta autenticar
            user = serializer.get_user()

            if user:
                # Para atualizar o token ao logar consegui fazer de duas formas, deletando o token antigo e criando outro
                # old_token = Token.objects.get(user=user)
                # old_token.delete()
                # new_token = Token.objects.create(user=user)

                # Ou filtrando o token com filter e usando o método update para atualizar somente o campo key usando
                # o generate_key só que ao fazer isso o django vai retornar 0 ou 1 de acordo com o resultado da operação update
                Token.objects.filter(user=user).update(key=Token.generate_key())
                # Logo é necessário fazer novamente  a busca pelo token
                token = Token.objects.get(user=user)

                # Passa o token e mensagem de sucesso
                data['token'] = token.key
                data['detail'] = 'User authenticated'

                return Response(data, status.HTTP_200_OK)

        else:
            # Caso os dados sejam inválidos retorna a response com mensagem de erro e a lista de erros de cada field
            data['errors'] = serializer.errors
            data['detail'] = 'Email or password are invalid'
            return Response(data, status.HTTP_400_BAD_REQUEST)
