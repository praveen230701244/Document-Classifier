const form = document.getElementById("upload-form");
const input = document.getElementById("documents");
const dropZone = document.getElementById("drop-zone");
const preview = document.getElementById("preview");
const loadingOverlay = document.getElementById("loading-overlay");

if (dropZone && input) {
  dropZone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
  });

  dropZone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropZone.classList.remove("dragover");
    if (event.dataTransfer.files.length) {
      input.files = event.dataTransfer.files;
      renderPreview(input.files);
    }
  });
}

if (input) {
  input.addEventListener("change", () => renderPreview(input.files));
}

if (form) {
  form.addEventListener("submit", () => {
    if (loadingOverlay) {
      loadingOverlay.classList.remove("hidden");
    }
  });
}

function renderPreview(files) {
  if (!preview) {
    return;
  }

  preview.innerHTML = "";
  Array.from(files).forEach((file) => {
    if (!file.type.startsWith("image/")) {
      return;
    }

    const reader = new FileReader();
    const card = document.createElement("div");
    card.className = "preview-item";
    const image = document.createElement("img");
    const name = document.createElement("p");
    name.textContent = file.name;
    card.appendChild(image);
    card.appendChild(name);
    preview.appendChild(card);

    reader.onload = (event) => {
      image.src = event.target.result;
    };
    reader.readAsDataURL(file);
  });
}
