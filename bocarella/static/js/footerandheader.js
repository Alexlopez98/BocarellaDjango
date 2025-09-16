document.addEventListener("DOMContentLoaded", () => {

  function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
  }

  function updateCartCount() {
    const cartCountEls = document.querySelectorAll("#cart-count");
    let total = 0;
    const cartSession = JSON.parse(localStorage.getItem("cart_session") || "{}");
    for (let key in cartSession) total += cartSession[key];
    cartCountEls.forEach(el => el.textContent = total);
  }

  function updateButtonText(btn, productId) {
    const cartSession = JSON.parse(localStorage.getItem("cart_session") || "{}");
    const count = cartSession[productId] || 0;
    btn.innerHTML = count > 0 
      ? `Agregado (${count}) ✅` 
      : `<i class="fa-solid fa-cart-plus"></i> Agregar`;
  }

  // Función para agregar unidad
  function addToCart(productId, btn) {
    btn.disabled = true;
    fetch(`/carrito/agregar/${productId}/`, {
      method: "POST",
      headers: { 'X-CSRFToken': getCSRFToken() }
    }).then(res => {
      if(res.ok){
        let cartSession = JSON.parse(localStorage.getItem("cart_session") || "{}");
        cartSession[productId] = (cartSession[productId] || 0) + 1;
        localStorage.setItem("cart_session", JSON.stringify(cartSession));

        updateCartCount();
        updateButtonText(btn, productId);

        const badge = document.querySelector("#cart-count");
        if(badge){
          badge.classList.add("animate__animated", "animate__bounce");
          setTimeout(() => badge.classList.remove("animate__animated", "animate__bounce"), 500);
        }
      } else {
        alert("Error al agregar el producto");
      }
    }).catch(() => alert("Error de conexión"))
      .finally(() => btn.disabled = false);
  }

  // Función para quitar unidad
  function removeFromCart(productId, btn) {
    let cartSession = JSON.parse(localStorage.getItem("cart_session") || "{}");
    if(cartSession[productId] && cartSession[productId] > 0){
      cartSession[productId] -= 1;
      if(cartSession[productId] === 0) delete cartSession[productId];
      localStorage.setItem("cart_session", JSON.stringify(cartSession));
      updateCartCount();
      updateButtonText(btn, productId);
    }
  }

  // Inicializar botones
  document.querySelectorAll(".add-to-cart").forEach(btn => {
    const productId = btn.dataset.productId;
    updateButtonText(btn, productId);

    // Controles + y - si existen
    const btnAdd = btn.parentElement.querySelector(".btn-add");
    const btnRemove = btn.parentElement.querySelector(".btn-remove");

    btn.addEventListener("click", e => {
      e.preventDefault();
      addToCart(productId, btn);
    });

    if(btnAdd) btnAdd.addEventListener("click", () => addToCart(productId, btn));
    if(btnRemove) btnRemove.addEventListener("click", () => removeFromCart(productId, btn));
  });

  // Sticky subheader
  const subHeader = document.getElementById("subHeader");
  if(subHeader) {
    const showScroll = 155;
    let clonedSubHeader = null;

    window.addEventListener("scroll", () => {
      const scrollTop = window.scrollY;
      if (scrollTop > showScroll) {
        if (!clonedSubHeader) {
          clonedSubHeader = subHeader.cloneNode(true);
          clonedSubHeader.id = "subHeaderClone";
          clonedSubHeader.style.position = "fixed";
          clonedSubHeader.style.top = `-${subHeader.offsetHeight}px`;
          clonedSubHeader.style.width = "100%";
          clonedSubHeader.style.zIndex = "999";
          clonedSubHeader.style.transition = "top 0.9s ease-out";
          document.body.appendChild(clonedSubHeader);
          clonedSubHeader.getBoundingClientRect();
          clonedSubHeader.style.top = "0px";
          updateCartCount();
        }
      } else if (clonedSubHeader) {
        clonedSubHeader.style.transition = "top 0.1s ease";
        clonedSubHeader.style.top = `-${subHeader.offsetHeight}px`;
        setTimeout(() => {
          if (clonedSubHeader) {
            clonedSubHeader.remove();
            clonedSubHeader = null;
          }
        }, 500);
      }
    });
  }

  window.updateCartCount = updateCartCount;
  updateCartCount();
});
