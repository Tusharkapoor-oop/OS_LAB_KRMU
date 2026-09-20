import os
import subprocess

TEST_FILE = "test_file.txt"
INVALID_PATH = "/root/forbidden_dir/secret.txt"
PROC_FILE = "/proc/version"      
DEV_NULL = "/dev/null"
DEV_ZERO = "/dev/zero"

def child_task():
    print("\n[CHILD] Child process started")
    print("[CHILD] Child PID  :", os.getpid())
    print("[CHILD] Parent PID :", os.getppid())

    print("\n[CHILD] Running Linux command: uname -a")
    subprocess.run(["uname", "-a"])

    print("\n[CHILD] Creating test file:", TEST_FILE)
    with open(TEST_FILE, "w") as f:
        f.write("Hello from child process\n")
        f.write("System calls demo\n")
    print("[CHILD] File written and closed.")

    with open(TEST_FILE, "r") as f:
        content = f.read()
    print("[CHILD] File content read back:")
    print(content, end="")

    print("\n[CHILD] Writing to /dev/null (should produce no output):")
    with open(DEV_NULL, "w") as f:
        f.write("This text disappears")
    print("[CHILD] /dev/null write succeeded silently.")

    print("\n[CHILD] Reading 8 bytes from /dev/zero:")
    with open(DEV_ZERO, "rb") as f:
        data = f.read(8)
    print("[CHILD] Bytes read (as integers):", list(data))

    print("\n[CHILD] Reading read-only /proc interface:", PROC_FILE)
    try:
        with open(PROC_FILE, "r") as f:
            first_line = f.readline().strip()
        print("[CHILD] /proc/version line 1:", first_line)
    except Exception as e:
        print("[CHILD] Error reading /proc file:", e)

    print("\n[CHILD] Attempting to open invalid path:", INVALID_PATH)
    try:
        with open(INVALID_PATH, "r") as f:
            f.read()
    except FileNotFoundError:
        print("[CHILD] Error: File not found ->", INVALID_PATH)
    except PermissionError:
        print("[CHILD] Error: Permission denied ->", INVALID_PATH)
    except Exception as e:
        print("[CHILD] Unexpected error:", type(e).__name__, "-", e)

    print("\n[CHILD] Child process finishing.")

def main():
    print("[PARENT] Parent process started")
    print("[PARENT] Parent PID :", os.getpid())

    pid = os.fork()

    if pid == 0:
        # Child branch
        child_task()
        os._exit(0)
    else:
        # Parent branch
        print("[PARENT] Created child with PID:", pid)

        # 3. Wait for child to complete
        _, status = os.wait()
        print("\n[PARENT] Child exited with status:", status)
        print("[PARENT] Parent process finishing.")

if __name__ == "__main__":
    main()
