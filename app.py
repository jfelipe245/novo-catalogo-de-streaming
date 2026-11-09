from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
cadastro = "straming educacional.db"

app = Flask(__name__)
app.secret_key = 'AfroEdu_RaizesDosSaberes_Conexao_2026!'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////workspaces/catalogo-de-streaming/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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

# class Series(db.Model):
#    __tablename__ = 'Series'#

#     id = db.Column(db.Integer, primary_key=True)
#     genero = db.Column(db.String(50), nullable=False)
#     tipo = db.Column(db.String(50), nullable=False)
#     imagem = db.Column(db.String(200), nullable=False)
#     titulo = db.Column(db.String(100), nullable=False)
#     diretor = db.Column(db.String(100), nullable=False)
#     descricao = db.Column(db.Text, nullable=False)
#     ano_lancamento = db.Column(db.Integer, nullable=False)

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

# class Musica_de_protesto(db.Model):
#     __tablename__ = 'Musica_de_protesto'

#     id = db.Column(db.Integer, primary_key=True)
#     genero = db.Column(db.String(50), nullable=False)
#     tipo = db.Column(db.String(50), nullable=False)
#     imagem = db.Column(db.String(200), nullable=False)
#     titulo = db.Column(db.String(100), nullable=False)
#     artista = db.Column(db.String(100), nullable=False)
#     descricao = db.Column(db.Text, nullable=False)
#     ano_lancamento = db.Column(db.Integer, nullable=False)

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

@app.route('/')
def home():
    return redirect(url_for('cadastrar_Usuario'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(
            email=email,
            senha=senha
        ).first()

        if usuario:
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            return redirect(url_for('catalogo'))

        return render_template(
            'entrar.html',
            error='E-mail ou senha inválidos.'
        )

    return render_template('entrar.html')



@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_Usuario():
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
                error='Preencha todos os campos obrigatorios.'
            )

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return render_template(
                'login.html',
                error='Este e-mail ja esta cadastrado.'
            )

        cpf_existente = Usuario.query.filter_by(cpf=cpf).first()
        if cpf_existente:
            return render_template(
                'login.html',
                error='Este CPF ja esta cadastrado.'
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

    except ValueError:
        db.session.rollback()
        return render_template(
            'login.html',
            error='Confira se a idade foi preenchida corretamente.'
        )

    except Exception:
        db.session.rollback()
        app.logger.exception('Erro ao cadastrar usuario')
        return render_template(
            'login.html',
            error='Falha ao salvar o cadastro. Confira o terminal.'
        )

    return render_template(
        'login.html',
        error='O cadastro terminou sem concluir a operacao.'
    )


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html', nome=session.get('usuario_nome'))

@app.route('/meus_favoritos')
def meus_favoritos():
    
    return render_template('meus_favoritos.html')

@app.route('/adicionar_favoritos', methods=['POST'])
def adicionar_favoritos():
    titulo = request.form.get('titulo')
    categoria = request.form.get('categoria')
    genero = request.form.get('genero')


    db.session.addn()
    db.session.commit()
    return redirect(url_for('catalogo'))

@app.route('/remover_favoritos', methods=['POST'])
def remover_favoritos():
    favorito_id = request.form.get('favorito_id')
    favorito = Favorito.query.get(favorito_id)
    if favorito:
        db.session.delete(favorito)
        db.session.commit()

    return redirect(url_for('meus_favoritos'))

@app.route('/saiba-mais')
def saiba_mais():
    titulo = request.args.get('titulo', 'Obra')
    categoria = request.args.get('categoria', '')
    genero = request.args.get('genero', '')

    return render_template(
        'Saiba-Mais.html',
        titulo=titulo,
        categoria=categoria,
        genero=genero
    )

@app.route('/obra')
def obra():
    titulo = request.args.get('titulo', 'Obra')
    autor = request.args.get('autor', '')
    descricao = request.args.get('descricao', '')
    categoria = request.args.get('categoria', '')
    genero = request.args.get('genero', '')
    imagem = request.args.get('imagem', '')
    arquivo = request.args.get('arquivo', '')
    detalhes = request.args.get('detalhes', '')

    return render_template(
        'obra.html',
        titulo=titulo,
        autor=autor,
        descricao=descricao,
        categoria=categoria,
        genero=genero,
        imagem=imagem,
        arquivo=arquivo,
        detalhes=detalhes
    )

if __name__ == '__main__':
    app.run(debug=True)