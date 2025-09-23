let audio = new Audio(AUDIO_BELL);
let audioActivado = true;
let ordenTimestamps = {};
let estadoFiltro = "todas";

document.getElementById("toggleAudioBtn").addEventListener("click", () => {
    audioActivado = !audioActivado;
    const btn = document.getElementById("toggleAudioBtn");
    btn.textContent = audioActivado ? "🔔 Sonido Activado" : "🔕 Sonido Bloqueado";
    btn.classList.toggle("btn-success", audioActivado);
    btn.classList.toggle("btn-danger", !audioActivado);
});

document.querySelectorAll(".filtro-estado").forEach(btn => {
    btn.addEventListener("click", () => {
        estadoFiltro = btn.dataset.estado;
        actualizarOrdenes();
    });
});

function actualizarOrdenes() {
    fetch(URL_ORDENES_JSON + "?estado=" + estadoFiltro)
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector("#ordenes tbody");
            tbody.innerHTML = "";
            let nuevasOrdenes = [];
            const primeraCarga = Object.keys(ordenTimestamps).length === 0;

            data.ordenes.forEach(orden => {
                if (!ordenTimestamps[orden.id]) {
                    ordenTimestamps[orden.id] = true;
                    if (!primeraCarga) nuevasOrdenes.push(orden.id);
                }

                let itemsHTML = "<ul>";
                orden.items.forEach(item => {
                    itemsHTML += `<li>${item.nombre} x${item.cantidad} ($${item.subtotal})</li>`;
                });
                itemsHTML += "</ul>";

                const fila = document.createElement("tr");
                fila.innerHTML = `
                    <td>${orden.id}</td>
                    <td>$${orden.total}</td>
                    <td>${itemsHTML}</td>
                    <td>${orden.tiempo_legible}</td>
                    <td class="text-center text">
                        <strong id="estado-${orden.id}">${(orden.estado_cocina || "endiente").toUpperCase()}</strong><p></p>
                        <button class="btn btn-success avanzar-estado" data-id="${orden.id}">Avanzar</button>
                    </td>
                `;
                tbody.appendChild(fila);
            });

            const totalRecibidoElem = document.querySelector("#ordenes p.fw-bold");
            if (totalRecibidoElem) totalRecibidoElem.textContent = `Total recibido: $${data.total_recibido}`;

            if (nuevasOrdenes.length > 0 && audioActivado) audio.play().catch(e => console.log(e));
        })
        .catch(err => console.error(err));
}

document.addEventListener("click", function(e) {
    if (e.target.classList.contains("avanzar-estado")) {
        const id = e.target.dataset.id;
        const estadoElem = document.getElementById(`estado-${id}`);
        let nuevoEstado = { pendiente: "preparacion", preparacion: "lista", lista: "lista" }[estadoElem.textContent.trim()] || "pendiente";

        fetch(`/actualizar_estado_cocina/${id}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": CSRF_TOKEN
            },
            body: JSON.stringify({ estado: nuevoEstado })
        })
        .then(res => res.json())
        .then(data => { if (data.ok) estadoElem.textContent = data.estado; })
        .catch(err => console.error(err));
    }
});

setInterval(actualizarOrdenes, 1000);
actualizarOrdenes();
