import os


class env_file(object):
    lines = None
    env_dict = dict()

    def __init__(self, env_file):
        with open(env_file, "r") as e:
            self.lines = e.readlines()

            for line in self.lines:
                key, value = line.split("=")
                self.env_dict[key.strip()] = value.strip()

    def load(self):
        for key, value in self.env_dict.items():
            os.environ[key] = value
