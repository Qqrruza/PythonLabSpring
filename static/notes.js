
async function loadNotes() {
    try {
        const response = await fetch('/api/notes');
        if (!response.ok) throw new Error('Ошибка загрузки');
        const notes = await response.json();
        const listContainer = document.getElementById('notes-list');
        listContainer.innerHTML = '';
        notes.forEach(note => {
            const li = document.createElement('li');
            const span = document.createElement('span');
            span.className = 'note-text';
            if (note.important) {
                span.classList.add('important-note');
            }
            span.textContent = note.text;
            li.appendChild(span);
            listContainer.appendChild(li);
        });
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const textInput = document.getElementById('note-text');
    const text = textInput.value.trim();
    const important = document.getElementById('note-important').checked;
    if (!text) return;

    try {
        const response = await fetch('/api/notes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, important })
        });
        if (!response.ok) throw new Error('Ошибка добавления');
        textInput.value = '';
        document.getElementById('note-important').checked = false;
        await loadNotes(); // обновить список
    } catch (error) {
        console.error('Ошибка:', error);
    }
});

document.getElementById('clear-btn').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/notes/clear', { method: 'DELETE' });
        if (!response.ok) throw new Error('Ошибка очистки');
        await loadNotes();
    } catch (error) {
        console.error('Ошибка:', error);
    }
    
});

document.addEventListener('DOMContentLoaded', loadNotes);