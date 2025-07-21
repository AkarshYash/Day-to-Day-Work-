import json
import os

# File to store to-do tasks
TODO_FILE = "todo.json"

# Load existing tasks or start fresh
def load_tasks():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            return json.load(file)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Display all tasks
def show_tasks(tasks):
    if not tasks:
        print("\n📝 Your to-do list is empty.")
        return
    print("\n📋 To-Do List:")
    for idx, task in enumerate(tasks, start=1):
        status = "[✔]" if task["done"] else "[ ]"
        print(f"{idx}. {status} {task['task']}")

# Add a task
def add_task(tasks):
    task_text = input("🔹 Enter a new task: ").strip()
    if task_text:
        tasks.append({"task": task_text, "done": False})
        print("✅ Task added!")
    else:
        print("⚠️ Task cannot be empty.")

# Mark a task as done
def mark_done(tasks):
    show_tasks(tasks)
    try:
        num = int(input("🔸 Enter task number to mark as done: "))
        if 1 <= num <= len(tasks):
            tasks[num - 1]["done"] = True
            print("✅ Task marked as done!")
        else:
            print("❌ Invalid task number.")
    except ValueError:
        print("❌ Please enter a valid number.")

# Delete a task
def delete_task(tasks):
    show_tasks(tasks)
    try:
        num = int(input("❌ Enter task number to delete: "))
        if 1 <= num <= len(tasks):
            deleted = tasks.pop(num - 1)
            print(f"🗑️ Deleted: {deleted['task']}")
        else:
            print("❌ Invalid task number.")
    except ValueError:
        print("❌ Please enter a valid number.")

# Main app loop
def main():
    tasks = load_tasks()

    while True:
        print("\n===== TO-DO MENU =====")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task as done")
        print("4. Delete task")
        print("5. Exit")
        choice = input("Choose an option (1-5): ")

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
            save_tasks(tasks)
        elif choice == "3":
            mark_done(tasks)
            save_tasks(tasks)
        elif choice == "4":
            delete_task(tasks)
            save_tasks(tasks)
        elif choice == "5":
            print("👋 Exiting To-Do App... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
