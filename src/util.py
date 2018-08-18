class Options():
    def __init__(self, path):
        self.path = path
        self.options = {}
        with open(self.path, 'r') as file:
            for line in file:
                kv = line.split(':')
                key = kv[0]
                if len(kv) > 1:
                    value = kv[1]
                else:
                    value = ''
                self.options[str(key).strip()] = str(value).strip()

    def set(self, key, value):
        self.options[key] = value

    def get(self, key):
        return self.options[key]

    def save(self):
        with open(self.path, 'w') as file:
            for key in self.options:
                value = self.options[key]
                file.write(f'{key}:{value}\n')
