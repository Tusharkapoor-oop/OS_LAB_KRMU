import os

print("Before Fork")
print("Current PID:", os.getpid())

pid = os.fork()

if pid == 0:
    print("\nChild Process")
    print("Child PID :", os.getpid())
    print("Parent PID:", os.getppid())

else:
    os.wait()

    print("\nParent Process")
    print("Parent PID:", os.getpid())
    print("Child PID :", pid)
