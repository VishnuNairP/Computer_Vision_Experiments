import os
print("This python script installs the following packages:\n")
fileObj = open("requirements.txt","r")
print(fileObj.read())
ch = input("Do you wish to continue?(Y/N): ")
if ch == 'Y' or 'y':
    os.system("pip install -r requirements.txt")
else:
    print("Aborted!")