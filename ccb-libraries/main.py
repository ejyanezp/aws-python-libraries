# This is for unit testing
from ccb_toolbox import ccb_global

# Fetch a Secret from the Secrets Manager
print("Get Secret")
connection_data = ccb_global.get_secret(f"/qa/sql/bcredicorp")
print(connection_data)

# Fetch a JSON Parameter from the parameter Store of the AWS Systems Manager
print("Get Parameter")
connection_data = ccb_global.get_parameters(["/dev/sql/2016/globals", "/dev/sql/2016/bcredicorp"])
print(connection_data)
