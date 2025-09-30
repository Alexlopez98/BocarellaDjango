// Función para eliminar etiquetas HTML de un string
function stripHTML(html) {
    const tmp = document.createElement("div");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
}

document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById("items-container");

    fetch("/api/items/")
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                container.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                return;
            }

            const items = data.items;
            if (!items || items.length === 0) {
                container.innerHTML = `<p class="text-center text-muted">No se encontraron productos.</p>`;
                return;
            }

            const row = document.createElement("div");
            row.className = "row";

            items.forEach(item => {
                const col = document.createElement("div");
                col.className = "col-md-4 mb-4";

                const card = document.createElement("div");
                card.className = "card h-100 shadow-sm";

                const img = document.createElement("img");
                img.className = "card-img-top";
                img.alt = item.item_name || "Sin imagen";
                img.src = item.image_url || "/static/img/no-image.png";

                const cardBody = document.createElement("div");
                cardBody.className = "card-body";

                // Título
                const title = document.createElement("h5");
                title.className = "card-title";
                title.textContent = item.item_name;
                cardBody.appendChild(title);

                // Descripción sin etiquetas HTML
                const descText = stripHTML(item.description) || "No hay descripción";
                if (!item.description) {
                    const span = document.createElement("span");
                    span.className = "text-muted fst-italic";
                    span.textContent = descText;
                    cardBody.appendChild(span);
                } else {
                    cardBody.appendChild(document.createTextNode(descText));
                }

                card.appendChild(img);
                card.appendChild(cardBody);
                col.appendChild(card);
                row.appendChild(col);
            });

            container.innerHTML = "";
            container.appendChild(row);
        })
        .catch(err => {
            container.innerHTML = `<div class="alert alert-danger">Error al cargar los productos.</div>`;
            console.error(err);
        });
});
