const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const uploadForm = document.getElementById('uploadForm');

// Drag and drop events
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'white';
    dropZone.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'rgba(255, 255, 255, 0.5)';
    dropZone.style.backgroundColor = 'transparent';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.borderColor = 'rgba(255, 255, 255, 0.5)';
    dropZone.style.backgroundColor = 'transparent';
    const files = e.dataTransfer.files;
    if (files.length) {
        fileInput.files = files;
        uploadForm.submit();
    }
});

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        uploadForm.submit();
    }
});