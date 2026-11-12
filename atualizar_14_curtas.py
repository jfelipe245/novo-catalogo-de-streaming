
import sqlite3
import shutil
from datetime import datetime

BANCO = "instance/afroedu_streaming.db"

obras = {
    162: {
        "antigo": "A Senhora Do Fiar",
        "titulo": "A Velha a Fiar",
        "diretor": "Humberto Mauro",
        "ano": 1964,
        "duracao": "5 minutos e 31 segundos",
        "descricao": "Uma cantiga popular do interior do Brasil é ilustrada por cenas de animais, costumes e aspectos da vida nas antigas fazendas."
    },
    164: {
        "antigo": "Amo Meu Cabelo",
        "titulo": "Hair Love",
        "diretor": "Matthew A. Cherry, Everett Downing Jr. e Bruce W. Smith",
        "ano": 2019,
        "duracao": "6 minutos",
        "descricao": "Zuri, uma menina negra, precisa arrumar seu cabelo para uma ocasião especial e recebe a ajuda do pai, que aprende a cuidar dos cabelos da filha."
    },
    166: {
        "antigo": "Black Birt",
        "titulo": "Pássaro Preto",
        "diretor": "Maria Pereira",
        "duracao": "13 minutos"
    },
    168: {
        "antigo": "Disqui",
        "titulo": "Disque Quilombola",
        "diretor": "David Reeks",
        "ano": 2012,
        "duracao": "13 minutos",
        "descricao": "Crianças de uma comunidade quilombola e de um morro em Vitória conversam sobre suas raízes, brincadeiras e experiências de infância."
    },
    172: {
        "antigo": "Kalunga",
        "titulo": "Kalunga",
        "diretor": "Janaína de Figueiredo e Barbara Coimbra",
        "duracao": "12 minutos",
        "descricao": "Kaiá procura seu pai no grande Kalunga. A animação homenageia a comunidade Ilê Un Zambi e apresenta elementos da cultura afro-brasileira de matriz banto."
    },
    174: {
        "antigo": "Mar",
        "titulo": "O Papel e o Mar",
        "diretor": "Luiz Antonio Pilar",
        "duracao": "13 minutos",
        "descricao": "O filme apresenta um encontro imaginário entre João Cândido, líder da Revolta da Chibata, e Carolina Maria de Jesus, escritora de Quarto de Despejo."
    },
    175: {
        "antigo": "Menina",
        "titulo": "Menina Bonita do Laço de Fita",
        "diretor": "Diego Lopes e Claudio Bitencourt",
        "ano": 2014,
        "duracao": "7 minutos e 20 segundos",
        "descricao": "Um coelho fica encantado com a cor negra de sua vizinha e tenta descobrir como ficar parecido com ela. A animação aborda diversidade e valorização das diferenças."
    },
    180: {
        "antigo": "O Menino",
        "titulo": "O Menino que Engoliu o Choro",
        "diretor": "Joubert Amaral",
        "ano": 2025,
        "duracao": "6 minutos e 15 segundos",
        "descricao": "Animação inspirada no livro de Cris Pàz, que aborda emoções silenciadas e sentimentos que as crianças guardam."
    },
    184: {
        "antigo": "Pessoa",
        "titulo": "A Pessoa é para o que Nasce",
        "diretor": "Roberto Berliner",
        "ano": 1998,
        "duracao": "6 minutos",
        "descricao": "Documentário sobre três irmãs cegas que cantam em troca de esmolas em Campina Grande, na Paraíba."
    },
    190: {
        "antigo": "Visita Minha Pele",
        "titulo": "Vista a Minha Pele",
        "diretor": "Joel Zito Araújo",
        "ano": 2003,
        "duracao": "23 minutos",
        "descricao": "Uma história de realidade invertida na qual pessoas negras ocupam a posição social dominante e pessoas brancas enfrentam discriminação. O filme propõe uma reflexão sobre racismo e preconceito."
    },
    191: {
        "antigo": "Xadres",
        "titulo": "O Xadrez das Cores",
        "diretor": "Marco Schiavon",
        "ano": 2004,
        "duracao": "22 minutos",
        "descricao": "Cida, uma mulher negra, trabalha para Maria, uma senhora racista. A relação entre as duas muda quando Cida decide enfrentar as atitudes discriminatórias por meio de um jogo de xadrez."
    }
}

# Conferir os registros antes de alterar.
conexao = sqlite3.connect(BANCO)
cursor = conexao.cursor()

for id_obra, dados in obras.items():
    cursor.execute("""
        SELECT titulo, categoria, tipo
        FROM Obras
        WHERE id = ?
    """, (id_obra,))

    registro = cursor.fetchone()

    if registro is None:
        conexao.close()
        raise Exception(f"ID {id_obra} não encontrado.")

    titulo, categoria, tipo = registro

    if titulo != dados["antigo"]:
        conexao.close()
        raise Exception(
            f"Título diferente no ID {id_obra}: {titulo}. "
            "Nenhuma alteração foi realizada."
        )

    if str(categoria).lower() not in ("curta", "curtas") and \
       str(tipo).lower() not in ("curta", "curtas"):
        conexao.close()
        raise Exception(f"ID {id_obra} não pertence aos curtas.")

conexao.close()

# Criar backup.
data = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = f"instance/backup_14_curtas_{data}.db"
shutil.copy2(BANCO, backup)

print("Backup criado:", backup)

def esta_vazio(valor):
    if valor is None:
        return True

    texto = str(valor).strip().lower()

    return texto in (
        "",
        "não informado",
        "nao informado",
        "não identificado",
        "nao identificado",
        "descrição pendente de revisão."
    )

conexao = sqlite3.connect(BANCO)
cursor = conexao.cursor()

try:
    atualizados = 0

    for id_obra, dados in obras.items():
        cursor.execute("""
            SELECT diretor, ano_lancamento, duracao, descricao
            FROM Obras
            WHERE id = ?
        """, (id_obra,))

        atual = cursor.fetchone()

        diretor, ano, duracao, descricao = atual

        novos = {
            "titulo": dados["titulo"]
        }

        if esta_vazio(diretor):
            novos["diretor"] = dados.get("diretor")

        if (ano is None or ano == 0) and dados.get("ano"):
            novos["ano_lancamento"] = dados["ano"]

        if esta_vazio(duracao) and dados.get("duracao"):
            novos["duracao"] = dados["duracao"]

        if esta_vazio(descricao) and dados.get("descricao"):
            novos["descricao"] = dados["descricao"]

        conjunto = ", ".join(
            f"{campo} = ?" for campo in novos
        )

        valores = list(novos.values())
        valores.append(id_obra)

        cursor.execute(
            f"UPDATE Obras SET {conjunto} WHERE id = ?",
            valores
        )

        atualizados += 1
        print("Conferido:", dados["titulo"])

    conexao.commit()

    print("\nATUALIZAÇÃO CONCLUÍDA!")
    print("Registros processados:", atualizados)

except Exception:
    conexao.rollback()
    raise

finally:
    conexao.close()

print("Backup preservado:", backup)
print("\n3 registros continuam pendentes de identificação:")
print("- O Cabelo de Lelê")
print("- O Mundo de Dentro")
print("- Quijawua")
