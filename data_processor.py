import pandas as pd

def compile_data_to_csv(data, filename='output.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Example usage
compile_data_to_csv(meta_data) 