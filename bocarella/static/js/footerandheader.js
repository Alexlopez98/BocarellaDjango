document.addEventListener("DOMContentLoaded", () => {

  /*** Función para actualizar el carrito ***/
  window.updateHeaderCartCount = function() {
    const activeUser = JSON.parse(localStorage.getItem("activeUser"));
    const key = activeUser ? `cart_${activeUser.usuario}` : "cart_guest";
    const cart = JSON.parse(localStorage.getItem(key)) || [];
    const totalProducts = cart.reduce((sum, item) => sum + item.cantidad, 0);

    const cartCountOriginal = document.querySelector("#cart-count");
    if (cartCountOriginal) cartCountOriginal.textContent = totalProducts;

    const cartCountClone = document.querySelector("#subHeaderClone #cart-count");
    if (cartCountClone) cartCountClone.textContent = totalProducts;
  };

  updateHeaderCartCount();

  /*** Función para actualizar login/logout ***/
  const activeUser = JSON.parse(localStorage.getItem("activeUser"));
  const loginLink = document.querySelector(".ingresa");
  const logoutBtn = document.getElementById("logoutBtn");

  if (activeUser) {
    loginLink.textContent = activeUser.usuario;
    loginLink.href = "#";
    loginLink.classList.add("dropdown-toggle");
    loginLink.setAttribute("data-bs-toggle", "dropdown");

    if (logoutBtn) {
      logoutBtn.style.display = "block";
      logoutBtn.onclick = () => {
        localStorage.removeItem("activeUser");
        window.location.href = "/";
      };
    }
  } else {
    loginLink.innerHTML = 'Ingresa <i class="fa-regular fa-circle-user"></i>';
    loginLink.href = "/acceso/";
    loginLink.classList.remove("dropdown-toggle");
    loginLink.removeAttribute("data-bs-toggle");

    if (logoutBtn) logoutBtn.style.display = "none";
  }

  /*** Sticky subheader ***/
  const subHeader = document.getElementById("subHeader");
  if (!subHeader) return;

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
        updateHeaderCartCount();
      }
    } else {
      if (clonedSubHeader) {
        clonedSubHeader.style.transition = "top 0.1s ease";
        clonedSubHeader.style.top = `-${subHeader.offsetHeight}px`;
        setTimeout(() => {
          if (clonedSubHeader) {
            clonedSubHeader.remove();
            clonedSubHeader = null;
          }
        }, 500);
      }
    }
  });
});
