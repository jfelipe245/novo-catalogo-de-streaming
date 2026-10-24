
document.addEventListener('DOMContentLoaded', () => {

    // ========================================
    // ANO AUTOMÁTICO NO RODAPÉ
    // ========================================

    const rodape = document.querySelector('footer p');

    if (rodape) {
        const ano = new Date().getFullYear();

        rodape.innerHTML =
            '&copy; ' + ano +
            ' Catálogo Educacional NEABI - ' +
            'Promoção da Igualdade Racial e Diversidade nas Escolas.';
    }

    // ========================================
    // CONFIRMAÇÃO AO SAIR DA CONTA
    // ========================================

    const linkSair = document.querySelector(
        '.nav-list a[href*="logout"]'
    );

    if (linkSair) {
        linkSair.addEventListener('click', (event) => {

            const confirmar = window.confirm(
                'Deseja realmente sair da sua conta?'
            );

            if (!confirmar) {
                event.preventDefault();
            }

        });
    }

});
