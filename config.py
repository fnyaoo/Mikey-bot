from pymongo import MongoClient
from environs import Env

env = Env()
env.read_env()

cluster = MongoClient(env.str("MONGO_COONECTION_LINK"))

def cluster_con():
    return cluster

settings = {
    'TOKEN': env.str("BOT_TOKEN"),
    'PREFIX':'!',
}
