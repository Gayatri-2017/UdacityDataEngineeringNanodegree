import configparser
import ast
# Below code is working
config = configparser.RawConfigParser()
config.read('config.cfg')
    
details_dict = dict(config.items('geocoding_mapping'))
x = ast.literal_eval(details_dict["column_list"])
print(x)
