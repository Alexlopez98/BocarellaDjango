document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registroForm");

  const password = document.getElementById("id_password");
  const confirm = document.getElementById("id_password_confirm");
  const username = document.getElementById("id_username");
  const email = document.getElementById("id_email");

  const strengthBar = document.getElementById("passwordStrengthBar");
  const strengthText = document.getElementById("passwordStrengthText");

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // ----------------------------
  // Funciones de validación
  // ----------------------------
  function evaluarFuerza(pass) {
    let score = 0;
    if (pass.length >= 6) score++;
    if (/[A-Z]/.test(pass)) score++;
    if (/\d/.test(pass)) score++;
    if (/[@$!%*?&]/.test(pass)) score++;
    return score; // 0 a 4
  }

  function actualizarBarra(pass) {
    const score = evaluarFuerza(pass);
    let width = (score / 4) * 100;
    strengthBar.style.width = width + "%";

    if (score === 0) {
      strengthBar.className = "progress-bar bg-danger";
      strengthText.textContent = "";
    } else if (score === 1) {
      strengthBar.className = "progress-bar bg-danger";
      strengthText.textContent = "Muy débil";
    } else if (score === 2) {
      strengthBar.className = "progress-bar bg-warning";
      strengthText.textContent = "Débil";
    } else if (score === 3) {
      strengthBar.className = "progress-bar bg-info";
      strengthText.textContent = "Media";
    } else if (score === 4) {
      strengthBar.className = "progress-bar bg-success";
      strengthText.textContent = "Fuerte";
    }
  }

  function validarConfirm() {
    // Eliminar cualquier mensaje previo
    const msgExistente = confirm.parentNode.querySelector(".invalid-feedback");
    if (msgExistente) msgExistente.remove();

    if (confirm.value === "") {
      confirm.classList.remove("is-valid", "is-invalid");
      return;
    }

    if (confirm.value === password.value) {
      confirm.classList.add("is-valid");
      confirm.classList.remove("is-invalid");
    } else {
      confirm.classList.add("is-invalid");
      confirm.classList.remove("is-valid");

      const msg = document.createElement("div");
      msg.className = "invalid-feedback";
      msg.textContent = "Las contraseñas no coinciden";
      confirm.parentNode.appendChild(msg);
    }
  }

  function validarEmail() {
    if (email.value === "") {
      email.classList.remove("is-valid", "is-invalid");
      return;
    }
    if (emailRegex.test(email.value.trim())) {
      email.classList.add("is-valid");
      email.classList.remove("is-invalid");
    } else {
      email.classList.add("is-invalid");
      email.classList.remove("is-valid");
    }
  }

  function validarUsername() {
    if (username.value.trim().length >= 3) {
      username.classList.add("is-valid");
      username.classList.remove("is-invalid");
    } else {
      username.classList.add("is-invalid");
      username.classList.remove("is-valid");
    }
  }

  // ----------------------------
  // Eventos
  // ----------------------------
  password.addEventListener("input", () => {
    actualizarBarra(password.value);
    validarConfirm();
  });

  confirm.addEventListener("input", validarConfirm);
  email.addEventListener("input", validarEmail);
  username.addEventListener("input", validarUsername);

  form.addEventListener("submit", (e) => {
    // Validaciones finales antes de enviar
    actualizarBarra(password.value);
    validarConfirm();
    validarEmail();
    validarUsername();

    const invalido = form.querySelector(".is-invalid");
    if (invalido) {
      e.preventDefault();
      alert("❌ Corrige los errores antes de enviar.");
    }
  });
});
