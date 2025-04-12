# Local access requirements

## Checking Prerequisites (All Systems)

###Python Installation: Open your terminal or command prompt and type:

```Bash
python --version
```
or sometimes:
```Bash
python3 --version
```
You should see the Python version printed. If not, you'll need to download and install Python from python.org. Make sure you select the option to add Python to your system's PATH during installation on Windows.

pip Installation: Pip is the package installer for Python. Check if it's installed by running:

```Bash
pip --version
```
or:
```Bash
pip3 --version
```
If pip isn't installed, you can usually install it by running the following in your terminal:

```Bash
python -m ensurepip --default-pip
```
or:
```Bash
python3 -m ensurepip --default-pip
```
If your version is 3.3 or higher, you're good to go! If not, you'll need to install a more recent Python version from python.org.
### Creating a venv Virtual Environment
Open your terminal or command prompt and navigate to the project's root directory (the folder where you want to create the virtual environment). Then, run the appropriate command for your system:
*We may need to make our individual environments in separate folders, especially if we are working on different OS's.*
*May need to monitor if we need to exclude the venvs from github uploads.*

Windows:

```cmd
python -m venv .venv
```
or
```cmd
python3 -m venv .venv
```
Linux and macOS:
```Bash
python3 -m venv .venv
```
or (if python3 isn't your default Python 3 command)
```Bash
python -m venv .venv
```
**Explanation:**

`python` or `python3`: This invokes your Python interpreter.
`-m venv`: This tells Python to run the venv module.
`.venv`: This is the name of the directory where the virtual environment will be created. The . at the beginning makes it a hidden directory on Unix-like systems (Linux and macOS), which is a common convention. You can name it something else if you prefer (e.g., env, virtualenv).
### Activating the Virtual Environment
Before you can install packages into your isolated environment, you need to activate it. Here's how:
Windows:
```cmd
.\.venv\Scripts\activate
```
Linux and macOS:
```Bash
source .venv/bin/activate
```
**Explanation:**

This command runs the activate script located within your virtual environment's directory.
Once activated, you'll see the name of your virtual environment (e.g., (.venv)) at the beginning of your terminal prompt. This indicates that any pip commands you run will now operate within this isolated environment.
### Installing Requirements from requirements.txt

Make sure your requirements.txt file is located in the root directory of your project (or provide the correct path to it). With your virtual environment activated, run the following command:

```
pip install -r requirements.txt
```
Explanation:

`pip install`: This is the command to install Python packages.
`-r requirements.txt`: This tells pip to read the list of packages and their versions from the requirements.txt file and install them in the active environment.