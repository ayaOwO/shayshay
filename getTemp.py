from subprocess import run, PIPE

a = run(["vcgencmd", "measure_temp"], stdout=PIPE)
print(a.stdout.decode().split("=")[1].replace("'", " "))
