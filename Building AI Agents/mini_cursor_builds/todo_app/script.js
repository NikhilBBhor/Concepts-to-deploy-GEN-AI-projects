function addTodo() {
    const todoText = document.getElementById("new-todo").value;
    if (todoText === "") return;
    const newTodo = document.createElement("li");
    newTodo.textContent = todoText;
    document.getElementById("todo-list").appendChild(newTodo);
    document.getElementById("new-todo").value = "";
}
