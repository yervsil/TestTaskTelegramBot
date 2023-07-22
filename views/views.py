class TodoBotView:
    @staticmethod
    def welcome_message():
        return "Привет! Я тестовый ToDo-бот. Вот доступные команды:\n\n" \
               "/start - Вывести это приветственное сообщение и доступные команды\n" \
               "/add <задача> - Добавить новую задачу в список\n" \
               "/done <индекс> - Отметить задачу с указанным индексом как выполненную\n" \
               "/list - Вывести список всех задач с их статусами\n" \
               "/delete <индекс> - Удалить задачу с указанным индексом из списка"

    @staticmethod
    def list_tasks(tasks):
        if not tasks:
            return "Список задач пуст."
        result = "Список задач:\n"
        for index, task in enumerate(tasks, start=1):
            status = "✓" if task[3] else "❌"
            result += f"{index}. {status} {task[2]}\n"
        return result

