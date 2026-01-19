 document.addEventListener('DOMContentLoaded', () => {
            const dropZone = document.getElementById('drop-zone');
            const fileInput = document.getElementById('file-upload');
            const fileInfo = document.getElementById('file-info');
            const fileNameDisplay = document.getElementById('filename');
            const fileSizeDisplay = document.getElementById('filesize');
            const clearBtn = document.getElementById('clear-file');
            const form = document.getElementById('uploadForm');
            const submitBtn = document.getElementById('submit-btn');

            function formatBytes(bytes, decimals = 2) {
                if (!+bytes) 
                    return '0 Bytes';

                const k = 1024;
                const dm = decimals < 0 ? 0 : decimals;
                const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
            }

            function handleFileSelect(file) {
                if (file) {
                    fileNameDisplay.textContent = file.name;
                    fileSizeDisplay.textContent = formatBytes(file.size);
                    fileInfo.classList.remove('hidden');
                    dropZone.classList.add('border-indigo-400', 'bg-indigo-50/30');
                }
            }

            fileInput.addEventListener('change', function(e) {
                if (this.files[0]) handleFileSelect(this.files[0]);
            });

            const preventDefaults = (e) => {
                e.preventDefault();
                e.stopPropagation();
            };

            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, preventDefaults, false);
            });

            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-active'), false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-active'), false);
            });

            dropZone.addEventListener('drop', (e) => {
                const dt = e.dataTransfer;
                const files = dt.files;
                
                if (files.length > 0) {
                    fileInput.files = files;
                    handleFileSelect(files[0]);
                }
            }, false);

            clearBtn.addEventListener('click', () => {
                fileInput.value = '';
                fileInfo.classList.add('hidden');
                dropZone.classList.remove('border-indigo-400', 'bg-indigo-50/30');
            });

            form.addEventListener('submit', (e) => {
                const originalContent = submitBtn.innerHTML;
                
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processando...';
                submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
        
            });
        });