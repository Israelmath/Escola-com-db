from Verificadores import mascara_celular, mascara_cep, busca_endereco, busca_bairro


class Usuario:

    def __init__(self, id, nome, sobrenome, celular, cep):
        self.__id = id
        self.__nome = nome.title()
        self.__sobrenome = sobrenome.title()
        self.__celular = mascara_celular(celular)
        self.__cep = mascara_cep(cep)
        self.__endereco = busca_endereco(cep)
        self.__bairro = busca_bairro(cep)

    @property
    def celular(self):
        return self.__celular

    @property
    def sobrenome(self):
        return self.__sobrenome

    @property
    def cep(self):
        return self.__cep

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @property
    def endereco(self):
        return self.__endereco

    @property
    def bairro(self):
        return self.__bairro

    @id.setter
    def id(self, novo_id):
        self.__id = novo_id

    @celular.setter
    def celular(self, novo_celular):
        self.__celular = novo_celular

    @nome.setter
    def nome(self, novo_nome):
        self.__nome = novo_nome

    @sobrenome.setter
    def sobrenome(self, novo_sobrenome):
        self.__sobrenome = novo_sobrenome

    def __str__(self):
        return '{},{}'.format(self.nome, self.celular)