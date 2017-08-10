def handler(cb, ts, thread_id, author_id, message):
    print("New message!")
    print("From:", author_id)
    print("Thread:", thread_id)
    print(message)
    print("Time:", ts)
    if message.startswith("!"):
        cb(thread_id, message[1:])
