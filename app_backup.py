from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'AfroEdu_RaizesDosSaberes_Conexao_2026!'

app.config['SQLALCHEMY_DATABASE_URI'] = (r'sqlite:///D:/meu github/meus projetos/catalogo de streaming/login.db')
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


class Musica_de_protesto(db.Model):
    __tablename__ = 'Musica_de_protesto'

    id = db.Column(db.Integer, primary_key=True)
    genero = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    artista = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    ano_lancamento = db.Column(db.Integer, nullable=False)


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
    return redirect(url_for('cadastrar_usuarios'))


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
def cadastrar_usuarios():
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


# ==========================================
# CATÁLOGO PRINCIPAL
# ==========================================

@app.route('/catalogo')
def catalogo():
    favoritos = []

    if 'usuario_id' in session:
        favoritos = Favorito.query.filter_by(
            usuario_id=session['usuario_id']
        ).all()

    dados_favoritos = [
        {'id': favorito.id, 'titulo': favorito.titulo}
        for favorito in favoritos
    ]

    return render_template(
        'catalogo.html',
        nome=session.get('usuario_nome'),
        favoritos=favoritos,
        dados_favoritos=dados_favoritos
    )


# ==========================================
# PÁGINAS DAS CATEGORIAS
# ==========================================

@app.route('/livros')
def livros():
    obras = Livros.query.order_by(Livros.id.desc()).all()

    return render_template(
        'livros.html',
        obras=obras,
        categoria='livros'
    )


@app.route('/filmes')
def filmes():
    obras = Filmes.query.order_by(Filmes.id.desc()).all()

    return render_template(
        'filmes.html',
        obras=obras,
        categoria='filmes'
    )


@app.route('/series')
def series():
    obras = Series.query.order_by(Series.id.desc()).all()

    return render_template(
        'series.html',
        obras=obras,
        categoria='series'
    )


@app.route('/musica')
def musica():
    obras = Musica_de_protesto.query.order_by(
        Musica_de_protesto.id.desc()
    ).all()

    return render_template(
        'musica.html',
        obras=obras,
        categoria='musica'
    )


@app.route('/documentarios')
def documentarios():
    obras = Documentarios.query.order_by(
        Documentarios.id.desc()
    ).all()

    return render_template(
        'documentarios.html',
        obras=obras,
        categoria='documentarios'
    )


@app.route('/curtas')
def curtas():
    obras = Curta_Metragem.query.order_by(
        Curta_Metragem.id.desc()
    ).all()

    return render_template(
        'tipos/curtas.html',
        obras=obras,
        categoria='curtas'
    )


# ==========================================
# FAVORITOS
# ==========================================

@app.route('/meus_favoritos')
def meus_favoritos():
    favoritos = Favorito.query.filter_by(
        usuario_id=session['usuario_id']
    ).order_by(Favorito.id.desc()).all()

    return render_template(
        'meus_favoritos.html',
        favoritos=favoritos
    )
    return redirect(url_for('login'))


@app.route('/adicionar_favoritos', methods=['POST'])
def adicionar_favoritos():
    titulo = request.form.get('titulo', '').strip()
    categoria = request.form.get('categoria', '').strip()
    genero = request.form.get('genero', '').strip()

    favorito = Favorito.query.filter_by(
        usuario_id=session['usuario_id'],
        titulo=titulo,
        categoria=categoria)
        
    favorito = Favorito(
            usuario_id=session['usuario_id'],
            titulo=titulo,
            categoria=categoria,
            genero=genero
        ).first()

    db.session.add(favorito)
    db.session.commit()

@app.route('/remover_favoritos', methods=['POST'])
def remover_favoritos():
    favorito_id=[]
    favorito = Favorito.query.filter_by(id=favorito_id,usuario_id=session['usuario_id']).first()

    if favorito:
        db.session.delete(favorito)
        db.session.commit()

# ==========================================
# SAIBA MAIS
# ==========================================

@app.route('/saibamais')
def saiba_mais():
    return render_template(
        'Saiba-Mais.html',
        titulo=request.args.get('titulo', 'Obra'),
        categoria=request.args.get('categoria', ''),
        genero=request.args.get('genero', ''),
        autor=request.args.get('autor', ''),
        imagem=request.args.get('imagem', ''),
        descricao=request.args.get('descricao', '')
    )


# ==========================================
# PÁGINA DA OBRA
# ==========================================

@app.route('/obra')
def obra():
    return render_template(
        'acessar_obra.html',
        titulo=request.args.get('titulo', 'Obra'),
        autor=request.args.get('autor', ''),
        descricao=request.args.get('descricao', ''),
        categoria=request.args.get('categoria', ''),
        genero=request.args.get('genero', ''),
        imagem=request.args.get('imagem', ''),
        arquivo=request.args.get('arquivo', ''),
        detalhes=request.args.get('detalhes', '')
    )


# ==========================================
# SAIR
# ==========================================

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
