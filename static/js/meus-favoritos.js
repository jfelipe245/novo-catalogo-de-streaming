
document.addEventListener('DOMContentLoaded', () => {
    const formularios = document.querySelectorAll(
        '#container-favoritos form'
    );

    formularios.forEach(formulario => {
        formulario.addEventListener('submit', (evento) => {
            const confirmar = window.confirm(
                'Deseja remover esta obra dos seus favoritos? ' +
                'Ela continuará disponível no catálogo.'
            );

            if (!confirmar) {
                evento.preventDefault();
            }
        });
    });
});
