document.addEventListener("DOMContentLoaded", () => {

      function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }

      const updateCart = async (pizzaId, action) => {
        const response = await fetch(`/carrito/update/${pizzaId}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({ action: action })
        });
        const data = await response.json();
        const container = document.getElementById(`container-${pizzaId}`);

        if (data.cantidad > 0) {
          container.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
              <button class="btn btn-danger btn-sm btn-minus" data-id="${pizzaId}">-</button>
              <span class="mx-2 fw-bold quantity" id="qty-${pizzaId}">${data.cantidad}</span>
              <button class="btn btn-success btn-sm btn-plus" data-id="${pizzaId}">+</button>
            </div>
          `;
        } else {
          container.innerHTML = `<button class="btn btn-add-full btn-add" data-id="${pizzaId}">Agregar</button>`;
        }

        attachButtons(); // Reasignar eventos
      };

      function attachButtons() {
        document.querySelectorAll('.btn-plus').forEach(btn => {
          btn.onclick = () => updateCart(btn.dataset.id, 'add');
        });
        document.querySelectorAll('.btn-minus').forEach(btn => {
          btn.onclick = () => updateCart(btn.dataset.id, 'remove');
        });
        document.querySelectorAll('.btn-add').forEach(btn => {
          btn.onclick = () => updateCart(btn.dataset.id, 'add');
        });
      }

      attachButtons();

    });