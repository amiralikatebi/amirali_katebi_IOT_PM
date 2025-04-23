import json
import random
import os
from datetime import datetime

DATA_FILE = "data.json"
LOG_FILE = "log.txt"

# Log baraye sabte taghirat
def log_action(text):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as file:
        file.write(f"[{now}] {text}\n")


# Dastgah ha mesle light va camera va sensor dama va harekat
class Light:
    def __init__(self, name, is_on=False):
        self.name = name
        self.is_on = is_on

    def turn_on(self):
        self.is_on = True
        print(self.name, "roshan shod")

    def turn_off(self):
        self.is_on = False
        print(self.name, "khamoosh shod")

    def status(self):
        return f"{self.name} (light): {'Roshan' if self.is_on else 'Khamoosh'}"


class Camera:
    def __init__(self, name, is_on=False):
        self.name = name
        self.is_on = is_on

    def turn_on(self):
        self.is_on = True
        print(self.name, "roshan shod")

    def turn_off(self):
        self.is_on = False
        print(self.name, "khamoosh shod")

    def status(self):
        return f"{self.name} (camera): {'Roshan' if self.is_on else 'Khamoosh'}"


class Sensor:
    def __init__(self, name, sensor_type):
        self.name = name
        self.sensor_type = sensor_type

    def read_data(self):
        if self.sensor_type == "dama":
            return f"{random.randint(20, 30)}°C"
        elif self.sensor_type == "harekat":
            return random.choice(["harekat nadarad", "harekat shenasaei shod"])
        else:
            return "namaloom"

    def status(self):
        return f"{self.name} (sensor - {self.sensor_type}): {self.read_data()}"

# Control panel baraye taghirat va ezafe kardan va hazf kardan
class ControlPanel:
    def __init__(self):
        self.devices = {}
        self.load_data()

    def save_data(self):
        data = []
        for name, obj in self.devices.items():
            if isinstance(obj, Light):
                data.append({"name": name, "type": "light", "is_on": obj.is_on})
            elif isinstance(obj, Camera):
                data.append({"name": name, "type": "camera", "is_on": obj.is_on})
            elif isinstance(obj, Sensor):
                data.append({"name": name, "type": "sensor", "sensor_type": obj.sensor_type})
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                try:
                    data = json.load(f)
                    for item in data:
                        name = item["name"]
                        if item["type"] == "light":
                            self.devices[name] = Light(name, item.get("is_on", False))
                        elif item["type"] == "camera":
                            self.devices[name] = Camera(name, item.get("is_on", False))
                        elif item["type"] == "sensor":
                            self.devices[name] = Sensor(name, item.get("sensor_type", ""))
                except:
                    print("Error in reading JSON file.")

    def add(self, obj):
        self.devices[obj.name] = obj
        print(obj.name, "ezafe shod")
        log_action(f"{obj.name} ({obj.__class__.__name__}) ezafe shod")
        self.save_data()

    def remove(self, name):
        if name in self.devices:
            del self.devices[name]
            print(name, "hazf shod")
            log_action(f"{name} hazf shod")
            self.save_data()
        else:
            print("peyda nashod")

    def control(self, name, action):
        if name in self.devices:
            obj = self.devices[name]
            if hasattr(obj, 'turn_on'):
                if action == "roshan":
                    obj.turn_on()
                    log_action(f"{name} roshan shod")
                elif action == "khamoosh":
                    obj.turn_off()
                    log_action(f"{name} khamoosh shod")
                self.save_data()
            else:
                print(name, "sensor ast, nemishe kontrol kard")
        else:
            print("peyda nashod")

    def show_all(self):
        for item in self.devices.values():
            print(item.status())


# Run barname va dastorat
panel = ControlPanel()

print("="*45)
print("📌 Rahnamaye Estefade az Barname:")
print("="*45)
print("add light <esm>         --> ezafe kardan lamp")
print("add camera <esm>        --> ezafe kardan camera")
print("add sensor <esm>        --> ezafe kardan sensor (dama ya harekat)")
print("roshan <esm>            --> roshan kardan device (faghat light/camera)")
print("khamoosh <esm>          --> khamoosh kardan device")
print("hazf <esm>              --> pak kardan device ya sensor")
print("vaziyat                 --> namayesh vaziat tamami ajza")
print("khorooj                 --> khorooj az barname")
print("="*45)
print("💻 Developers </> : Ali Pilehvar & Amirali Katebi")
print("="*45)

while True:
    cmd = input(">>> ").strip().lower()

    if cmd.startswith("add "):
        parts = cmd.split()
        if len(parts) >= 3:
            kind = parts[1]
            name = " ".join(parts[2:])
            if kind == "light":
                panel.add(Light(name))
            elif kind == "camera":
                panel.add(Camera(name))
            elif kind == "sensor":
                sensor_type = input("noe sensor? (dama/harekat): ").strip().lower()
                panel.add(Sensor(name, sensor_type))
            else:
                print("noe eshtebah")
        else:
            print("dastoor kam ast")

    elif cmd.startswith("roshan "):
        name = cmd[7:]
        panel.control(name, "roshan")

    elif cmd.startswith("khamoosh "):
        name = cmd[9:]
        panel.control(name, "khamoosh")

    elif cmd.startswith("hazf "):
        name = cmd[5:]
        panel.remove(name)

    elif cmd == "vaziyat":
        panel.show_all()

    elif cmd == "khorooj":
        print("bye bye barname baste shod")
        break

    else:
        print("dastoor eshtebah ast")
#=============================================
#End of code