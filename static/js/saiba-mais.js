
"use strict";

document.addEventListener("DOMContentLoaded", () => {

    const btnAcessar = document.getElementById("btn-acessar");
    const btnFavoritos = document.getElementById("btn-favoritos");
    const pagina = document.querySelector(".detalhes-pagina");

    if (!pagina) return;

    const obraId = pagina.dataset.obraId;
    const titulo =
        document.getElementById("detalhe-titulo")?.textContent.trim()
        || "Obra";

    /* =====================================
       FAVORITOS
    ===================================== */

    if (btnFavoritos) {

        btnFavoritos.addEventListener("click", () => {

            if (!obraId) {
                alert("Não foi possível identificar esta obra.");
                return;
            }

            const confirmar = confirm(
                `Adicionar "${titulo}" aos seus favoritos?`
            );

            if (!confirmar) return;

            const formulario = document.createElement("form");

            formulario.method = "POST";
            formulario.action = window.url_Adicionar_Favoritos;
            formulario.hidden = true;

            const campo = document.createElement("input");

            campo.type = "hidden";
            campo.name = "obra_id";
            campo.value = obraId;

            formulario.appendChild(campo);
            document.body.appendChild(formulario);

            formulario.submit();

        });

    }

    /* =====================================
       ACESSAR OBRA
    ===================================== */

    if (btnAcessar) {

        btnAcessar.addEventListener("click", () => {

            alert(
                `O acesso à obra "${titulo}" precisa ter um link cadastrado.`
            );

        });

    }

});
