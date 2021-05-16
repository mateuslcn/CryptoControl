import pymongo
import warnings

warnings.filterwarnings('ignore')

# connect to the mongoclient
client = pymongo.MongoClient('mongodb://localhost:27017')

# get the database
database = client['Coinext_login']

# get collection weekly_demand
coinext_collection = database.get_collection("CoinextCredentials")
values = database.get_collection("Values")