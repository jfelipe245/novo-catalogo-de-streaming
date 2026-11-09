
document.addEventListener('DOMContentLoaded', () => {

    // =====================================================
    // ELEMENTOS DO CATÁLOGO
    // =====================================================

    const botoes_Filtro = document.querySelectorAll(
        '.filter-btn, .btn-filtro'
    );

    const cards = document.querySelectorAll('.card');

    const Pesquisa = document.getElementById('pesquisa');
    const botao_Pesquisa = document.getElementById('botao-pesquisa');
    const container = document.getElementById('card-container');

    const botaoTodos = document.getElementById('botao-todos');
    const opcoesCategorias = document.getElementById('opcoes-categorias');

    const links_saiba_mais = document.querySelectorAll(
        '.Saiba-Mais a, .saiba-mais a, a.saiba_mais, a.btn-info'
    );

    const STORAGE_KEY = 'meu_catalogo_educacional';
    const REMOVIDOS_KEY = 'catalogo_itens_removidos';

    const filtrosPermitidos = [
        'todos',
        'livro',
        'filme',
        'documentario',
        'curta-metragem',
        'series',
        'musica_de_protesto'
    ];

    let categoria_Atual = 'todos';


    // =====================================================
    // NORMALIZAR TEXTO
    // =====================================================

    function Texto(texto) {
        return String(texto || '')
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .trim();
    }


    // =====================================================
    // LOCALSTORAGE
    // =====================================================

    function lerStorage(chave) {
        try {
            const dados = JSON.parse(
                localStorage.getItem(chave) || '[]'
            );

            return Array.isArray(dados) ? dados : [];
        } catch (erro) {
            console.error('Erro ao ler os dados:', erro);
            return [];
        }
    }

    function salvarStorage(chave, dados) {
        try {
            localStorage.setItem(chave, JSON.stringify(dados));
            return true;
        } catch (erro) {
            console.error('Erro ao salvar os dados:', erro);
            alert('Não foi possível salvar os dados no navegador.');
            return false;
        }
    }

    function obter_Favoritos() {
        return lerStorage(STORAGE_KEY);
    }

    function obter_Removidos() {
        return lerStorage(REMOVIDOS_KEY);
    }


    // =====================================================
    // INFORMAÇÕES DOS CARDS
    // =====================================================

    function obter_Titulo(card) {
        const elemento = card.querySelector(
            '.titulo, .Título, .titulo-obra'
        );

        if (elemento && elemento.textContent.trim()) {
            return elemento.textContent.trim();
        }

        const tituloAlternativo = card.querySelector('h2, h3');

        return tituloAlternativo?.textContent.trim()
            || 'Obra sem título';
    }

    function obter_Autor(card) {
        const elemento = card.querySelector(
            '.Autor, .autor, .autor-diretor'
        );

        if (!elemento) return '';

        return elemento.textContent
            .replace(/Autor\s*\/\s*Diretor\s*:/i, '')
            .replace(/^Autor\s*:/i, '')
            .replace(/^Diretor\s*:/i, '')
            .trim();
    }


    // =====================================================
    // MENSAGEM DE RESULTADOS
    // =====================================================

    function verificar_Resultado(quantidadeVisivel) {
        if (!container) return;

        let mensagem = document.getElementById(
            'mensagem-semresultados'
        );

        if (!mensagem) {
            mensagem = document.createElement('p');
            mensagem.id = 'mensagem-semresultados';

            mensagem.style.gridColumn = '1 / -1';
            mensagem.style.textAlign = 'center';
            mensagem.style.padding = '40px';
            mensagem.style.color = '#F5E8D3';
            mensagem.style.fontSize = '1.1rem';

            container.appendChild(mensagem);
        }

        mensagem.textContent = quantidadeVisivel === 0
            ? 'Nenhum item encontrado com esses critérios.'
            : '';

        mensagem.style.display = quantidadeVisivel === 0
            ? 'block'
            : 'none';
    }


    // =====================================================
    // PESQUISA, FILTROS E VISIBILIDADE
    // =====================================================

    function atualizar_Cards() {
        const texto_Pesquisa = Texto(Pesquisa?.value);
        const itens_Removidos = obter_Removidos();

        let quantidadeVisivel = 0;

        cards.forEach((card) => {
            const categoria = Texto(card.dataset.category || '');
            const titulo = Texto(obter_Titulo(card));
            const autor = Texto(obter_Autor(card));
            const conteudoCard = Texto(card.innerText);

            const corresponde_Categoria =
                categoria_Atual === 'todos' ||
                categoria === Texto(categoria_Atual);

            const corresponde_Pesquisa =
                !texto_Pesquisa ||
                titulo.includes(texto_Pesquisa) ||
                autor.includes(texto_Pesquisa) ||
                conteudoCard.includes(texto_Pesquisa);

            const foi_Removido = itens_Removidos.some(
                (item) => Texto(item) === titulo
            );

            const deveMostrar =
                corresponde_Categoria &&
                corresponde_Pesquisa &&
                !foi_Removido;

            card.style.display = deveMostrar ? '' : 'none';

            if (deveMostrar) {
                quantidadeVisivel++;
            }
        });

        verificar_Resultado(quantidadeVisivel);
    }


    // =====================================================
    // MENU DE CATEGORIAS
    // =====================================================

    if (botaoTodos && opcoesCategorias) {

        botaoTodos.addEventListener('click', (event) => {
            event.preventDefault();

            opcoesCategorias.classList.toggle('aberto');
        });

        opcoesCategorias.addEventListener('click', (event) => {
            const botao = event.target.closest('[data-filter]');

            if (!botao) return;

            event.preventDefault();

            const filtro = Texto(
                botao.dataset.filter || 'todos'
            );

            if (!filtrosPermitidos.includes(filtro)) {
                console.warn('Categoria não reconhecida:', filtro);
                return;
            }

            categoria_Atual = filtro;

            botaoTodos.textContent =
                botao.textContent.trim() + ' ▾';

            opcoesCategorias.classList.remove('aberto');

            botoes_Filtro.forEach((item) => {
                item.classList.remove('active', 'ativo');
            });

            botao.classList.add('active', 'ativo');

            atualizar_Cards();
        });

        document.addEventListener('click', (event) => {
            if (!event.target.closest('.menu-categorias')) {
                opcoesCategorias.classList.remove('aberto');
            }
        });
    }


    // =====================================================
    // BOTÕES DE FILTRO
    // =====================================================

    botoes_Filtro.forEach((botao) => {

        botao.addEventListener('click', (event) => {
            event.preventDefault();

            const filtro = Texto(
                botao.dataset.filter || 'todos'
            );

            if (filtro === 'home') {
                categoria_Atual = 'todos';
                atualizar_Cards();

                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });

                return;
            }

            if (filtro === 'catalogo') {
                categoria_Atual = 'todos';
                atualizar_Cards();

                container?.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                return;
            }

            if (!filtrosPermitidos.includes(filtro)) {
                console.warn('Filtro não reconhecido:', filtro);
                return;
            }

            categoria_Atual = filtro;

            botoes_Filtro.forEach((item) => {
                item.classList.remove('active', 'ativo');
            });

            botao.classList.add('active', 'ativo');

            atualizar_Cards();
        });

    });


    // =====================================================
    // EVENTOS DA PESQUISA
    // =====================================================

    if (Pesquisa) {
        Pesquisa.addEventListener('input', atualizar_Cards);

        Pesquisa.addEventListener('keydown', (event) => {
            if (event.key === 'Enter') {
                event.preventDefault();
                atualizar_Cards();
            }
        });
    }

    if (botao_Pesquisa) {
        botao_Pesquisa.addEventListener('click', (event) => {
            event.preventDefault();
            atualizar_Cards();
        });
    }


    // =====================================================
    // SAIBA MAIS
    // =====================================================

    function abrir_Saiba_Mais(card, link) {
        const destino =
            link?.getAttribute('href') ||
            window.url_Saiba_Mais;

        if (!destino || destino === '#') {
            console.error(
                'URL de Saiba Mais não encontrada.'
            );
            return;
        }

        const url = new URL(destino, window.location.href);

        url.searchParams.set('titulo', obter_Titulo(card));

        const autor = obter_Autor(card);

        if (autor) {
            url.searchParams.set('autor', autor);
        }

        url.searchParams.set(
            'categoria',
            card.dataset.category || ''
        );

        url.searchParams.set(
            'genero',
            card.dataset.genero || ''
        );

        window.location.href = url.href;
    }

    links_saiba_mais.forEach((link) => {
        link.addEventListener('click', (event) => {
            const card = link.closest('.card');

            if (!card) return;

            event.preventDefault();

            try {
                abrir_Saiba_Mais(card, link);
            } catch (erro) {
                console.error(
                    'Erro ao abrir Saiba Mais:',
                    erro
                );
            }
        });
    });


    // =====================================================
    // ADICIONAR AOS FAVORITOS
    // =====================================================

    function adicionar_Favorito(card) {
        const titulo = obter_Titulo(card);
        const favoritos = obter_Favoritos();

        const jaExiste = favoritos.some(
            (item) => Texto(item) === Texto(titulo)
        );

        if (jaExiste) {
            alert(`"${titulo}" já está nos seus favoritos.`);
            return;
        }

        favoritos.push(titulo);

        if (salvarStorage(STORAGE_KEY, favoritos)) {
            alert(`"${titulo}" foi adicionado aos favoritos! ❤️`);
        }
    }


    // =====================================================
    // REMOVER DOS FAVORITOS
    // =====================================================

    function remover_Favorito(card) {
        const titulo = obter_Titulo(card);
        const favoritos = obter_Favoritos();

        const existe = favoritos.some(
            (item) => Texto(item) === Texto(titulo)
        );

        if (!existe) {
            alert(`"${titulo}" não está nos seus favoritos.`);
            return;
        }

        const atualizados = favoritos.filter(
            (item) => Texto(item) !== Texto(titulo)
        );

        if (salvarStorage(STORAGE_KEY, atualizados)) {
            alert(`"${titulo}" foi removido dos favoritos. ❤️`);
        }
    }


    // =====================================================
    // REMOVER DO CATÁLOGO
    // =====================================================

    function removerDoCatalogo(card) {
        const titulo = obter_Titulo(card);

        if (!confirm(`Deseja remover "${titulo}" do catálogo?`)) {
            return;
        }

        const removidos = obter_Removidos();

        const jaExiste = removidos.some(
            (item) => Texto(item) === Texto(titulo)
        );

        if (!jaExiste) {
            removidos.push(titulo);
        }

        if (salvarStorage(REMOVIDOS_KEY, removidos)) {
            atualizar_Cards();
            alert(`"${titulo}" foi removido do catálogo.`);
        }
    }


    // =====================================================
    // ACESSAR OBRA
    // =====================================================

    function acessar_Obra(card, botao) {
        const arquivo = card.dataset.arquivo || '';

        if (arquivo) {
            window.location.href = arquivo;
            return;
        }

        abrir_Saiba_Mais(card, botao);
    }


    // =====================================================
    // EVENTOS DOS BOTÕES DOS CARDS
    // =====================================================

    cards.forEach((card) => {

        const botao_Adicionar = card.querySelector(
            '[class*="adicionar-catalogo"], ' +
            '[class*="adicionar-favorito"]'
        );

        const botao_Remover = card.querySelector(
            '[class*="remover-favorito"], ' +
            '[class*="remover-catalogo"]:not([class*="remover-do-catalogo"])'
        );

        const botao_Acessar = card.querySelector(
            '[class*="ler-catalogo"], ' +
            '[class*="assistir-catalogo"]'
        );

        const botaoRemoverCatalogo = card.querySelector(
            '[class*="remover-do-catalogo"]'
        );

        botao_Adicionar?.addEventListener('click', (event) => {
            event.preventDefault();
            adicionar_Favorito(card);
        });

        botao_Remover?.addEventListener('click', (event) => {
            event.preventDefault();
            remover_Favorito(card);
        });

        botao_Acessar?.addEventListener('click', (event) => {
            event.preventDefault();
            acessar_Obra(card, event.currentTarget);
        });

        botaoRemoverCatalogo?.addEventListener('click', (event) => {
            event.preventDefault();
            removerDoCatalogo(card);
        });

    });


    // =====================================================
    // INICIAR CATÁLOGO
    // =====================================================

    atualizar_Cards();

});
