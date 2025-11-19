const API_BASE_URL = "http://localhost:8001/process";

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const processBtn = document.getElementById('processBtn');
    const modeSelect = document.getElementById('modeSelect');
    const originalImage = document.getElementById('originalImage');
    const processedImage = document.getElementById('processedImage');
    const originalPlaceholder = document.getElementById('originalPlaceholder');
    const processedPlaceholder = document.getElementById('processedPlaceholder');
    const originalCard = document.getElementById('originalCard');
    const processedCard = document.getElementById('processedCard');
    const fileNameDisplay = document.getElementById('fileName');

    // File selection handler
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Update file name display
        fileNameDisplay.textContent = file.name;

        // Show preview
        const objectUrl = URL.createObjectURL(file);
        originalImage.src = objectUrl;
        originalImage.style.display = 'block';
        originalPlaceholder.style.display = 'none';
        originalCard.classList.add('has-image');
        
        // Reset processed image
        processedImage.style.display = 'none';
        processedPlaceholder.style.display = 'block';
        processedCard.classList.remove('has-image');
    });

    // Process button handler
    processBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) {
            alert("画像を選択してください");
            return;
        }

        const mode = modeSelect.value;
        const url = `${API_BASE_URL}/${mode}`;
        
        // Set loading state
        setLoading(true);

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch(url, {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                const objectUrl = URL.createObjectURL(blob);
                
                processedImage.src = objectUrl;
                processedImage.style.display = 'block';
                processedPlaceholder.style.display = 'none';
                processedCard.classList.add('has-image');
            } else {
                const errorText = await response.text();
                alert(`エラーが発生しました: ${response.status} - ${errorText}`);
            }
        } catch (error) {
            console.error(error);
            alert("サーバーとの通信に失敗しました。バックエンドが起動しているか確認してください。");
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        if (isLoading) {
            processBtn.disabled = true;
            processBtn.classList.add('loading');
            processBtn.querySelector('.btn-text').textContent = '処理中...';
        } else {
            processBtn.disabled = false;
            processBtn.classList.remove('loading');
            processBtn.querySelector('.btn-text').textContent = '加工実行';
        }
    }
});
