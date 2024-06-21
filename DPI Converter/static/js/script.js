document.addEventListener('DOMContentLoaded', () => {
    const directoryForm = document.getElementById('directory-form');
    const dpiForm = document.getElementById('dpi-form');

    if (directoryForm) {
        directoryForm.addEventListener('submit', (e) => {
            const directoryInput = document.getElementById('directory');
            if (!directoryInput.value.trim()) {
                e.preventDefault();
                alert('Por favor, insira um diretório válido.');
            }
        });
    }

    if (dpiForm) {
        dpiForm.addEventListener('submit', (e) => {
            const dpiInput = document.getElementById('dpi');
            if (!dpiInput.value.trim() || parseInt(dpiInput.value) <= 0) {
                e.preventDefault();
                alert('Por favor, insira um valor de DPI válido.');
            }
        });
    }
});
