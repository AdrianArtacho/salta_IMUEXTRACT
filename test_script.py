# File: imuextract/test_script.py

def main(arg1, arg2="argumento2"):
    print(f"Positional argument: {arg1}")
    print(f"Optional argument: {arg2}")

if __name__ == "__main__":
    import sys
    arg1 = sys.argv[1] if len(sys.argv) > 1 else None
    arg2 = sys.argv[2] if len(sys.argv) > 2 else "argumento2"
    main(arg1, arg2)
