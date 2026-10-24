document.addEventListener('DOMContentLoaded', () => {
    const STORAGE_KEY = 'meu_catalogo_educacional';
    const containerFavoritos = document.getElementById('container-favoritos');

    function obterFavoritos() {
        try {
            const dados = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
            return Array.isArray(dados) ? dados : [];
        } catch (erro) {
            console.error('Erro ao ler favoritos:', erro);
            return [];
        }
    }

    function salvarFavoritos(favoritos) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(favoritos));
            return true;
        } catch (erro) {
            console.error('Erro ao salvar favoritos:', erro);
            return false;
        }
    }

    function renderizarFavoritos() {
        if (!containerFavoritos) return;

        const salvos = obterFavoritos();
        containerFavoritos.innerHTML = '';

        if (salvos.length === 0) {
            containerFavoritos.innerHTML = `
                <div class="sem-favoritos">
                    <p>Você ainda não adicionou nenhum livro, filme ou série aos seus favoritos.</p>
                </div>
            `;
            return;
        }

        salvos.forEach(titulo => {
            const card = document.createElement('article');
            card.classList.add('card');

            const badge = document.createElement('span');
            badge.className = 'badge';
            badge.textContent = 'Favorito';

            const tituloElemento = document.createElement('h2');
            tituloElemento.className = 'titulo-fav';
            tituloElemento.textContent = String(titulo);

            const btnRemover = document.createElement('button');
            btnRemover.type = 'button';
            btnRemover.className = 'btn-remover-fav';
            btnRemover.textContent = 'Remover dos Favoritos';
            btnRemover.addEventListener('click', () => removerFavorito(titulo));

            card.append(badge, tituloElemento, btnRemover);
            containerFavoritos.appendChild(card);
        });
    }

    function removerFavorito(titulo) {
        const salvos = obterFavoritos().filter(item => item !== titulo);

        if (!salvarFavoritos(salvos)) {
            alert('Não foi possível atualizar os favoritos neste navegador.');
            return;
        }

        renderizarFavoritos();
    }

    renderizarFavoritos();
});
