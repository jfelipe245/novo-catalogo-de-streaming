
document.addEventListener('DOMContentLoaded', () => {

    // ========================================
    // ELEMENTOS DO LOGIN
    // ========================================

    const loginForm = document.getElementById('login-form');
    const emailInput = document.getElementById('email-login');

    const passwordInput =
        document.getElementById('senha-login') ||
        document.getElementById('password-login') ||
        document.getElementById('senha');

    const togglePasswordBtn = document.getElementById('toggle-password');
    const btnEntrar = document.getElementById('btn-entrar');

    // ========================================
    // MOSTRAR OU OCULTAR SENHA
    // ========================================

    if (togglePasswordBtn && passwordInput) {

        togglePasswordBtn.addEventListener('click', () => {

            const mostrar = passwordInput.type === 'password';

            passwordInput.type = mostrar ? 'text' : 'password';

            togglePasswordBtn.textContent = mostrar ? 'Ocultar' : 'Mostrar';

            togglePasswordBtn.setAttribute(
                'aria-label',
                mostrar ? 'Ocultar senha' : 'Mostrar senha'
            );

            togglePasswordBtn.setAttribute(
                'aria-pressed',
                mostrar ? 'true' : 'false'
            );

        });

    }

    // ========================================
    // LOGIN COM FLASK
    // ========================================

    if (loginForm) {

        loginForm.addEventListener('submit', event => {

            const email = emailInput ? emailInput.value.trim() : '';
            const senha = passwordInput ? passwordInput.value : '';

            if (!email || !senha.trim()) {
                event.preventDefault();

                alert('Preencha o e-mail e a senha para entrar.');
                return;
            }

            // Não usamos preventDefault quando os campos estão corretos.
            // Assim, o formulário é enviado para a rota Flask.

            if (btnEntrar) {
                btnEntrar.textContent = 'Entrando...';
                btnEntrar.disabled = true;
            }

        });

    }

    // ========================================
    // CADASTRO
    // ========================================

    const cadastroForm = document.getElementById('cadastro-form');

    if (cadastroForm) {

        cadastroForm.addEventListener('submit', event => {

            const senhaCadastro =
                document.getElementById('senha');

            const confirmarSenha =
                document.getElementById('confirmar-senha');

            if (senhaCadastro && confirmarSenha) {

                if (senhaCadastro.value !== confirmarSenha.value) {
                    event.preventDefault();

                    alert('As senhas não são iguais.');
                    confirmarSenha.focus();
                    return;
                }

                if (senhaCadastro.value.length < 8) {
                    event.preventDefault();

                    alert('A senha deve ter pelo menos 8 caracteres.');
                    senhaCadastro.focus();
                }

            }

        });

    }

});
