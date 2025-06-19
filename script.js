const API_URL = "/api/tasks";
const input = document.getElementById("task-input");
const list = document.getElementById("task-list");

async function loadTasks() {
    const res = await fetch(API_URL);
    const tasks = await res.json();
    renderTasks(tasks);
}

function renderTasks(tasks) {
    list.innerHTML = "";
    tasks.forEach(task => {
        const li = document.createElement("li");
        li.className = task.done ? "finished" : "";

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = task.done;
        checkbox.onchange = async () => {
            await fetch(`${API_URL}/${task.id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ done: checkbox.checked })
            });
            loadTasks();
        };

        const text = document.createTextNode(" " + task.name + " ");

        const removeBtn = document.createElement("button");
        removeBtn.textContent = "刪除";
        removeBtn.onclick = async () => {
            await fetch(`${API_URL}/${task.id}`, { method: "DELETE" });
            loadTasks();
        };

        li.appendChild(checkbox);
        li.appendChild(text);
        li.appendChild(removeBtn);
        list.appendChild(li);
    });
}

async function addTask() {
    const name = input.value.trim();
    if (!name) return;
    await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    });
    input.value = "";
    loadTasks();
}

async function clearTasks() {
    await fetch(API_URL, { method: "DELETE" });
    loadTasks();
}

loadTasks();
