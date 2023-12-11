# from users import Candidato

class Vaga:
    def __init__(self, nome, area, descricao, quantidade:int, nome_empresa, salario, requisitos):
        self.__nome = nome
        self.__area = area
        self.__descricao = descricao
        self.__quantidade = quantidade
        self.__nome_empresa = nome_empresa
        self.__salario = salario
        self.__requisitos = requisitos
        self.__lista_candidaturas = []  # lista do professor vulgo Alex
    
    @property
    def nome(self):
        return self.__nome
    
    def adicionarCandidatura(self,candidato):
        self.__lista_candidaturas.append(candidato.nome)

    def mostrarCandidaturas(self):
        return self.__lista_candidaturas

    def dict_user(self):
        return {
            "nome": self.__nome,
            "area": self.__area,
            "descricao": self.__descricao,
            "quantidade": self.__quantidade,
            "nome_empresa": self.__nome_empresa,
            "salario": self.__salario,
            "requisitos": self.__requisitos,
            "lista_candidaturas": self.__lista_candidaturas
        }

        return user_dict
    
    def __str__(self) -> str:
        return f"""
------------------------------------
    Nome: {self.__nome}
    Area: {self.__area}
    Empresa: {self.__nome_empresa} 
    Requisitos: {self.__requisitos}

    Salario: {self.__salario}
    Quantidade de Vagas: {self.__quantidade}
    Descrição: {self.__descricao}
------------------------------------
"""
    
# if __name__ == '__main__':
#     v = Vaga('tsi','ti','adf','fsr','hsdfiuwshgf','fhwiufhw', 'hhdsgf')
#     c = Candidato('luiz','lf','1234')
#     d = Candidato('lucas','lf','1234')
#     e = Candidato('marcelo','lf','1234')
#     f = Candidato('bruno','lf','1234')
#     v.adicionarCandidatura(c)
#     v.adicionarCandidatura(d)
#     v.adicionarCandidatura(e)
#     v.adicionarCandidatura(f)
#     print(v.mostrarCandidaturas())
