import pickle


with open("cfw/data/rules.list", "rb") as f:
    data = pickle.load(f)
    
print(data)