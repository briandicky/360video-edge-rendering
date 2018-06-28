import subprocess

for i in range(1, 51):
    copy = "cp -r template_360dataset " + "user" + str(i).zfill(2) + "_360dataset/" 
    print(copy)
    subprocess.call(copy, shell=True)
