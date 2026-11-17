
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
    criarBotoesDeFavoritosNosCards();
    inicializarEstadoDosFavoritos();
    inicializarMenuCategorias();
    inicializarCamposAdicionar();
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

    function normalizarCategoria(categoria) {
        const valor = normalizarTexto(categoria);

        const equivalencias = {
            livros: "livro",
            livro: "livro",
            filmes: "filme",
            filme: "filme",
            series: "serie",
            serie: "serie",
            documentarios: "documentario",
            documentario: "documentario",
            musicas: "musica",
            musica: "musica",
            "musica de protesto": "musica",
            curtas: "curta",
            curta: "curta",
            "curta metragem": "curta",
            "curtas metragens": "curta"
        };

        return equivalencias[valor] || valor;
    }

    function aplicarFiltros() {
        const categoriaSelecionada = normalizarCategoria(
            filtroCategoria.value
        );

        const termo = normalizarTexto(
            campoPesquisa?.value || ""
        );

        let quantidade = 0;

        cards.forEach((card) => {
            const categoria = normalizarCategoria(
                obterCategoria(card)
            );

            // Pesquisa também diretamente no texto do card.
            const textoCard = normalizarTexto(card.textContent);

            const titulo = normalizarTexto(obterTitulo(card));
            const responsavel = normalizarTexto(obterResponsavel(card));
            const genero = normalizarTexto(obterGenero(card));

            const descricao = normalizarTexto(
                card.dataset.descricao ||
                selecionar(".descricao", card)?.textContent ||
                ""
            );

            const correspondeCategoria =
                !categoriaSelecionada ||
                categoria === categoriaSelecionada;

            const textoCompleto = [
                textoCard,
                titulo,
                responsavel,
                genero,
                descricao
            ].join(" ");

            const correspondePesquisa =
                !termo || textoCompleto.includes(termo);

            const mostrar =
                correspondeCategoria && correspondePesquisa;

            card.hidden = !mostrar;

            if (mostrar) {
                quantidade++;
            }
        });

        selecionarTodos(".secao-categoria", container).forEach((secao) => {
            const possuiObrasVisiveis = selecionarTodos(".card", secao)
                .some((card) => !card.hidden);

            secao.hidden = !possuiObrasVisiveis;
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
    const obraId = card.dataset.id;

    if (!destino) {
        alert("A página de detalhes não foi configurada.");
        return;
    }

    if (!obraId) {
        alert("Não foi possível identificar esta obra.");
        return;
    }

    const url = new URL(destino, window.location.origin);

    url.searchParams.set("obra_id", obraId);

    window.location.href = url.toString();
}

/* =========================================
   4. REMOVER OBRA DO CATÁLOGO
   APENAS ESCONDE O CARD NA PÁGINA
========================================= */

function inicializarRemoverDoCatalogo() {
    document.addEventListener("submit", function (evento) {
        const formulario = evento.target;

        if (
            !(formulario instanceof HTMLFormElement) ||
            !formulario.matches('form[action*="/remover"]')
        ) {
            return;
        }

        const card = formulario.closest(".card");

        if (!card) {
            return;
        }

        evento.preventDefault();

        const titulo = obterTitulo(card);

        const confirmar = window.confirm(
            `Deseja esconder "${titulo}" temporariamente do catálogo?`
        );

        if (!confirmar) {
            return;
        }

        card.hidden = true;

        const mensagem = selecionar("#mensagem-pesquisa");

        if (mensagem) {
            const cardsVisiveis = selecionarTodos(
                "#card-container .card"
            ).filter((item) => !item.hidden).length;

            mensagem.textContent = `${cardsVisiveis} obra(s) encontrada(s).`;
        }
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

/*
   Cria um botão de favorito em cada card.
   O botão envia o ID real da obra ao Flask.
*/

function criarBotoesDeFavoritosNosCards() {
    const cards = selecionarTodos("#card-container .card");

    cards.forEach((card) => {
        const acoes = selecionar(".card-actions", card);

        if (!acoes) return;

        if (selecionar(".adicionar-catalogo-favorito", acoes)) {
            return;
        }

        const botao = document.createElement("button");

        botao.type = "button";
        botao.className =
            "btn-acao btn-favoritos adicionar-catalogo-favorito";

        botao.textContent = "+ Adicionar aos favoritos";

        acoes.appendChild(botao);
    });
}

function inicializarBotoesDeFavoritos() {
    document.addEventListener("click", (evento) => {
        const botao = evento.target.closest(
            ".adicionar-catalogo-favorito, " +
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

    const obraId = card.dataset.id;
    const titulo = obterTitulo(card);

    if (!obraId) {
        alert("Não foi possível identificar o ID desta obra.");
        return;
    }

    if (!confirm(`Adicionar "${titulo}" aos favoritos?`)) {
        return;
    }

    botao.disabled = true;
    botao.textContent = "Salvando...";

    criarFormulario(url, {
        obra_id: obraId,
        origem: "catalogo"
    });
}

/* =========================================
   7. IDENTIFICAR FAVORITOS EXISTENTES
========================================= */

function inicializarEstadoDosFavoritos() {
    const favoritos = selecionarTodos("[data-favorito-obra-id]");

    const idsFavoritos = new Set(
        favoritos
            .map((item) => String(item.dataset.favoritoObraId || ""))
            .filter(Boolean)
    );

    selecionarTodos("#card-container .card").forEach((card) => {
        const obraId = String(card.dataset.id || "");

        const botao = selecionar(
            ".adicionar-catalogo-favorito",
            card
        );

        if (!botao) return;

        const jaFavoritado = idsFavoritos.has(obraId);

        botao.textContent = jaFavoritado
            ? "✓ Já está nos favoritos"
            : "+ Adicionar aos favoritos";

        botao.disabled = jaFavoritado;
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


/* =========================================
   9. FORMULÁRIO ADICIONAR OBRA
   EXIBE OS CAMPOS DA CATEGORIA SELECIONADA
========================================= */

function inicializarCamposAdicionar() {

    const seletor = selecionar("#tipo");
    const campos = selecionarTodos(".grupo-categoria");

    // Se não estiver na página adicionar, encerra.
    if (!seletor || campos.length === 0) {
        return;
    }

    function atualizarCampos() {

        const categoria = normalizarTexto(seletor.value);

        campos.forEach((campo) => {

            const categorias = campo.dataset.tipos
                .split(" ")
                .map(normalizarTexto);

            const mostrar = categorias.includes(categoria);

            campo.hidden = !mostrar;
            campo.style.display = mostrar ? "" : "none";

            selecionarTodos("input, select, textarea", campo)
                .forEach((input) => {
                    input.disabled = !mostrar;
                });

        });
    }

    seletor.addEventListener("change", atualizarCampos);

    // Aplica a categoria recebida pela URL ao abrir a página.
    atualizarCampos();
}
