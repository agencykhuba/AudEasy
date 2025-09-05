import pandas as pd

def audit(data):
    print("Auditing with AudEasy:", data)

if __name__ == "__main__":
    print("Welcome to AudEasy!")
    audit(pd.DataFrame({"value": [1, 2, 3]}))
