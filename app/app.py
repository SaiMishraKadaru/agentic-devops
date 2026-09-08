import os, sys, time

def main():
    print("Starting service...")
    print("Loading configuration...")
    db_host = os.environ.get("DB_HOST")
    if not db_host:
        print("ERROR: DB_HOST environment variable is not set")
        sys.exit(1)
    print(f"Connecting to database at {db_host}...")
    print("Service running.")
    print(f"DB_HOST={db_host}")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()