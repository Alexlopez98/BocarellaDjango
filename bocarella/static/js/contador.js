document.addEventListener("DOMContentLoaded", () => {

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(cookie => {
        const [key, value] = cookie.trim().split('=');
        if (key === name) cookieValue = decodeURIComponent(value);
      });
    }
    return cookieValue;
  }

  function crearControl(id, cantidad) {
    const container = document.getElementById(`container-${id}`);
    container.innerHTML = `
      <div class="d-flex justify-content-between align-items-center">
        <button class="btn btn-danger btn-sm btn-minus" data-id="${id}">-</button>
        <span class="mx-2 fw-bold quantity" id="qty-${id}">${cantidad}</span>
        <button class="btn btn-success btn-sm btn-plus" data-id="${id}">+</button>
      </div>
    `;
    agregarEventos(id);
  }

  function agregarEventos(id) {
    const btnPlus = document.querySelector(`#container-${id} .btn-plus`);
    const btnMinus = document.querySelector(`#container-${id} .btn-minus`);
    const qtySpan = document.getElementById(`qty-${id}`);

    btnPlus.addEventListener("click", () => {
      fetch(`/carrito/agregar/${id}/`, {
        method: "POST",
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
      })
      .then(res => res.json())
      .then(data => {
        qtySpan.textContent = data.qty;
      });
    });

    btnMinus.addEventListener("click", () => {
      fetch(`/carrito/eliminar/${id}/`, {
        method: "POST",
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
      })
      .then(res => res.json())
      .then(data => {
        if (data.qty <= 0) {
          const container = document.getElementById(`container-${id}`);
          container.innerHTML = `<button class="btn btn-add-full btn-add" data-id="${id}">Agregar</button>`;
          agregarBotonAgregar();
        } else {
          qtySpan.textContent = data.qty;
        }
      });
    });
  }

  function agregarBotonAgregar() {
    document.querySelectorAll(".btn-add").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.dataset.id;
        fetch(`/carrito/agregar/${id}/`, {
          method: "POST",
          headers: { 'X-CSRFToken': getCookie('csrftoken') }
        })
        .then(res => res.json())
        .then(data => {
          crearControl(id, data.qty);
        });
      });
    });
  }

  agregarBotonAgregar();

});
