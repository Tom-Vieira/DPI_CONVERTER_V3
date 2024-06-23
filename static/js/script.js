document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const fileList = document.getElementById('file-list');
    const submitButton = document.getElementById('submit-button');
    const downloadAllButton = document.querySelector('.download-all-button');
    const labelEsc = document.getElementById('label-1')
    const labelDpi = document.getElementById('label-2')
    const dpi = document.getElementById('dpi')

    // Monitorar mudanças no input de arquivo
    fileInput.addEventListener('change', function(event) {
        fileList.innerHTML = '';
        const files = event.target.files;

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const listItem = document.createElement('div');
            listItem.textContent = file.name;
            fileList.appendChild(listItem);
        }

     
        
    });

  

    // Verificar se há imagens processadas para mostrar o botão download
    if (document.querySelector('.processed-images li')) {
       
        downloadAllButton.style.display = 'inline-block';
    } else {
       
        downloadAllButton.style.display = 'none';
    }

    //Verificar se há imagens processadas para ocultar as labels e os inputs já usados
    if (document.querySelector('.processed-images li')){
        labelEsc.style.display = 'none'
        labelDpi.style.display = 'none'
        dpi.style.display = 'none'
        fileInput.style.display = 'none'
        submitButton.style.display = 'none'
    }

   


      


});

 
