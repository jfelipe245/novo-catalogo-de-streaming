
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // ==================================================
    // 1. ELEMENTOS PRINCIPAIS DO CATÁLOGO
    // ==================================================

    const container = document.getElementById('card-container');
    const pesquisa = document.getElementById('pesquisa');
    const botaoPesquisa = document.getElementById('botao-pesquisa');

    if (!container) {
        console.error(
            'AfroEdu: não encontrei o elemento #card-container.'
        );
        return;
    }

    const cards = Array.from(
        container.querySelectorAll('.card')
    );

    let categoriaAtual = 'todos';

    // ==================================================
    // 2. FUNÇÕES AUXILIARES
    // ==================================================

    // Padroniza textos para pesquisa e comparação.
    // Exemplo: "SÉRIES" passa a ser "series".
    function normalizar(texto) {
        return String(texto || '')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .toLowerCase()
            .trim();
    }

    // Obtém o título da obra.
    function tituloDo(card) {
        const elemento = card.querySelector('.titulo');

        return elemento
            ? elemento.textContent.trim()
            : '';
    }

    // Obtém o texto de um elemento e remove seu rótulo.
    function textoDo(card, seletor, prefixos) {
        const elemento = card.querySelector(seletor);

        if (!elemento) {
            return '';
        }

        let texto = elemento.textContent.trim();

        prefixos.forEach(function (prefixo) {
            texto = texto.replace(prefixo, '');
        });

        return texto.trim();
    }

    // Identifica os dados da obra usando o próprio cartão.
    function dadosDaObra(card) {
        const imagem = card.querySelector('img');

        return {
            titulo: tituloDo(card),

            categoria: card.dataset.category || '',

            genero: card.dataset.genero || '',

            autor: textoDo(card, '.autor', [
                /^(?:Autor(?:\/Diretor)?|Diretor|Artista)\s*:\s*/i
            ]),

            descricao: textoDo(card, '.descricao', [
                /^Descri[cç][aã]o\s*:\s*/i
            ]),

            imagem: imagem
                ? imagem.getAttribute('src') || ''
                : ''
        };
    }

    // ==================================================
    // 3. FILTROS POR CATEGORIA
    // ==================================================

    const categorias = [
        { valor: 'todos', texto: 'Todos' },
        { valor: 'livro', texto: 'Livros' },
        { valor: 'filme', texto: 'Filmes' },
        { valor: 'serie', texto: 'Séries' },
        { valor: 'documentario', texto: 'Documentários' },
        { valor: 'musica', texto: 'Músicas' },
        { valor: 'curta-metragem', texto: 'Curtas' }
    ];

    // Evita criar filtros duplicados caso o HTML já os tenha.
    let filtros = document.getElementById('filtros-catalogo');

    if (!filtros) {
        filtros = document.createElement('div');
        filtros.id = 'filtros-catalogo';
        filtros.className = 'filtros-catalogo';

        container.parentNode.insertBefore(filtros, container);
    }

    // Só cria os botões se ainda não existirem.
    if (!filtros.querySelector('[data-filter]')) {
        categorias.forEach(function (categoria) {
            const botao = document.createElement('button');

            botao.type = 'button';
            botao.textContent = categoria.texto;
            botao.dataset.filter = categoria.valor;
            botao.className = 'btn-filtro';

            if (categoria.valor === 'todos') {
                botao.classList.add('ativo');
                botao.setAttribute('aria-pressed', 'true');
            } else {
                botao.setAttribute('aria-pressed', 'false');
            }

            filtros.appendChild(botao);
        });
    }

    // ==================================================
    // 4. PESQUISA E FILTRAGEM
    // ==================================================

    let mensagem = document.getElementById('sem-resultados');

    if (!mensagem) {
        mensagem = document.createElement('p');
        mensagem.id = 'sem-resultados';
        mensagem.className = 'mensagem-catalogo-vazio';
        mensagem.textContent = 'Nenhuma obra encontrada.';
        mensagem.hidden = true;

        container.insertAdjacentElement('afterend', mensagem);
    }

    function atualizarCatalogo() {
        const termo = normalizar(pesquisa ? pesquisa.value : '');

        let encontrados = 0;

        cards.forEach(function (card) {
            const categoria = normalizar(card.dataset.category);
            const conteudo = normalizar(card.textContent);

            const correspondeCategoria =
                categoriaAtual === 'todos' ||
                categoria === normalizar(categoriaAtual);

            const correspondePesquisa =
                termo === '' || conteudo.includes(termo);

            const mostrar =
                correspondeCategoria && correspondePesquisa;

            card.hidden = !mostrar;

            if (mostrar) {
                encontrados++;
            }
        });

        mensagem.hidden = encontrados > 0;

        container.setAttribute(
            'aria-label',
            encontrados + ' obras encontradas'
        );
    }

    // Clicar em uma categoria.
    filtros.addEventListener('click', function (event) {
        const botao = event.target.closest('[data-filter]');

        if (!botao || !filtros.contains(botao)) {
            return;
        }

        categoriaAtual = botao.dataset.filter || 'todos';

        filtros.querySelectorAll('[data-filter]').forEach(
            function (outro) {
                const ativo =
                    outro.dataset.filter === categoriaAtual;

                outro.classList.toggle('ativo', ativo);
                outro.setAttribute('aria-pressed', String(ativo));
            }
        );

        atualizarCatalogo();
    });

    // Pesquisa enquanto a pessoa digita.
    if (pesquisa) {
        pesquisa.addEventListener('input', atualizarCatalogo);
    }

    // Botão de pesquisa.
    if (botaoPesquisa) {
        botaoPesquisa.addEventListener('click', function (event) {
            event.preventDefault();
            atualizarCatalogo();
        });
    }

    // ==================================================
    // 5. ENVIO DE FORMULÁRIOS POST
    // ==================================================

    // Envia campos de formulário ao Flask sem JSON.
    function enviarFormulario(url, campos) {
        if (!url) {
            alert(
                'O endereço desta função não está configurado. ' +
                'Confira as rotas no catálogo.html.'
            );

            return;
        }

        const formulario = document.createElement('form');

        formulario.method = 'POST';
        formulario.action = url;
        formulario.hidden = true;

        Object.entries(campos).forEach(function (par) {
            const campo = document.createElement('input');

            campo.type = 'hidden';
            campo.name = par[0];
            campo.value = par[1] == null ? '' : String(par[1]);

            formulario.appendChild(campo);
        });

        document.body.appendChild(formulario);
        formulario.submit();
    }

    // ==================================================
    // 6. ABRIR SAIBA MAIS
    // ==================================================

    function abrirDetalhes(card) {
        const obra = dadosDaObra(card);

        if (!obra.titulo) {
            alert('Não consegui identificar o título desta obra.');
            return;
        }

        const endereco =
            window.url_Saiba_Mais || '/saibamais';

        const destino = new URL(
            endereco,
            window.location.origin
        );

        Object.entries(obra).forEach(function (par) {
            destino.searchParams.set(par[0], par[1]);
        });

        window.location.href = destino.href;
    }

    // ==================================================
    // 7. ACESSAR LIVRO, FILME, SÉRIE OU OUTRA OBRA
    // ==================================================

    function acessarObra(card) {
        const obra = dadosDaObra(card);

        if (!obra.titulo) {
            alert('Não consegui identificar o título desta obra.');
            return;
        }

        const endereco =
            window.url_Obra || '/obra';

        const destino = new URL(
            endereco,
            window.location.origin
        );

        Object.entries(obra).forEach(function (par) {
            destino.searchParams.set(par[0], par[1]);
        });

        window.location.href = destino.href;
    }

    // ==================================================
    // 8. CONECTAR OS BOTÕES DE CADA CARTÃO
    // ==================================================

    cards.forEach(function (card) {

        // ----------------------------------------------
        // ADICIONAR AOS FAVORITOS
        // ----------------------------------------------

        const adicionar = card.querySelector(
            'button[class*="adicionar-catalogo"]'
        );

        adicionar?.addEventListener('click', function () {
            const obra = dadosDaObra(card);

            if (!obra.titulo || !obra.categoria) {
                alert(
                    'Não consegui identificar o título ou ' +
                    'a categoria desta obra.'
                );

                return;
            }

            const endereco =
                window.url_Adicionar_Favoritos ||
                '/adicionar_favoritos';

            enviarFormulario(endereco, {
                titulo: obra.titulo,
                categoria: obra.categoria,
                genero: obra.genero
            });
        });

        // ----------------------------------------------
        // LER OU ASSISTIR
        // ----------------------------------------------

        const acessar = card.querySelector(
            'button[class*="ler-catalogo"], ' +
            'button[class*="assistir-catalogo"]'
        );

        acessar?.addEventListener('click', function (event) {
            event.preventDefault();
            acessarObra(card);
        });

        // ----------------------------------------------
        // SAIBA MAIS
        // ----------------------------------------------

        const detalhes = card.querySelector('a.btn-info');

        detalhes?.addEventListener('click', function (event) {
            event.preventDefault();
            abrirDetalhes(card);
        });

        // ----------------------------------------------
        // REMOVER OU OCULTAR CARTÃO
        // ----------------------------------------------

        const remover = card.querySelector(
            'button[class*="remover-catalogo"]'
        );

        remover?.addEventListener('click', function () {
            const confirmar = window.confirm(
                'Deseja ocultar este cartão nesta página? ' +
                'Esta ação não apaga a obra do banco de dados.'
            );

            if (!confirmar) {
                return;
            }

            card.remove();

            const indice = cards.indexOf(card);

            if (indice !== -1) {
                cards.splice(indice, 1);
            }

            atualizarCatalogo();
        });
    });

    // ==================================================
    // 9. INICIALIZAÇÃO
    // ==================================================

    atualizarCatalogo();

    console.info(
        'AfroEdu Stream: catálogo carregado.',
        'Obras encontradas:',
        cards.length
    );
});
