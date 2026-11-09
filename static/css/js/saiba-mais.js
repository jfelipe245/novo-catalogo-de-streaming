 // --- INÍCIO: integração do botão Saiba Mais ---
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.card .btn-info').forEach(link => {
        const card = link.closest('.card');
        if (!card) return;

        link.addEventListener('click', event => {
            event.preventDefault();

            const texto = seletor =>
                card.querySelector(seletor)?.textContent.trim() || '';

            const imagem = card.querySelector('img');

            const dados = new URLSearchParams({
                titulo: texto('.titulo') || imagem?.alt || 'Obra do catálogo',
                autor: texto('.autor'),
                categoria: card.dataset.category || texto('.genero-badge') || 'Obra',
                genero: card.dataset.genero || '',
                sinopse: texto('.descricao'),
                detalhes: texto('.detalhes'),
                capa: imagem ? imagem.src : ''
            });

            window.location.href =
                `${link.href}?${dados.toString()}`;
        });
    });
});
// --- FIM: integração do botão Saiba Mais ---
