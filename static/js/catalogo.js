
"use strict";

/* =========================================
   AFROEDU STREAM
   JAVASCRIPT PRINCIPAL
========================================= */

document.addEventListener("DOMContentLoaded", () => {
    inicializarFiltros();
    inicializarBotoesDeDetalhes();
    inicializarRemoverDoCatalogo();
    inicializarBotoesDeFavoritos();
    inicializarEstadoDosFavoritos();
    inicializarMenuCategorias();
});

/* =========================================
   1. ELEMENTOS E FUNÇÕES AUXILIARES
========================================= */

const selecionar = (seletor, contexto = document) =>
    contexto.querySelector(seletor);

const selecionarTodos = (seletor, contexto = document) =>
    Array.from(contexto.querySelectorAll(seletor));

function normalizarTexto(texto) {
    return String(texto || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLocaleLowerCase("pt-BR")
        .trim();
}

function obterCategoria(card) {
    return (
        card.dataset.category ||
        card.dataset.categoria ||
        ""
    ).trim();
}

function obterGenero(card) {
    return card.dataset.genero || "";
}

function obterTitulo(card) {
    return (
        card.dataset.titulo ||
        selecionar(".titulo", card)?.textContent.trim() ||
        ""
    );
}

function obterResponsavel(card) {
    const responsavel =
        card.dataset.autor ||
        card.dataset.diretor ||
        card.dataset.artista ||
        selecionar(".autor", card)?.textContent ||
        "";

    return responsavel
        .replace(/^(autor|diretor|artista)\s*:\s*/i, "")
        .trim();
}

/* =========================================
   2. PESQUISA E FILTROS
========================================= */

function inicializarFiltros() {
    const container = selecionar("#card-container");
    const filtroCategoria = selecionar("#filtro-categoria");
    const campoPesquisa = selecionar("#pesquisa");
    const botaoPesquisa = selecionar("#botao-pesquisa");

    if (!container || !filtroCategoria) {
        console.warn("AFROEDU: elementos do catálogo não encontrados.");
        return;
    }

    const cards = selecionarTodos(".card", container);

    function categoriaNormalizada(card) {
        const categoria = normalizarTexto(obterCategoria(card));

        const equivalencias = {
            livros: "livro",
            filmes: "filme",
            series: "serie",
            documentarios: "documentario",
            musicas: "musica",
            "musica de protesto": "musica",
            curtas: "curta",
            "curta metragem": "curta",
            "curta-metragem": "curta",
            "curtas-metragens": "curta"
        };

        return equivalencias[categoria] || categoria;
    }

    function aplicarFiltros() {
        const categoriaSelecionada =
            normalizarTexto(filtroCategoria.value);

        const termo =
            normalizarTexto(campoPesquisa?.value || "");

        let quantidade = 0;

        cards.forEach((card) => {
            const categoria = categoriaNormalizada(card);
            const titulo = normalizarTexto(obterTitulo(card));
            const responsavel = normalizarTexto(obterResponsavel(card));

            const correspondeCategoria =
                !categoriaSelecionada ||
                categoria === categoriaSelecionada;

            // Pesquisa somente título e responsável.
            const correspondePesquisa =
                !termo ||
                titulo.includes(termo) ||
                responsavel.includes(termo);

            const mostrar =
                correspondeCategoria && correspondePesquisa;

            card.hidden = !mostrar;

            if (mostrar) quantidade++;
        });

        let mensagem = selecionar("#mensagem-pesquisa");

        if (!mensagem) {
            mensagem = document.createElement("p");
            mensagem.id = "mensagem-pesquisa";
            mensagem.setAttribute("role", "status");
            mensagem.setAttribute("aria-live", "polite");

            container.insertAdjacentElement("beforebegin", mensagem);
        }

        const existemFiltros =
            Boolean(categoriaSelecionada) || Boolean(termo);

        mensagem.textContent = existemFiltros
            ? `${quantidade} obra(s) encontrada(s).`
            : "";
    }

    filtroCategoria.addEventListener("change", aplicarFiltros);
    campoPesquisa?.addEventListener("input", aplicarFiltros);
    botaoPesquisa?.addEventListener("click", aplicarFiltros);

    aplicarFiltros();
}

/* =========================================
   3. LER, ASSISTIR E OUVIR
========================================= */

function inicializarBotoesDeDetalhes() {
    document.addEventListener("click", (evento) => {
        const botao = evento.target.closest(
            ".ler-catalogo-Livro, " +
            ".assistir-catalogo-Filme, " +
            ".assistir-catalogo-Serie, " +
            ".assistir-catalogo-documentario, " +
            ".assistir-catalogo-Documentario, " +
            ".assistir-catalogo-curta, " +
            ".assistir-catalogo-Curta, " +
            ".assistir-catalogo-musica, " +
            ".assistir-catalogo-Musica, " +
            ".ouvir-catalogo-musica, " +
            ".ouvir-catalogo-Musica"
        );

        if (!botao) return;

        const card = botao.closest(".card");

        if (!card) {
            alert("Não foi possível localizar esta obra.");
            return;
        }

        evento.preventDefault();
        abrirDetalhesDaObra(card);
    });
}

function abrirDetalhesDaObra(card) {
    const destino = window.url_Obra;

    if (!destino) {
        alert("A página de detalhes não foi configurada.");
        return;
    }

    const obraId = card.dataset.id;
    const categoria = normalizarTexto(obterCategoria(card));

    if (!obraId || !categoria) {
        alert("Não foi possível identificar o ID ou a categoria da obra.");
        return;
    }

    const categoriasValidas = [
        "livro",
        "filme",
        "serie",
        "documentario",
        "curta",
        "musica"
    ];

    if (!categoriasValidas.includes(categoria)) {
        alert("A categoria desta obra não é reconhecida.");
        return;
    }

    const url = new URL(destino, window.location.origin);

    // O Flask consulta os dados diretamente no banco.
    url.searchParams.set("obra_id", obraId);
    url.searchParams.set("categoria", categoria);

    window.location.href = url.toString();
}

/* =========================================
   4. REMOVER OBRA DO CATÁLOGO
   REMOÇÃO TEMPORÁRIA COM CONFIRMAÇÃO
========================================= */
/* =========================================
   4. REMOVER OBRA DO CATÁLOGO
   APENAS ESCONDE O CARD
========================================= */

function inicializarRemoverDoCatalogo() {
    document.addEventListener("submit", function (evento) {
        const formulario = evento.target;

        // Verifica se é o formulário de remoção do catálogo
        if (!formulario.matches('form[action*="/remover"]')) {
            return;
        }

        evento.preventDefault();

        const card = formulario.closest(".card");

        if (!card) {
            return;
        }

        const titulo = obterTitulo(card);

        const confirmar = confirm(
            `Deseja esconder "${titulo}" do catálogo?`
        );

        if (!confirmar) {
            return;
        }

        // Esconde somente o card na página atual
        card.hidden = true;
    });
}

/* =========================================
   5. FORMULÁRIOS AUXILIARES
========================================= */

function criarFormulario(url, campos) {
    if (!url) {
        alert("A rota necessária não foi configurada.");
        return;
    }

    const formulario = document.createElement("form");

    formulario.method = "POST";
    formulario.action = url;
    formulario.hidden = true;

    Object.entries(campos).forEach(([nome, valor]) => {
        const input = document.createElement("input");

        input.type = "hidden";
        input.name = nome;
        input.value = String(valor ?? "");

        formulario.appendChild(input);
    });

    document.body.appendChild(formulario);
    formulario.submit();
}

/* =========================================
   6. FAVORITOS
========================================= */

function inicializarBotoesDeFavoritos() {
    document.addEventListener("click", (evento) => {
        const botao = evento.target.closest(
            ".adicionar-catalogo-Livro, " +
            ".adicionar-catalogo-Filme, " +
            ".adicionar-catalogo-Serie, " +
            ".adicionar-catalogo-Documentario, " +
            ".adicionar-catalogo-documentario, " +
            ".adicionar-catalogo-Curta, " +
            ".adicionar-catalogo-curta, " +
            ".adicionar-catalogo-Musica, " +
            ".adicionar-catalogo-musica"
        );

        if (!botao || botao.disabled) return;

        evento.preventDefault();
        adicionarFavorito(botao);
    });
}


function adicionarFavorito(botao) {
    const url = window.url_Adicionar_Favoritos;
    const card = botao.closest(".card");

    if (!url || !card) {
        alert("Não foi possível preparar o favorito.");
        return;
    }

    const titulo = obterTitulo(card);
    const categoria = obterCategoria(card);
    const genero = obterGenero(card);

    if (!titulo || !categoria) {
        alert("Não foi possível identificar o título ou a categoria.");
        return;
    }

    if (!confirm(`Adicionar "${titulo}" aos favoritos?`)) {
        return;
    }

    criarFormulario(url, {
        titulo: titulo,
        categoria: categoria,
        genero: genero,
        origem: "catalogo"
    });
}

/* =========================================
   7. IDENTIFICAR FAVORITOS EXISTENTES
========================================= */

function inicializarEstadoDosFavoritos() {
    const favoritos = selecionarTodos("[data-favorito-id]");

    if (!favoritos.length) return;

    const mapa = new Set(
        favoritos.map((item) =>
            `${normalizarTexto(item.dataset.favoritoTitulo)}::` +
            `${normalizarTexto(item.dataset.favoritoCategoria)}`
        )
    );

    selecionarTodos("#card-container .card").forEach((card) => {
        const chave =
            `${normalizarTexto(obterTitulo(card))}::` +
            `${normalizarTexto(obterCategoria(card))}`;

        const adicionar = selecionar(
            "[class*='adicionar-catalogo-']",
            card
        );

        if (!adicionar) return;

        const jaFavoritado = mapa.has(chave);

        adicionar.textContent = jaFavoritado
            ? "✓ Já está nos favoritos"
            : "+ Adicionar esta obra";

        adicionar.disabled = jaFavoritado;
    });
}

/* =========================================
   8. MENU DE CATEGORIAS
========================================= */

function inicializarMenuCategorias() {
    const botao = selecionar("#botao-menu-categorias");
    const lista = selecionar("#lista-categorias-catalogo");
    const nome = selecionar("#nome-categoria-selecionada");
    const filtro = selecionar("#filtro-categoria");

    if (!botao || !lista || !nome || !filtro) {
        return;
    }

    const nomes = {
        "": "Todos",
        livro: "Livros",
        filme: "Filmes",
        serie: "Séries",
        documentario: "Documentários",
        musica: "Músicas de protesto",
        curta: "Curtas-metragens"
    };

    function atualizarNome() {
        nome.textContent = nomes[filtro.value] || "Todos";
    }

    function fecharMenu() {
        botao.setAttribute("aria-expanded", "false");
        lista.hidden = true;
    }

    atualizarNome();

    filtro.addEventListener("change", atualizarNome);

    botao.addEventListener("click", () => {
        const aberto =
            botao.getAttribute("aria-expanded") === "true";

        botao.setAttribute("aria-expanded", String(!aberto));
        lista.hidden = aberto;
    });

    lista.querySelectorAll("[data-categoria-menu]").forEach((opcao) => {
        opcao.addEventListener("click", () => {
            filtro.value = opcao.dataset.categoriaMenu;

            atualizarNome();
            fecharMenu();

            filtro.dispatchEvent(
                new Event("change", { bubbles: true })
            );
        });
    });

    document.addEventListener("click", (evento) => {
        if (
            !botao.contains(evento.target) &&
            !lista.contains(evento.target)
        ) {
            fecharMenu();
        }
    });

    document.addEventListener("keydown", (evento) => {
        if (evento.key === "Escape") {
            fecharMenu();
        }
    });
}
