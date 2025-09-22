document.addEventListener("DOMContentLoaded", () => {

  function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
  }

  // 🔹 Actualizar contador desde Django
  function updateCartCount() {
    fetch("/carrito/contador/")
      .then(res => res.json())
      .then(data => {
        document.querySelectorAll("#cart-count").forEach(el => {
          el.textContent = data.total || 0;
        });
      });
  }

  // 🔹 Crear controles + / -
  function crearControl(id, tipo, cantidad) {
    const container = document.getElementById(`container-${tipo}-${id}`);
    if (!container) return;

    container.innerHTML = `
      <div class="d-flex justify-content-between align-items-center">
        <button class="btn btn-danger btn-sm btn-minus" data-id="${id}" data-tipo="${tipo}">-</button>
        <span class="mx-2 fw-bold quantity" id="qty-${tipo}-${id}">${cantidad}</span>
        <button class="btn btn-success btn-sm btn-plus" data-id="${id}" data-tipo="${tipo}">+</button>
      </div>
    `;

    agregarEventos(id, tipo);
  }

  // 🔹 Eventos + / -
  function agregarEventos(id, tipo) {
    const btnPlus = document.querySelector(`#container-${tipo}-${id} .btn-plus`);
    const btnMinus = document.querySelector(`#container-${tipo}-${id} .btn-minus`);
    const qtySpan = document.getElementById(`qty-${tipo}-${id}`);

    if (btnPlus) {
      btnPlus.addEventListener("click", () => {
        fetch(`/carrito/agregar/${tipo}/${id}/`, {
          method: "POST",
          headers: { 'X-CSRFToken': getCSRFToken() }
        })
        .then(res => res.json())
        .then(data => {
          qtySpan.textContent = data.qty;
          updateCartCount();
        });
      });
    }

    if (btnMinus) {
      btnMinus.addEventListener("click", () => {
        fetch(`/carrito/eliminar/${tipo}/${id}/`, {
          method: "POST",
          headers: { 'X-CSRFToken': getCSRFToken() }
        })
        .then(res => res.json())
        .then(data => {
          if (data.qty <= 0) {
            const container = document.getElementById(`container-${tipo}-${id}`);
            container.innerHTML = `<button class="btn btn-add-full btn-add" data-id="${id}" data-tipo="${tipo}">Agregar</button>`;
            agregarBotonAgregar();
          } else {
            qtySpan.textContent = data.qty;
          }
          updateCartCount();
        });
      });
    }
  }

  // 🔹 Botón "Agregar" inicial
  function agregarBotonAgregar() {
    document.querySelectorAll(".btn-add").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.dataset.id;
        const tipo = btn.dataset.tipo;

        fetch(`/carrito/agregar/${tipo}/${id}/`, {
          method: "POST",
          headers: { 'X-CSRFToken': getCSRFToken() }
        })
        .then(res => res.json())
        .then(data => {
          crearControl(id, tipo, data.qty);
          updateCartCount();
        });
      });
    });
  }

  // 🔹 Restaurar cantidades al cargar la página
  function restaurarCantidades() {
    fetch("/carrito/estado/")
      .then(res => res.json())
      .then(data => {
        data.items.forEach(item => {
          if(item.qty > 0){
            crearControl(item.id, item.tipo, item.qty);
          }
        });
        updateCartCount();
      });
  }

  // Inicializar
  agregarBotonAgregar();
  restaurarCantidades();

});
