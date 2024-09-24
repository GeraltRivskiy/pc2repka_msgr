import importlib.util
import os
import importlib
import inspect
import paho.mqtt.client as mqtt

class local_except(Exception):
    pass

class Command:
    def __init__(self, device, command_msg: str):
        self.command_msg = command_msg
        self.device = device
        split_str = self.command_msg.split()
        if len(split_str) > 0:
            self.command, *self.args = split_str
        else:
            self.command = None

    def execute(self):
        if self.command == "help":
            self.help()
        elif self.command == None:
            pass
        else:
            self.run_action()

    def help(self):
        print(f"Available commands: help, {[str(act) for act in actions.keys()]}")
        print("Usage:")
        print("  help - Show this help message")
        for action in actions.values():
            print(f"{action.__doc__} ")

    def run_action(self):
        if self.command in actions:
            action_instance = actions[self.command](self.device, *self.args)
            action_instance.execute()
        else:
            print(f"Unknown command: {self.command}")

class Action:
    def __init__(self, device, *args):
        self.device = device
        self.args = args
    def execute(self):
        raise NotImplementedError("Данный метод должен быть перезаписан в дочернем классе")

class repka:
    def __init__(self, host:str, port, keepalive=1000):
        # Connect to repka ip by mqtt
        self.client = mqtt.Client()
        on_connect = lambda client, userdata, flags, rc: print("Connected with result code "+str(rc)+"\n")
        self.client.on_connect = on_connect
        self.client.connect(host, port, keepalive)
    def publish(self,msg):
        self.client.publish("drone_actions", msg)

        

def change_args_type(func):
        def wrapper(self, *args, **kwargs):
            self.args = list(self.args)
            for i,arg in enumerate(self.args):
                try:
                    self.args[i] = float(arg)
                except:
                    print(f"Unsupported type of argument {i+1}")
                    raise local_except()
            result = func(self, *args, **kwargs)
            return result
        return wrapper

def load_actions():
    actions = {}
    actions_dir = "actions"
    for filename in os.listdir(actions_dir):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            file_path = os.path.join(actions_dir, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            classes = inspect.getmembers(module, inspect.isclass)
            for cls in classes:
                if cls[0] == module_name:
                    actions[module_name] = cls[1]
    return actions
actions =  load_actions()




def main():
    host, port = input('Введите <host> <port> для подключения\n').split()
    port = int(port)
    drone = repka(host, port)
    welcome = Command(drone, input('Введите "help" чтобы начать, Enter чтобы пропустить \n'))
    welcome.execute()
    while True:
        com = Command(drone, input('Введите команду: \n'))
        try:
            com.execute()
        except:
            continue


if __name__ == "__main__":
    main()