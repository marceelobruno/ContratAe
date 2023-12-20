def mostrarVagas(vaga):
    print(f"""
    -------------------------

    Nome: {vaga["nome"]}
    ID: {vaga['id_vaga']}
    Area: {vaga["area"]}
    Descricao: {vaga["descricao"]}
    Quantidade de vagas: {vaga['quantidade']}
    Empresa: {vaga['nome_empresa']}
    Salario: {vaga['salario']}
    Requisitos: {vaga['requisito']}

    -------------------------

""")