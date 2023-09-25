import config


def extract_arg(arg):
    return arg.split()[1:]


def read_users():
    with open(config.SUBSCRIBERS, "r") as f:
        return set(int(i) for i in f.readlines())


def add_user(chat_id: int, subscribers: set):
    subscribers.add(chat_id)
    with open(config.SUBSCRIBERS, "w") as f:
        for user_id in subscribers:
            f.write(str(user_id) + "\n")
    return subscribers
