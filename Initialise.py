def install_requirements(file="requirements.txt"):
    import subprocess
    import sys

    try:
        print(f"Installing packages from {file}...\n")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file])
        print("\nAll packages installed successfully!")
    except subprocess.CalledProcessError:
        print("\n❌ Error: Failed to install packages.")
    except FileNotFoundError:
        print(f"\n❌ Error: The file '{file}' was not found.")

if __name__ == "__main__":
    install_requirements()
