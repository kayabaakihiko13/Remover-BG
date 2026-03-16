const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadForm = document.getElementById('uploadForm');

// Drag and drop
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'white';
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'rgba(255, 255, 255, 0.5)';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'rgba(255, 255, 255, 0.5)';
    const files = e.dataTransfer.files;
    if (files.length) {
        fileInput.files = files;
        uploadForm.submit(); // ✅ Langsung submit dan redirect
    }
});

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        uploadForm.submit(); // ✅ Submit form dan redirect ke /upload
    }
});