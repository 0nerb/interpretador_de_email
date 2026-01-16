 document.addEventListener('DOMContentLoaded', () => {
            // Elementos do DOM
            const dropZone = document.getElementById('drop-zone');
            const fileInput = document.getElementById('file-upload');
            const fileInfo = document.getElementById('file-info');
            const fileNameDisplay = document.getElementById('filename');
            const fileSizeDisplay = document.getElementById('filesize');
            const clearBtn = document.getElementById('clear-file');
            const form = document.getElementById('uploadForm');
            const submitBtn = document.getElementById('submit-btn');

            // --- FUNÇÕES UTILITÁRIAS ---
            
            // Formata bytes para KB/MB
            function formatBytes(bytes, decimals = 2) {
                if (!+bytes) return '0 Bytes';
                const k = 1024;
                const dm = decimals < 0 ? 0 : decimals;
                const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
            }

            // Atualiza a interface com dados do arquivo
            function handleFileSelect(file) {
                if (file) {
                    fileNameDisplay.textContent = file.name;
                    fileSizeDisplay.textContent = formatBytes(file.size);
                    fileInfo.classList.remove('hidden');
                    dropZone.classList.add('border-indigo-400', 'bg-indigo-50/30');
                }
            }

            // --- EVENT LISTENERS ---

            // 1. Clique tradicional no input
            fileInput.addEventListener('change', function(e) {
                if (this.files[0]) handleFileSelect(this.files[0]);
            });

            // 2. Drag and Drop (Arrastar e Soltar)
            const preventDefaults = (e) => {
                e.preventDefault();
                e.stopPropagation();
            };

            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, preventDefaults, false);
            });

            // Efeitos visuais ao arrastar
            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-active'), false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-active'), false);
            });

            // Soltar arquivo
            dropZone.addEventListener('drop', (e) => {
                const dt = e.dataTransfer;
                const files = dt.files;
                
                if (files.length > 0) {
                    fileInput.files = files; // Transfere arquivos para o input real
                    handleFileSelect(files[0]);
                }
            }, false);

            // 3. Botão Limpar
            clearBtn.addEventListener('click', () => {
                fileInput.value = ''; // Limpa o input
                fileInfo.classList.add('hidden'); // Esconde card
                dropZone.classList.remove('border-indigo-400', 'bg-indigo-50/30'); // Reseta estilo
            });

            // 4. Submit do Formulário (Feedback visual)
            form.addEventListener('submit', (e) => {
                // Em produção, remova o e.preventDefault() se quiser envio padrão
                // e.preventDefault(); 
                
                const originalContent = submitBtn.innerHTML;
                
                // Muda estado do botão
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processando...';
                submitBtn.classList.add('opacity-75', 'cursor-not-allowed');

                // Simulação de delay (Remover em produção)
                setTimeout(() => {
                    alert('Arquivo pronto para envio ao Django!');
                    submitBtn.innerHTML = originalContent;
                    submitBtn.disabled = false;
                    submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
                }, 1500);
            });
        });