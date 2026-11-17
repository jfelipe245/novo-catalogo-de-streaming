from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)

app.config['SECRET_KEY'] = 'jao2020'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///afroedu_streaming.db'

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
    cidade = db.Column(db.String(100), nullable=False)


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

    __tablename__ = 'Obras'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)

    categoria = db.Column(db.String(50), nullable=True)
    genero = db.Column(db.String(100))
    tipo = db.Column(db.String(50))

    subtitulo = db.Column(db.String(255), nullable=True)
    autor = db.Column(db.String(150))
    editora = db.Column(db.String(150), nullable=True)
    edicao = db.Column(db.String(50))
    isbn = db.Column(db.String(20), nullable=True)

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

    favoritos = db.relationship(
        'Favorito',
        back_populates='obra',
        cascade='all, delete-orphan'
    )

    informacoes = db.relationship(
        'SaibaMais',
        back_populates='obra',
        cascade='all, delete-orphan'
    )


# ==========================================
# MODELO DE FAVORITOS
# ==========================================

class Favorito(db.Model):

    __tablename__ = 'Favoritos'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('Usuarios.id'),
        nullable=False
    )

    obra_id = db.Column(
        db.Integer,
        db.ForeignKey('Obras.id'),
        nullable=False
    )

    obra = db.relationship(
        'Obra',
        back_populates='favoritos'
    )

class SaibaMais(db.Model):

    __tablename__ = 'Saiba_Mais'

    id = db.Column(db.Integer, primary_key=True)

    obra_id = db.Column(
        db.Integer,
        db.ForeignKey('Obras.id'),
        nullable=False
    )

    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)

    obra = db.relationship(
        'Obra',
        back_populates='informacoes'
    )

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

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario is None:
            return render_template(
                'entrar.html',
                error='E-mail ou senha inválidos.'
            )

        if usuario.senha != senha:
            return render_template(
                'entrar.html',
                error='E-mail ou senha inválidos.'
            )

        session.clear()
        session['usuario_id'] = usuario.id
        session['usuario_nome'] = usuario.nome
        session['usuario_email'] = usuario.email

        return redirect(url_for('catalogo'))

    return render_template('entrar.html')


@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    return login()
# ==========================================
# CADASTRO
# ======================================


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_usuario():
    if request.method == 'GET':
        return render_template('login.html')

    try:
        nome_usuario = request.form.get('nome_usuario', '').strip()
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
        cidade = request.form.get('cidade', '').strip()

        if not all([
            nome_usuario, nome, idade, cpf,
            data_nascimento, email, senha, telefone, rua, bairro, endereco, cidade
        ]):
            return render_template(
                'login.html',
                error='Preencha todos os campos obrigatórios.'
            )

        if not idade.isdigit() or not 1 <= int(idade) <= 120:
            return render_template(
                'login.html',
                error='Digite uma idade válida.'
            )

        if len(senha) < 8:
            return render_template(
                'login.html',
                error='A senha deve ter pelo menos 8 caracteres.'
            )

        if Usuario.query.filter_by(email=email).first():
            return render_template(
                'login.html',
                error='Este e-mail já está cadastrado.'
            )

        if nome_usuario:
            if Usuario.query.filter_by(
                nome_usuario=nome_usuario
            ).first():
                return render_template(
                    'login.html',
                    error='Este nome de usuário já está cadastrado.'
                )

        if cpf:
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
            telefone=telefone or None,
            senha=senha,
            rua=rua or '',
            bairro=bairro or '',
            endereco=endereco or '',
            cidade=cidade or ''
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


# ==========================================
# CATÁLOGO PRINCIPAL
# ==========================================


