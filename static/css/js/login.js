document.addEventListener('DOMContentLoaded', () => {

    const loginForm = document.getElementById('login-form');
    const passwordInput = document.getElementById('password-login');
    const togglePasswordBtn = document.getElementById('toggle-password');
    const btnGerarTeste = document.getElementById('btn-teste-login');

    // MOSTRAR / OCULTAR SENHA
    if (togglePasswordBtn && passwordInput) {

        togglePasswordBtn.addEventListener('click', event => {

            event.preventDefault();

            const mostrar = passwordInput.type === 'password';

            passwordInput.type = mostrar ? 'text' : 'password';

            togglePasswordBtn.textContent = mostrar ? '🙈' : '👁️';

        });

    }


    // GERAR DADOS DE TESTE
    if (btnGerarTeste) {

        btnGerarTeste.addEventListener('click', event => {

            event.preventDefault();

            const nomeInput = document.getElementById('login-nome');
            const idadeInput = document.getElementById('login-idade');
            const dataInput = document.getElementById('data-login');
            const emailInput = document.getElementById('email-login');
            const telefoneInput = document.getElementById('telefone-login');
            const bairroInput = document.getElementById('bairro-login');
            const ruaInput = document.getElementById('rua-login');
            const enderecoInput = document.getElementById('endereco-login');

            if (nomeInput) {
                nomeInput.value = 'Joao Felipe';
            }

            if (idadeInput) {
                idadeInput.value = '17';
            }

            if (dataInput) {
                dataInput.value = '2009-01-15';
            }

            if (emailInput) {
                emailInput.value = 'teste@afroedu.com';
            }

            if (telefoneInput) {
                telefoneInput.value = '74999999999';
            }

            if (bairroInput) {
                bairroInput.value = 'Centro';
            }

            if (ruaInput) {
                ruaInput.value = 'Rua Principal';
            }

            if (enderecoInput) {
                enderecoInput.value = '100';
            }

            if (passwordInput) {
                passwordInput.value = '123456';
            }

        });

    }

});