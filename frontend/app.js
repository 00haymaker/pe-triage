const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const resultBody = document.getElementById('resultBody');

uploadBtn.addEventListener('click', async () => {
    const files = fileInput.files;
    if (!files || files.length === 0) {
        alert('분석할 파일을 하나 이상 선택해 주세요.');
        return;
    }

    // 파일별로 테이블 행을 동적으로 추가하고 분석 요청
    for (const file of files) {
        const rowId = `row-${Date.now()}-${Math.random().toString(36).substr(2, 5)}`;
        appendInitialRow(rowId, file.name);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/api/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`서버 에러 (${response.status})`);
            }

            const data = await response.json();
            updateRowSuccess(rowId, data);
        } catch (error) {
            updateRowError(rowId, error.message);
        }
    }
});

function appendInitialRow(rowId, fileName) {
    const tr = document.createElement('tr');
    tr.id = rowId;
    tr.innerHTML = `
        <td><strong>${fileName}</strong></td>
        <td><span class="badge analyzing">분석 중...</span></td>
        <td>-</td>
        <td>-</td>
        <td>-</td>
    `;
    resultBody.appendChild(tr);
}

function updateRowSuccess(rowId, result) {
    const tr = document.getElementById(rowId);
    if (!tr) return;

    const summary = result.summary;
    const details = result.details;

    tr.innerHTML = `
        <td><strong>${result.filename}</strong></td>
        <td><span class="badge normal">${summary.verdict}</span></td>
        <td>
            <div>${details.hash_engine.status}</div>
            <div class="detail-text">SHA-256: ${details.hash_engine.sha256.substring(0, 16)}...</div>
        </td>
        <td>
            <div>${details.pe_engine.status}</div>
            <div class="detail-text">Entropy: ${details.pe_engine.entropy}</div>
        </td>
        <td>
            <div>${details.yara_engine.status}</div>
            <div class="detail-text">Matched: ${details.yara_engine.matched_count}건</div>
        </td>
    `;
}

function updateRowError(rowId, errorMessage) {
    const tr = document.getElementById(rowId);
    if (!tr) return;

    tr.innerHTML = `
        <td><strong>분석 실패</strong></td>
        <td><span class="badge error">ERROR</span></td>
        <td colspan="3">${errorMessage}</td>
    `;
}