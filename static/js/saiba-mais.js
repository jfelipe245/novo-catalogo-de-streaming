
document.addEventListener('DOMContentLoaded', () => {

    const STORAGE_KEY = 'meu_catalogo_educacional';

    const btn_acessar = document.getElementById('btn-acessar');
    const btn_favoritos = document.getElementById('btn-favoritos');

    const parametros = new URLSearchParams(window.location.search);

    const dados = {
        titulo: parametros.get('titulo') || 'Obra AfroEdu',
        autor: parametros.get('autor') || 'Autor não informado',
        categoria: parametros.get('categoria') || 'Não informada',
        genero: parametros.get('genero') || 'Não informado',
        ano_publicacao: parametros.get('ano_publicacao'),
        ano_lancamento: parametros.get('ano_lancamento'),
        editora: parametros.get('editora'),
        paginas: parametros.get('paginas'),
        diretor: parametros.get('diretor'),
        artista: parametros.get('artista'),
        nacionalidade: parametros.get('nacionalidade'),
        edicao: parametros.get('edicao'),
        tematica: parametros.get('tematica')
    };

    // Identificação da obra

    document.getElementById('detalhe-titulo').textContent = dados.titulo;

    document.getElementById('detalhe-autor').textContent = dados.autor;

    document.getElementById('ficha-categoria').textContent = dados.categoria;

    document.getElementById('ficha-genero').textContent = dados.genero;

    // Preenchimento dos campos adicionais

    function preencher_campo(id, valor) {
        const campo = document.getElementById(id);

        if (campo && valor && valor !== '0') {
            campo.querySelector('dd').textContent = valor;
            campo.hidden = false;
        }
    }

    const ano = dados.categoria.toLowerCase() === 'livro'
        ? dados.ano_publicacao
        : dados.ano_lancamento;

    preencher_campo('campo-ano', ano);
    preencher_campo('campo-editora', dados.editora);
    preencher_campo('campo-paginas', dados.paginas);
    preencher_campo('campo-diretor', dados.diretor);
    preencher_campo('campo-artista', dados.artista);
    preencher_campo('campo-nacionalidade', dados.nacionalidade);
    preencher_campo('campo-edicao', dados.edicao);
    preencher_campo('campo-tematica', dados.tematica);

    // Temas abordados

    const temas = document.getElementById('temas-abordados');

    if (temas && dados.genero !== 'Não informado') {
        temas.textContent = '';

        const etiqueta = document.createElement('span');
        etiqueta.textContent = dados.genero;

        temas.appendChild(etiqueta);
    }

    // Favoritos

    function obter_favoritos() {
        try {
            const salvos = JSON.parse(
                localStorage.getItem(STORAGE_KEY) || '[]'
            );

            return Array.isArray(salvos) ? salvos : [];

        } catch (erro) {
            console.error('Erro ao ler favoritos:', erro);
            return [];
        }
    }

    function salvar_favoritos(favoritos) {
        try {
            localStorage.setItem(
                STORAGE_KEY,
                JSON.stringify(favoritos)
            );

            return true;

        } catch (erro) {
            console.error('Erro ao salvar favoritos:', erro);
            return false;
        }
    }

    function atualiza_estado_botao() {

        if (!btn_favoritos) return;

        const salvos = obter_favoritos();
        const ja_favorito = salvos.includes(dados.titulo);

        btn_favoritos.textContent = ja_favorito
            ? 'Remover dos favoritos'
            : 'Adicionar aos favoritos';

        btn_favoritos.style.backgroundColor =
            ja_favorito ? '#dc2626' : '#ca8a04';
    }

    if (btn_favoritos) {

        btn_favoritos.addEventListener('click', event => {

            event.preventDefault();

            let salvos = obter_favoritos();

            const ja_favorito = salvos.includes(dados.titulo);

            if (ja_favorito) {

                salvos = salvos.filter(
                    item => item !== dados.titulo
                );

            } else {

                salvos.push(dados.titulo);

            }

            if (!salvar_favoritos(salvos)) {

                alert('Não foi possível atualizar os favoritos neste navegador.');
                return;

            }

            alert(
                ja_favorito
                    ? `"${dados.titulo}" foi removido dos favoritos.`
                    : `"${dados.titulo}" foi adicionado aos favoritos.`
            );

            atualiza_estado_botao();

        });

    }

    // Botão de acesso

    if (btn_acessar) {

        btn_acessar.addEventListener('click', event => {

            event.preventDefault();

            alert(
                `O acesso à obra "${dados.titulo}" precisa ter um link cadastrado.`
            );

        });

    }

    atualiza_estado_botao();

});
