import storage
import tabulate
import textwrap

def add_task():
    task = str(input("Enter task name (necessary)# "))
    details = str(input("Enter additional details. No more than 200 characters.# ")).lower()
    priority = str(input("Priority (low, mid, high)# ")).lower()
    due_date = input("When will this task be due? Enter date thus: DD/MM/YY. \n And yes if it's today, enter today's date (it's anti-lazy training 👀)# ")

    if task == None:
        return Exception("Enter task, oga. No dey use me play.")
    elif len(details) > 200:
        return Exception("Details has passed character limit.")
    elif priority not in ['low', 'mid', 'high']:
        return Exception("invalid prioriy entry")
    else:
        try:
            storage.add_task(task, details, priority, due_date)
            print("Task added successfully.")
            return 1
        except Exception as e:
            print(e)
            return 0

def mark_done():
    id = int(input("Enter task ID mark as done, sharp sharp, no waste my time: "))
    status = "Done"
    storage.mark_done(id, status)
    print("Task marked as done successfully.")

def delete_task():
    id = int(input("Enter task ID to delete: "))
    storage.delete_task(id)
    print("Task deleted successfully.")

def filter_by_status_or_priority():
    status = input("Enter status to filter by (Pending, Done) or leave blank: ").strip()
    priority = input("Enter priority to filter by (low, mid, high) or leave blank: ").strip()
    tasks = storage.filter_tasks(status=status if status else None, priority=priority if priority else None)
    return tasks

def get_archived_tasks():
    tasks = storage.get_tasks(archived=True)
    return tasks

def sort_by_due_date_and_or_priority():
    due_date = input("Sort by urgency (due date)? Enter 1 if yes, or 0 otherwise: \n")
    priority = input("Sort by level of priority? Enter 1 if yes, or 0 otherwise: ")
    # I never sabi to sort am, chai , edit: I don do am !!!!! Comot there!!!!
    tasks = storage.sort_tasks_and_or_priority(due_date=due_date, priority=priority)
    return tasks

def print_tasks(tasks):
    table = []
    for t in tasks:
        wrapped_details = "\n".join(textwrap.wrap(t.details, width=30))  # Wrap at 30 chars
        table.append([
            t.id,
            t.description,
            wrapped_details,
            t.priority,
            t.due_date,
            t.status,
            "Yes" if t.archived else "No"
        ])
    headers = ["ID", "Description", "Details", "Priority", "Due Date", "Status", "Archived"]
    print(tabulate.tabulate(table, headers, tablefmt="grid"))

def home():
    flag = True
    tasks = storage.get_tasks()
    if tasks:
        print_tasks(tasks)
    else:
        print("No tasks here yet")

    while flag:
        print("Actions: ")
        print("1. Add Task \n2. Mark Done \n3. Delete Task \n4. Filter by Status or priority \n5. Get archived tasks \n6. Sort by due date and or priority \n7. Exit ")
        ans = int(input("What action do you want to perform? Enter the corresponding number: "))
        if ans == 1:
            if add_task():
                tasks = storage.get_tasks()
                print_tasks(tasks)
        elif ans == 2:
            mark_done()
            tasks = storage.get_tasks()
            print_tasks(tasks)
        elif ans == 3:
            delete_task()
            tasks = storage.get_tasks()
            print_tasks(tasks)
        elif ans == 4:
            tasks = filter_by_status_or_priority()
            if not tasks:
                print("No tasks found with the given criteria.")
            else:
                print_tasks(tasks)
        elif ans == 5:
            tasks = get_archived_tasks()
            if not tasks:
                print("No tasks in the archive.")
            else:
                print_tasks(tasks)
        elif ans == 6:
            tasks = sort_by_due_date_and_or_priority()
            print_tasks(tasks)
        elif ans == 7:
            print("Alright. Get to work!")
            flag = False
            break
        else:
            print("Invalid action!")
    return None
           

def main():
    storage.init_db()
    storage.archive_old_tasks()
    print("Welcome! Today go choke if you no plan!!")
    print("Here are your current tasks, boss/bossress:")
    home()     
    exit()

main()
