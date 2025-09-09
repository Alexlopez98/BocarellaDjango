document.addEventListener("DOMContentLoaded", () => {
  const passRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,18}$/;

  // Login
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      alert("✅ Bienvenido DemoUser");
      window.location.href = "/";  // redirige al index
    });
  }

  // Registro
  const registroForm = document.getElementById("registroForm");
  if (registroForm) {
    const pass = document.getElementById("regPass");
    const confirm = document.getElementById("regConfirm");
    const strengthBar = document.createElement("div");
    strengthBar.className = "progress my-2";
    strengthBar.innerHTML = `<div class="progress-bar" role="progressbar" style="width: 0%;"></div>`;
    pass.parentNode.appendChild(strengthBar);
    const strengthFill = strengthBar.querySelector(".progress-bar");

    pass.addEventListener("input", () => {
      const val = pass.value;
      let strength = 0;
      if (val.length >= 6) strength++;
      if (/[A-Z]/.test(val)) strength++;
      if (/\d/.test(val)) strength++;
      if (/[@$!%*?&]/.test(val)) strength++;

      const colors = ["bg-danger", "bg-warning", "bg-info", "bg-success"];
      strengthFill.style.width = `${(strength / 4) * 100}%`;
      strengthFill.className = `progress-bar ${colors[strength - 1] || "bg-danger"}`;
    });

    registroForm.addEventListener("submit", (e) => {
      e.preventDefault();
      if (pass.value !== confirm.value) {
        alert("❌ Las contraseñas no coinciden");
        return;
      }
      if (!passRegex.test(pass.value)) {
        alert("❌ Contraseña débil");
        return;
      }
      alert("✅ Registro exitoso (Demo)");
      window.location.href = "/";  // redirige al index
    });
  }

  // Perfil (solo visual)
  const perfilPass = document.getElementById("perfilPass");
  if (perfilPass) {
    const perfilStrengthBar = document.createElement("div");
    perfilStrengthBar.className = "progress my-2";
    perfilStrengthBar.innerHTML = `<div class="progress-bar" role="progressbar" style="width: 0%;"></div>`;
    perfilPass.parentNode.appendChild(perfilStrengthBar);
    const perfilStrengthFill = perfilStrengthBar.querySelector(".progress-bar");

    perfilPass.addEventListener("input", () => {
      const val = perfilPass.value;
      let strength = 0;
      if (val.length >= 6) strength++;
      if (/[A-Z]/.test(val)) strength++;
      if (/\d/.test(val)) strength++;
      if (/[@$!%*?&]/.test(val)) strength++;

      const colors = ["bg-danger", "bg-warning", "bg-info", "bg-success"];
      perfilStrengthFill.style.width = `${(strength / 4) * 100}%`;
      perfilStrengthFill.className = `progress-bar ${colors[strength - 1] || "bg-danger"}`;
    });
  }
});