@app.route('/catalogo')
def catalogo():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    # Carrega todas as obras, sem ocultar nenhuma pelo histórico da sessão.
    obras = Obra.query.order_by(Obra.id.desc()).all()

    livros = [o for o in obras if o.categoria == 'livro']
    filmes = [o for o in obras if o.categoria == 'filme']

    series = [
        o for o in obras
        if o.categoria in ['serie', 'série']
    ]

    documentarios = [
        o for o in obras
        if o.categoria in ['documentario', 'documentário']
    ]

    musicas = [
        o for o in obras
        if o.categoria in ['musica', 'música']
    ]

    curtas = [
        o for o in obras
        if o.categoria == 'curta'
    ]

    favoritos = Favorito.query.filter_by(
        usuario_id=session['usuario_id']
    ).all()

    return render_template(
        'catalogo.html',
        obras=obras,
        livros=livros,
        filmes=filmes,
        series=series,
        documentarios=documentarios,
        musicas=musicas,
        curtas=curtas,
        favoritos=favoritos,
        nome=session.get('usuario_nome', 'Visitante')
    )


# ==========================================
# PÁGINAS DAS CATEGORIAS
# ==========================================
@app.route('/livros')
def livros():

    obras = Obra.query.filter_by(
        categoria="livro"
    ).order_by(Obra.id.desc()).all()

    return render_template(
        'tipos/livros.html',
        obras=obras,
        categoria='livros'
    )


@app.route('/filmes')
def filmes():
    obras = Obra.query.filter_by(
        categoria="filme"
    ).order_by(Obra.id.desc()).all()

    return render_template(
        'tipos/filmes.html',
        obras=obras,
        categoria='filmes'
    )


@app.route('/series')
def series():
    obras = Obra.query.filter(
        Obra.categoria.in_(['serie', 'série'])
    ).order_by(Obra.id.desc()).all()

    return render_template(
        'tipos/series.html',
        obras=obras,
        categoria='series'
    )


@app.route('/documentarios')
def documentarios():
    obras = Obra.query.filter(
        Obra.categoria.in_(['documentario', 'documentário'])
    ).order_by(Obra.id.desc()).all()

    return render_template(
        'tipos/documentarios.html',
        obras=obras,
        categoria='documentarios'
    )


