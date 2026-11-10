from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'AfroEdu_RaizesDosSaberes_Conexao_2026!'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/meu github/meus projetos/catalogo de streaming/instance/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ==========================================
# MODELOS DO BANCO DE DADOS
# ==========================================

class Usuario(db.Model):
    __tablename__ = 'Usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    senha = db.Column(db.String(100), nullable=False)
    rua = db.Column(db.String(100), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)


class Livros(db.Model):
    __tablename__ = 'Livros'

    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    ano_lancamento = db.Column(db.Integer, nullable=False)


class Filmes(db.Model):
    __tablename__ = 'Filmes'

    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    diretor = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    ano_lancamento = db.Column(db.Integer, nullable=False)


class Series(db.Model):
    __tablename__ = 'Series'

    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    diretor = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    ano_lancamento = db.Column(db.Integer, nullable=False)


class Documentarios(db.Model):
    __tablename__ = 'Documentarios'

    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    diretor = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    ano_lancamento = db.Column(db.Integer, nullable=False)


class Curta_Metragem(db.Model):
    __tablename__ = 'Curta_Metragem'

    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    diretor = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    ano_lancamento = db.Column(db.Integer, nullable=False)


class Musica(db.Model):
    __tablename__ = 'Musica_de_protesto'

    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    artista = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    ano_lancamento = db.Column(db.Integer, nullable=False)


# CLASSE PRINCIPAL DE OBRAS
class Obra(db.Model):

    __tablename__ = "Obras"

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(200), nullable=False)
    genero = db.Column(db.String(100))
    tipo = db.Column(db.String(50))

    autor = db.Column(db.String(150))
    diretor = db.Column(db.String(150))
    artista = db.Column(db.String(150))
    album = db.Column(db.String(150))

    ano_publicacao = db.Column(db.Integer)
    ano_lancamento = db.Column(db.Integer)

    numero_paginas = db.Column(db.Integer)
    duracao = db.Column(db.String(50))
    temporadas = db.Column(db.Integer)

    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(255))

class Favorito(db.Model):
    __tablename__ = 'Favoritos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    genero = db.Column(db.String(50), nullable=False)


class saiba_mais(db.Model):
    __tablename__ = 'Saiba_Mais'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)


# ==========================================
# INÍCIO E LOGIN
# ==========================================

