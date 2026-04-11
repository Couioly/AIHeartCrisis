function initForm() {
    const container = document.getElementById('formFields');
    container.innerHTML = formFields.map(field => {
        let input;
        if (field.type === 'select') {
            input = `
                <select id="field_${field.key}" required>
                    <option value="">请选择</option>
                    ${field.options.map(opt => `<option value="${opt.value}">${opt.label}</option>`).join('')}
                </select>
            `;
        } else {
            input = `
                <input 
                    type="${field.type}" 
                    id="field_${field.key}" 
                    placeholder="${field.placeholder || ''}"
                    ${field.min !== undefined ? `min="${field.min}"` : ''}
                    ${field.max !== undefined ? `max="${field.max}"` : ''}
                    ${field.step !== undefined ? `step="${field.step}"` : ''}
                    required
                >
            `;
        }
        return `
            <div class="form-group">
                <label>${field.label}</label>
                ${input}
            </div>
        `;
    }).join('');
}

function resetForm() {
    formFields.forEach(field => {
        const el = document.getElementById(`field_${field.key}`);
        if (el) el.value = '';
    });
    document.getElementById('resultPanel').classList.remove('show');
}

function getFormData() {
    const data = {};
    formFields.forEach(field => {
        const el = document.getElementById(`field_${field.key}`);
        if (el) {
            data[field.key] = field.type === 'number' ? parseFloat(el.value) : el.value;
        }
    });
    return data;
}
