document.addEventListener("DOMContentLoaded", () => {

  // 🔹 Obtener CSRF token
  function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
  }

  // 🔹 Actualizar cantidad en la tarjeta del producto
  function actualizarCantidad(id, tipo, qty) {
    const qtySpan = document.getElementById(`qty-${tipo}-${id}`);
    if(qtySpan) qtySpan.textContent = qty;
  }

  // 🔹 Agregar eventos + / -
  function agregarEventos(id, tipo) {
    const container = document.getElementById(`container-${tipo}-${id}`);
    if(!container) return;

    const btnPlus = container.querySelector(".btn-plus");
    const btnMinus = container.querySelector(".btn-minus");

    if(btnPlus){
      btnPlus.addEventListener("click", () => {
        fetch(`/carrito/agregar/${tipo}/${id}/`, {
          method: "POST",
          headers: { "X-CSRFToken": getCSRFToken() }
        })
        .then(res => res.json())
        .then(data => {
          actualizarCantidad(id, tipo, data.qty);
        });
      });
    }

    if(btnMinus){
      btnMinus.addEventListener("click", () => {
        fetch(`/carrito/eliminar/${tipo}/${id}/`, {
          method: "POST",
          headers: { "X-CSRFToken": getCSRFToken() }
        })
        .then(res => res.json())
        .then(data => {
          if(data.qty <= 0){
            container.innerHTML = `<button class="btn btn-add-full btn-add" data-id="${id}" data-tipo="${tipo}">Agregar</button>`;
            agregarBotonAgregar(); // Reasignar evento al nuevo botón
          } else {
            actualizarCantidad(id, tipo, data.qty);
          }
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
          headers: { "X-CSRFToken": getCSRFToken() }
        })
        .then(res => res.json())
        .then(data => {
          const container = document.getElementById(`container-${tipo}-${id}`);
          if(container){
            container.innerHTML = `
              <div class="d-flex justify-content-between align-items-center">
                <button class="btn btn-danger btn-sm btn-minus" data-id="${id}" data-tipo="${tipo}">-</button>
                <span class="mx-2 fw-bold quantity" id="qty-${tipo}-${id}">${data.qty}</span>
                <button class="btn btn-success btn-sm btn-plus" data-id="${id}" data-tipo="${tipo}">+</button>
              </div>
            `;
            agregarEventos(id, tipo);
          }
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
          const container = document.getElementById(`container-${item.tipo}-${item.id}`);
          if(container){
            container.innerHTML = `
              <div class="d-flex justify-content-between align-items-center">
                <button class="btn btn-danger btn-sm btn-minus" data-id="${item.id}" data-tipo="${item.tipo}">-</button>
                <span class="mx-2 fw-bold quantity" id="qty-${item.tipo}-${item.id}">${item.qty}</span>
                <button class="btn btn-success btn-sm btn-plus" data-id="${item.id}" data-tipo="${item.tipo}">+</button>
              </div>
            `;
            agregarEventos(item.id, item.tipo);
          }
        });
      });
  }

  // 🔹 Inicializar
  agregarBotonAgregar();
  restaurarCantidades();

});