@app.route('/musica')
def musica():
    obras = Obra.query.filter(
        Obra.tipo.in_(['musica', 'música'])
    ).order_by(Obra.id.desc()).all()

    return render_template(
        'tipos/musicas.html',
        obras=obras,
        categoria='musica'
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

    if 'usuario_id' not in session:
        return redirect(url_for('login'))

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

    obra_id = request.form.get('obra_id', type=int)

    if not obra_id:
        return redirect(url_for('catalogo'))

    obra = db.session.get(Obra, obra_id)

    if obra is None:
        return redirect(url_for('catalogo'))

    existente = Favorito.query.filter_by(
        usuario_id=session['usuario_id'],
        obra_id=obra_id
    ).first()

    if existente is None:
        favorito = Favorito(
            usuario_id=session['usuario_id'],
            obra_id=obra_id
        )

        db.session.add(favorito)
        db.session.commit()

    return redirect(url_for('catalogo'))
# ==========================================
# ROTA ACESSAR OBRA
# ==========================================


@app.route('/acessar_obra/<int:obra_id>')
def acessar_obra(obra_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    obra = Obra.query.get_or_404(obra_id)

    categoria = (obra.categoria or obra.tipo or '').lower().strip()

    campos = {
        'livro': [
            ('Autor', obra.autor),
            ('Editora', obra.editora),
            ('Edição', obra.edicao),
            ('ISBN', obra.isbn),
            ('Ano de publicação', obra.ano_publicacao),
            ('Número de páginas', obra.numero_paginas),
            ('Gênero', obra.genero)
        ],
        'filme': [
            ('Diretor', obra.diretor),
            ('Ano de lançamento', obra.ano_lancamento),
            ('Duração', obra.duracao),
            ('Gênero', obra.genero)
        ],
        'serie': [
            ('Diretor', obra.diretor),
            ('Ano de lançamento', obra.ano_lancamento),
            ('Temporadas', obra.temporadas),
            ('Gênero', obra.genero)
        ],
        'documentario': [
            ('Diretor', obra.diretor),
            ('Ano de lançamento', obra.ano_lancamento),
            ('Duração', obra.duracao),
            ('Gênero', obra.genero)
        ],
        'curta': [
            ('Diretor', obra.diretor),
            ('Ano de lançamento', obra.ano_lancamento),
            ('Duração', obra.duracao),
            ('Gênero', obra.genero)
        ],
        'musica': [
            ('Artista', obra.artista),
            ('Álbum', obra.album),
            ('Ano de lançamento', obra.ano_lancamento),
            ('Gênero', obra.genero)
        ]
    }

    campos_obra = campos.get(categoria, [])

    return render_template(
        'funcoes/acessar_obra.html',
        obra=obra,
        campos_obra=campos_obra
    )


@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':

        titulo = request.form.get('titulo', '').strip()
        tipo = request.form.get('tipo', '').strip()

        tipos_permitidos = [
            'livro', 'filme', 'serie',
            'documentario', 'curta', 'musica'
        ]

        if not titulo or tipo not in tipos_permitidos:
            return render_template(
                'funcoes/adicionar.html',
                mensagem='Informe um título e uma categoria válida.'
            )

        try:
            def numero(campo):
                valor = request.form.get(campo, '').strip()
                return int(valor) if valor else None

            obra = Obra(
                titulo=titulo,
                categoria=tipo,
                tipo=tipo,
                genero=request.form.get('genero', '').strip() or None,
                imagem=request.form.get('imagem', '').strip() or None,
                descricao=request.form.get('descricao', '').strip() or None,
                autor=request.form.get('autor', '').strip() or None,
                diretor=request.form.get('diretor', '').strip() or None,
                artista=request.form.get('artista', '').strip() or None,
                album=request.form.get('album', '').strip() or None,
                ano_publicacao=numero('ano_publicacao'),
                ano_lancamento=numero('ano_lancamento'),
                numero_paginas=numero('numero_paginas'),
                duracao=request.form.get('duracao', '').strip() or None,
                temporadas=numero('temporadas')
            )

            db.session.add(obra)
            db.session.commit()

            return redirect(url_for('catalogo'))

        except ValueError:
            db.session.rollback()
            return render_template(
                'funcoes/adicionar.html',
                mensagem='Confira os campos numéricos.'
            )

        except Exception:
            db.session.rollback()
            app.logger.exception('Erro ao cadastrar obra')

            return render_template(
                'funcoes/adicionar.html',
                mensagem='Erro ao cadastrar obra. Consulte o terminal.'
            )

    return render_template('funcoes/adicionar.html')

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
    if 'usuario_id' not in session:
        return redirect(url_for('login'))



    return redirect(url_for('catalogo'))


@app.route('/restaurar/<int:obra_id>', methods=['POST'])
def restaurar(obra_id):

    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    obras_ocultas = session.get('obras_ocultas', [])

    if obra_id in obras_ocultas:
        obras_ocultas.remove(obra_id)

    session['obras_ocultas'] = obras_ocultas
    session.modified = True

    return redirect(url_for('catalogo'))
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

@app.route('/saibamais/<int:id>',methods=['GET'])
def saiba_mais(id):
    obra_id = id

    if not obra_id:
        obra_id = request.args.get('obra_id', type=int)

    obra = db.session.get(Obra, obra_id) if obra_id else None

    if obra is None:
        return redirect(url_for('catalogo'))

    informacao = SaibaMais.query.filter_by(
        obra_id=obra.id
    ).first()

    return render_template(
        'funcoes/Saiba-Mais.html',
        obra=obra,
        titulo=obra.titulo or '',
        categoria=obra.categoria or obra.tipo or '',
        genero=obra.genero or '',
        autor=obra.autor or obra.diretor or obra.artista or '',
        imagem=obra.imagem or '',
        descricao=(
            informacao.descricao
            if informacao and informacao.descricao
            else obra.descricao or ''
        ),
        ano_publicacao=obra.ano_publicacao or '',
        ano_lancamento=obra.ano_lancamento or '',
        editora=obra.editora or '',
        numero_paginas=obra.numero_paginas or '',
        diretor=obra.diretor or '',
        artista=obra.artista or '',
        edicao=obra.edicao or '',
        album=obra.album or '',
        duracao=obra.duracao or '',
        temporadas=obra.temporadas or ''
    )

# ==========================================
# rota SAIR
# ==========================================

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
