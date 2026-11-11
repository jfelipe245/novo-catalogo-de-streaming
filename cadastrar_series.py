
import os
import shutil
import sqlite3
from datetime import datetime

banco = "instance/afroedu_streaming.db"
pasta = "static/css/image/img/tipos/series"

if not os.path.exists(banco):
    print("Banco de dados não encontrado.")
    raise SystemExit

# Faz uma cópia de segurança antes de alterar o banco
backup = "instance/backup_series_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".db"
shutil.copy2(banco, backup)
print("Backup criado:", backup)

# Dados das séries
series = [
    ("A História do Brasil: Eternizado na Sua Casa", "a-historia.jpg", None, None, None, None),
    ("A Ética do Silêncio", "a_etica_do_silencio.jpg", "Documentário", "Joel Zito Araújo", 2023, "Série documental sobre racismo e relações raciais."),
    ("Africanidade Brasileira e Educação", "africanidade.jpg", None, None, None, None),
    ("A Aparição", "aparicao.jpg", None, None, None, None),
    ("Aprender a Sonhar", "aprender.jpg", "Documentário", "Vítor Rocha", None, "Série documental sobre jovens quilombolas, indígenas e de periferias e o acesso à universidade."),
    ("Bad Education", "bad.jpg", "Comédia dramática", None, 2012, "Série britânica ambientada no cotidiano de uma escola."),
    ("Bianca e Pedro", "bia-pedro.jpg", None, None, None, None),
    ("Blood & Water", "blood-&-water.jpg", "Drama", None, 2020, "Série sul-africana sobre identidade, família e vida escolar."),
    ("Corações e Mentes: Escolas que Transformam", "coracoes.jpg", "Documentário", "Cacau Rhoden", 2018, "Série documental sobre escolas brasileiras que transformam a educação."),
    ("De Menor: A Série", "de-menor.jpg", "Drama", "Caru Alves de Souza", None, "Série de ficção sobre adolescentes e o sistema de justiça."),
    ("Dear White People", "dear-white-peaple.jpg", "Comédia dramática", "Justin Simien", 2017, "Série sobre estudantes negros, racismo e identidade em uma universidade."),
    ("Desafios nas Escolas", "desafios.jpg", None, None, None, None),
    ("Sex Education", "educacao.jpg", "Comédia dramática", "Laurie Nunn", 2019, "Série sobre adolescência, convivência escolar e educação."),
    ("Grand Army", "grand-army.jpg", "Drama", "Katie Cappiello", 2020, "Série sobre estudantes de uma escola pública do Brooklyn."),
    ("Greenhouse Academy", "greenhouse.jpg", "Drama juvenil", "Giora Chamizer", 2017, "Série juvenil ambientada em um colégio interno."),
    ("Longe Demais", "longe-demais.jpg", None, None, None, None),
    ("Malhação: A Vida e a Diferença", "malhacao.webp", "Drama juvenil", None, None, "Série juvenil brasileira sobre adolescência e vida escolar."),
    ("Master of None", "master-of-none.jpg", "Comédia dramática", "Aziz Ansari e Alan Yang", 2015, "Série sobre identidade cultural, carreira, amizade e relacionamentos."),
    ("Merlí", "merli.jpg", "Drama", "Héctor Lozano", 2015, "Série sobre um professor de filosofia que incentiva o pensamento crítico."),
    ("Pátria Educadora", "patria-educadora.jpg", None, None, 2020, None),
    ("O Fim da História", "patria.jpg", None, None, 2020, None),
    ("E aí, Professora?", "professora.jpg", "Educacional", None, None, "Programa sobre educação, formação docente e Educação de Jovens e Adultos."),
    ("Segunda Chamada", "segunda-chamada.jpg", "Drama", "Joana Jabace", 2019, "Série sobre professores e estudantes da Educação de Jovens e Adultos."),
    ("Sementes da Educação", "sementes.jpg", "Documentário", None, 2018, "Série documental sobre iniciativas inovadoras na educação pública."),
    ("SKAM", "skan.jpg", "Drama adolescente", "Julie Andem", 2015, "Série sobre juventude, escola, identidade e pertencimento."),
    ("The Chair", "the-chair.jpg", "Comédia dramática", "Amanda Peet e Annie Julia Wyman", 2021, "Série sobre uma professora que assume a direção de um departamento universitário."),
    ("The Edible", "the-edible.jpg", None, None, None, None)
]

conexao = sqlite3.connect(banco)
cursor = conexao.cursor()

inseridos = 0
existentes = 0
sem_imagem = 0

for titulo, arquivo, genero, diretor, ano, descricao in series:
    caminho = "css/image/img/tipos/series/" + arquivo
    arquivo_completo = os.path.join(pasta, arquivo)

    if not os.path.exists(arquivo_completo):
        print("Imagem não encontrada:", arquivo)
        sem_imagem += 1
        continue

    cursor.execute(
        'SELECT id FROM "Obras" WHERE imagem = ?',
        (caminho,)
    )

    if cursor.fetchone():
        print("Já cadastrado:", titulo)
        existentes += 1
        continue

    cursor.execute("""
        INSERT INTO "Obras"
        (titulo, categoria, genero, tipo, imagem, descricao,
         diretor, ano_lancamento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        titulo,
        "série",
        genero,
        "série",
        caminho,
        descricao,
        diretor,
        ano
    ))

    print("Cadastrado:", titulo)
    inseridos += 1

conexao.commit()
conexao.close()

print("\n===== RESULTADO =====")
print("Novos registros:", inseridos)
print("Já existentes:", existentes)
print("Imagens não encontradas:", sem_imagem)
print("Backup:", backup)
