import subprocess

def main():
    # Call the scrape.py script
    print("Running scrape.py...")
    subprocess.run(["python", "scrape.py"])

    # Call the download.py script
    print("Running download.py...")
    subprocess.run(["python", "download.py"])

if __name__ == "__main__":
    main()
