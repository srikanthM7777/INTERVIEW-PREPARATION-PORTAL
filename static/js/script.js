// Highlight selected quiz option
document.addEventListener("click", function (e) {
  const option = e.target.closest(".quiz-option");
  if (!option) return;
  const group = option.closest(".options-group");
  group.querySelectorAll(".quiz-option").forEach((el) => el.classList.remove("border-primary", "bg-light"));
  option.classList.add("border-primary", "bg-light");
  const radio = option.querySelector("input[type=radio]");
  if (radio) radio.checked = true;
});

// Countdown timer for mock tests
function startCountdown(seconds, displayId, formId) {
  const display = document.getElementById(displayId);
  if (!display) return;
  let remaining = seconds;

  const interval = setInterval(() => {
    const m = Math.floor(remaining / 60).toString().padStart(2, "0");
    const s = (remaining % 60).toString().padStart(2, "0");
    display.textContent = `${m}:${s}`;

    if (remaining <= 0) {
      clearInterval(interval);
      const form = document.getElementById(formId);
      if (form) form.submit();
    }
    remaining--;
  }, 1000);
}

// Profile photo preview
function previewPhoto(input, imgId) {
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = function (e) {
      document.getElementById(imgId).src = e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  }
}
