from environs import Env

env = Env()
env.read_env()

ES_URL = env("ES_URL")
