
from app import app, db, Obra

dados_livros = {
    3: {
        "autor": "Vitor Henrique Paro",
        "editora": "Cortez"
    },
    6: {
        "autor": "Eliane dos Santos Cavalleiro",
        "editora": "Contexto",
        "ano_publicacao": 2000,
        "isbn": "9788572441476"
    },
    9: {
        "autor": "bell hooks",
        "editora": "WMF Martins Fontes",
        "ano_publicacao": 2017,
        "numero_paginas": 283,
        "edicao": "2ª",
        "isbn": "9788546901401"
    },
    14: {
        "autor": "Grada Kilomba",
        "editora": "Cobogó",
        "ano_publicacao": 2019,
        "numero_paginas": 248,
        "edicao": "1ª",
        "isbn": "9788555910807"
    },
    15: {
        "autor": "Nilma Lino Gomes",
        "editora": "Vozes",
        "ano_publicacao": 2017,
        "numero_paginas": 160,
        "edicao": "1ª",
        "isbn": "9788532655790"
    },
    16: {
        "autor": "Kabengele Munanga e Nilma Lino Gomes",
        "editora": "Global",
        "ano_publicacao": 2006,
        "numero_paginas": 224,
        "isbn": "9788526011342"
    },
    17: {
        "autor": "Paulo Freire",
        "editora": "Paz e Terra",
        "ano_publicacao": 2019,
        "numero_paginas": 144,
        "isbn": "9788577534098"
    },
    18: {
        "autor": "Paulo Freire",
        "editora": "Paz e Terra"
    },
    19: {
        "autor": "Maria Helena Souza Patto",
        "editora": "T. A. Queiroz",
        "ano_publicacao": 1984
    },
    20: {
        "autor": "Nilma Lino Gomes",
        "editora": "Autêntica",
        "ano_publicacao": 2006,
        "numero_paginas": 411,
        "isbn": "9788575262160"
    }
}

with app.app_context():

    campos_preenchidos = 0
    registros_atualizados = 0

    for livro_id, dados in dados_livros.items():

        livro = db.session.get(Obra, livro_id)

        if livro is None:
            print(f"ID {livro_id}: não encontrado.")
            continue

        alteracoes = 0

        for campo, novo_valor in dados.items():

            valor_atual = getattr(livro, campo)

            if valor_atual is None or valor_atual == "":
                setattr(livro, campo, novo_valor)
                alteracoes += 1

            elif valor_atual == "Não informado":
                setattr(livro, campo, novo_valor)
                alteracoes += 1

            elif valor_atual == 0 and isinstance(novo_valor, int):
                setattr(livro, campo, novo_valor)
                alteracoes += 1

        if alteracoes:
            registros_atualizados += 1
            campos_preenchidos += alteracoes

        print(f"ID {livro_id}: {alteracoes} campos preenchidos.")

    try:
        db.session.commit()

        print("\nATUALIZAÇÃO CONCLUÍDA")
        print("Registros atualizados:", registros_atualizados)
        print("Campos preenchidos:", campos_preenchidos)

    except Exception:
        db.session.rollback()
        print("Erro. Alterações revertidas.")
        raise
