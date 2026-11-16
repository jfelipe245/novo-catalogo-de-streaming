
"use strict";

document.addEventListener("DOMContentLoaded", () => {

    // LOGIN
    const loginForm = document.getElementById("login-form");
    const emailInput = document.getElementById("email-login");

    const passwordInput =
        document.getElementById("senha-login") ||
        document.getElementById("password-login") ||
        document.getElementById("senha");

    const togglePasswordBtn =
        document.getElementById("toggle-password");

    const btnEntrar = document.getElementById("btn-entrar");

    // Mostrar ou ocultar senha
    if (togglePasswordBtn && passwordInput) {
        togglePasswordBtn.addEventListener("click", () => {
            const mostrar = passwordInput.type === "password";

            passwordInput.type = mostrar ? "text" : "password";
            togglePasswordBtn.textContent = mostrar ? "Ocultar" : "Mostrar";

            togglePasswordBtn.setAttribute(
                "aria-label",
                mostrar ? "Ocultar senha" : "Mostrar senha"
            );
        });
    }

    // Envio do login
    if (loginForm) {
        loginForm.addEventListener("submit", event => {
            const email = emailInput?.value.trim() || "";
            const senha = passwordInput?.value || "";

            if (!email || !senha.trim()) {
                event.preventDefault();
                alert("Preencha o e-mail e a senha para entrar.");
                return;
            }

            if (btnEntrar) {
                btnEntrar.disabled = true;
                btnEntrar.textContent = "Entrando...";
            }
        });
    }

    // CADASTRO
    const cadastroForm = document.getElementById("cadastro-form");

    if (cadastroForm) {
        cadastroForm.addEventListener("submit", event => {
            const nome = document.getElementById("nome");
            const nomeUsuario = document.getElementById("nome_usuario");
            const senha = document.getElementById("senha");
            const confirmarSenha =
                document.getElementById("confirmar-senha");

            if (!nome?.value.trim() || !nomeUsuario?.value.trim()) {
                event.preventDefault();
                alert("Preencha seu nome e nome de usuário.");
                return;
            }

            if (!senha || senha.value.length < 8) {
                event.preventDefault();
                alert("A senha deve ter pelo menos 8 caracteres.");
                senha?.focus();
                return;
            }

            if (confirmarSenha && senha.value !== confirmarSenha.value) {
                event.preventDefault();
                alert("As senhas não são iguais.");
                confirmarSenha.focus();
            }
        });
    }

});