@app.route('/')
def home():
    return redirect(url_for('cadastrar_usuario'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')

        usuario = Usuario.query.filter_by(
            email=email,
            senha=senha
        ).first()

        if usuario:
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            session['usuario_email'] = usuario.email

            return redirect(url_for('catalogo'))

        return render_template(
            'entrar.html',
            error='E-mail ou senha inválidos.'
        )

    return render_template('entrar.html')

@app.route('/entrar')
def entrar():
    return render_template('entrar.html')

# ==========================================
# CADASTRO
# ==========================================

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'GET':
        return render_template('login.html')

    try:
        nome_usuario = request.form.get('Nome-Usuario', '').strip()
        nome = request.form.get('nome', '').strip()
        idade = request.form.get('idade', '').strip()
        cpf = request.form.get('cpf', '').strip()
        data_nascimento = request.form.get('data', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        senha = request.form.get('senha', '')
        rua = request.form.get('rua', '').strip()
        bairro = request.form.get('bairro', '').strip()
        endereco = request.form.get('endereco', '').strip()

        if not all([
            nome_usuario, nome, idade, cpf, data_nascimento,
            email, senha, rua, bairro, endereco
        ]):
            return render_template(
                'login.html',
                error='Preencha todos os campos obrigatórios.'
            )

        if not idade.isdigit():
            return render_template(
                'login.html',
                error='Digite uma idade válida.'
            )

        if Usuario.query.filter_by(email=email).first():
            return render_template(
                'login.html',
                error='Este e-mail já está cadastrado.'
            )

        if Usuario.query.filter_by(cpf=cpf).first():
            return render_template(
                'login.html',
                error='Este CPF já está cadastrado.'
            )

        novo_usuario = Usuario(
            nome_usuario=nome_usuario,
            nome=nome,
            idade=int(idade),
            cpf=cpf,
            data_nascimento=data_nascimento,
            email=email,
            telefone=telefone,
            senha=senha,
            rua=rua,
            bairro=bairro,
            endereco=endereco
        )

        db.session.add(novo_usuario)
        db.session.commit()

        session['usuario_id'] = novo_usuario.id
        session['usuario_nome'] = novo_usuario.nome
        session['usuario_email'] = novo_usuario.email

        return redirect(url_for('catalogo'))

    except Exception:
        db.session.rollback()
        app.logger.exception('Erro ao cadastrar usuário')

        return render_template(
            'login.html',
            error='Não foi possível concluir o cadastro. Confira o terminal.'
        )

@app.route('/cadastrar_obra', methods=['GET', 'POST'])
def cadastrar_obra():

    if request.method == 'POST':

        titulo = request.form.get('titulo', '').strip()
        tipo = request.form.get('tipo', '').strip().lower()

        tipos_validos = [
            'livro',
            'filme',
            'serie',
            'documentario',
            'musica',
            'curta'
        ]

        if not titulo:
            return render_template(
                'cadastrar_obra.html',
                error='O título é obrigatório.'
            )

        if tipo not in tipos_validos:
            return render_template(
                'cadastrar_obra.html',
                error='Selecione uma categoria válida.'
            )

        try:
            obra = Obra(
                titulo=titulo,
                tipo=tipo,
                genero=request.form.get('genero', '').strip(),
                descricao=request.form.get('descricao', '').strip(),
                imagem=request.form.get('imagem', '').strip(),
                autor=request.form.get('autor', '').strip(),
                diretor=request.form.get('diretor', '').strip(),
                artista=request.form.get('artista', '').strip(),
                album=request.form.get('album', '').strip(),
                ano_publicacao=request.form.get('ano_publicacao', type=int),
                ano_lancamento=request.form.get('ano_lancamento', type=int),
                numero_paginas=request.form.get('numero_paginas', type=int),
                duracao=request.form.get('duracao', '').strip(),
                temporadas=request.form.get('temporadas', type=int)
            )

            db.session.add(obra)
            db.session.commit()

            return redirect(url_for('catalogo'))

        except Exception:
            db.session.rollback()
            app.logger.exception('Erro ao cadastrar obra')

            return render_template(
                'cadastrar_obra.html',
                error='Erro ao salvar a obra.'
            )

    return render_template('cadastrar_obra.html')
# ==========================================
# CATÁLOGO PRINCIPAL
# ==========================================
@app.route('/catalogo')
def catalogo():

    obras = Obra.query.order_by(
        Obra.id.desc()
    ).all()

    livros = [o for o in obras if o.tipo == 'livro']
    filmes = [o for o in obras if o.tipo == 'filme']
    series = [o for o in obras if o.tipo == 'serie']
    documentarios = [o for o in obras if o.tipo == 'documentario']
    musicas = [o for o in obras if o.tipo == 'musica']
    curtas = [o for o in obras if o.tipo == 'curta']

    return render_template(
        'catalogo.html',
        obras=obras,
        livros=livros,
        filmes=filmes,
        series=series,
        documentarios=documentarios,
        musicas=musicas,
        curtas=curtas
    )
# ==========================================
# PÁGINAS DAS CATEGORIAS
# ==========================================
@app.route('/livros')
def livros():

    obras = Obra.query.filter_by(
        tipo="livro"
    ).order_by(Obra.id.desc()).all()

    return render_template(
        'tipos/livros.html',
        obras=obras,
        categoria='livros'
    )


@app.route('/filmes')
def filmes():
    obras = Obra.query.filter_by(
        tipo="filme"
    ).order_by(Obra.id.desc()).all()

    return render_template(
        'tipos/filmes.html',
        obras=obras,
        categoria='filmes'
    )


@app.route('/series')
def series():
    obras = Obra.query.filter_by(
        tipo="série"
    ).order_by(Obra.id.desc()).all()

    return render_template(
        'tipos/series.html',
        obras=obras,
        categoria='series'
    )


@app.route('/musica')
def musica():
    obras = Obra.query.filter_by(
        tipo="música"
    ).order_by(Obra.id.desc()).all()

    return render_template(
        'tipos/musicas.html',
        obras=obras,
        categoria='musica'
    )


@app.route('/documentarios')
def documentarios():
    obras = Obra.query.filter_by(
        tipo="documentário"
    ).order_by(Obra.id.desc()).all()

    return render_template(
        'tipos/documentarios.html',
        obras=obras,
        categoria='documentarios'
    )


@app.route('/curtas')
def curtas():
    obras = Obra.query.filter_by(
        tipo="curta"
    ).order_by(Obra.id.desc()).all()

    return render_template(
        'tipos/curtas.html',
        obras=obras,
        categoria='curtas'
    )


# ==========================================
# ROTA MEUS FAVORITOS
# ==========================================

@app.route('/meus_favoritos')
def meus_favoritos():

    favoritos = []

    if 'usuario_id' in session:
        favoritos = Favorito.query.filter_by(
            usuario_id=session['usuario_id']
        ).order_by(Favorito.id.desc()).all()

    return render_template(
        'funcoes/meus_favoritos.html',
        favoritos=favoritos
    )
#===========================================
# rota adicionar
#===========================================

@app.route('/adicionar_favoritos', methods=['POST'])
def adicionar_favoritos():

    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    titulo = request.form.get('titulo', '').strip()
    categoria = request.form.get('categoria', '').strip()
    genero = request.form.get('genero', '').strip()

    if not titulo or not categoria:
        return redirect(url_for('catalogo'))

    existente = Favorito.query.filter_by(
        usuario_id=session['usuario_id'],
        titulo=titulo,
        categoria=categoria
    ).first()

    if not existente:
        favorito = Favorito(
            usuario_id=session['usuario_id'],
            titulo=titulo,
            categoria=categoria,
            genero=genero
        )

        db.session.add(favorito)
        db.session.commit()

    return redirect(url_for('catalogo'))
# ==========================================
# ROTA ACESSAR OBRA
# ==========================================


@app.route('/acessar_obra')
def acessar_obra():

    campos = [
        'titulo',
        'imagem',
        'autor',
        'diretor',
        'artista',
        'categoria',
        'genero',
        'descricao',
        'ano_lancamento',
        'ano_publicacao',
        'paginas',
        'tipo'
    ]

    dados = {}

    for campo in campos:
        valor = request.args.get(campo, '')
        valor = (valor or '').strip()
    
        if valor.lower() in ['none', 'null', 'undefined']:
            valor = ''

        dados[campo] = valor

    return render_template(
        'funcoes/acessar_obra.html',
        **dados
    )


# ==========================================
# rota deletar FAVORITOS
# ==========================================

@app.route('/deletar_favorito', methods=['POST'])
def deletar_favorito():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    favorito_id = request.form.get(
        'favorito_id', request.form.get('id'), type=int
    )

    destino = (
        'catalogo'
        if request.form.get('origem') == 'catalogo'
        else 'meus_favoritos'
    )

    if favorito_id is None:
        return redirect(url_for(destino))

    favorito = Favorito.query.filter_by(
        id=favorito_id,
        usuario_id=session['usuario_id']
    ).first()

    if favorito is not None:
        db.session.delete(favorito)
        db.session.commit()

    return redirect(url_for(destino))


def obras_visiveis(modelo, categoria):
    obras = modelo.query.all()
    ocultas = session.get('obras_ocultas', {})

    ids_ocultos = set(
        ocultas.get(categoria, [])
    )

    return [
        obra for obra in obras
        if obra.id not in ids_ocultos
    ]

# ==========================================
# rota REMOVER OBRA TEMPORARIAMENTE DO CATÁLOGO
# ==========================================
@app.route('/remover', methods=['POST'])
def remover():

    obra_id = request.form.get('obra_id', type=int)

    if not obra_id:
        return redirect(url_for('catalogo'))

    obra = db.session.get(Obra, obra_id)

    if obra:

        obras_ocultas = session.get('obras_ocultas', [])

        if obra_id not in obras_ocultas:
            obras_ocultas.append(obra_id)

        session['obras_ocultas'] = obras_ocultas

        return redirect(url_for('catalogo'))
    return render_template('funcoes/remover.html', obra=obra)
#============================================
# rota deletar                                     #
#============================================
@app.route('/deletar', methods=['GET'])
def deletar():
    return render_template(
        'remover.html',
        titulo=request.args.get('titulo', ''),
        categoria=request.args.get('categoria', ''),
        obra_id=request.args.get('obra_id', '')
    )

# ==========================================
# rota SAIBA MAIS
# ==========================================

@app.route('/saibamais')
def saiba_mais():
    return render_template(
        'funcoes/Saiba-Mais.html',
        titulo=request.args.get('titulo', 'Obra'),
        categoria=request.args.get('categoria', ''),
        genero=request.args.get('genero', ''),
        autor=request.args.get('autor', ''),
        imagem=request.args.get('imagem', ''),
        descricao=request.args.get('descricao', '')
    )

# ==========================================
# rota SAIR
# ==========================================

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
