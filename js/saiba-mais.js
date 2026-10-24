document.addEventListener('DOMContentLoaded', () => {
    const STORAGE_KEY = 'meu_catalogo_educacional';

    const btn_acessar = document.getElementById('btn-acessar');
    const btn_favoritos = document.getElementById('btn-favoritos');
    const tituloElemento = document.getElementById('detalhe-titulo');
    const autorElemento = document.getElementById('detalhe-autor');

    const parametros = new URLSearchParams(window.location.search);
    const tituloParametro = parametros.get('titulo');
    const autorParametro = parametros.get('autor');

    if (tituloElemento && tituloParametro) {
        tituloElemento.textContent = tituloParametro;
    }

    if (autorElemento && autorParametro) {
        autorElemento.textContent = autorParametro;
    }

    const titulo_obra = tituloElemento
        ? tituloElemento.textContent.trim() || 'Obra AfroEdu'
        : 'Obra AfroEdu';

    function obter_favoritos() {
        try {
            const dados = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
            return Array.isArray(dados) ? dados : [];
        } catch (erro) {
            console.error('Erro ao ler favoritos:', erro);
            return [];
        }
    }

    function salvar_favoritos(favoritos) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(favoritos));
            return true;
        } catch (erro) {
            console.error('Erro ao salvar favoritos:', erro);
            return false;
        }
    }

    if (btn_acessar) {
        btn_acessar.addEventListener('click', event => {
            event.preventDefault();
            alert(`Você clicou no botão de acessar a obra "${titulo_obra}".`);
        });
    }

    function atualiza_estado_botao() {
        if (!btn_favoritos) return;

        const salvos = obter_favoritos();
        const ja_favorito = salvos.includes(titulo_obra);

        btn_favoritos.textContent = ja_favorito
            ? 'Remover do catálogo'
            : 'Adicionar ao catálogo';
        btn_favoritos.style.backgroundColor = ja_favorito ? '#dc2626' : '#ca8a04';
    }

    if (btn_favoritos) {
        btn_favoritos.addEventListener('click', event => {
            event.preventDefault();

            let salvos = obter_favoritos();
            const ja_favorito = salvos.includes(titulo_obra);

            if (ja_favorito) {
                salvos = salvos.filter(item => item !== titulo_obra);
            } else {
                salvos.push(titulo_obra);
            }

            if (!salvar_favoritos(salvos)) {
                alert('Não foi possível atualizar os favoritos neste navegador.');
                return;
            }

            alert(ja_favorito
                ? `"${titulo_obra}" foi removido com sucesso da sua lista de favoritos.`
                : `"${titulo_obra}" foi adicionado com sucesso aos seus favoritos.`
            );

            atualiza_estado_botao();
        });
    }

    atualiza_estado_botao();
});
