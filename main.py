from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

# Create the main Tkinter window
compiler = Tk()
compiler.title('My Fantastic IDE')

# Global variable to store the path of the currently opened or saved file
file_path = ''


# Function to set the global file_path variable
def set_file_path(path):
    global file_path
    file_path = path


# Function to open a file and load its content into the editor
def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        # Clear the editor and insert the code
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        # Set the file path
        set_file_path(path)


# Function to save the code either as a new file or overwrite the existing file
def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        # Write the code to the file
        file.write(code)
        # Set the file path
        set_file_path(path)


# Function to run the Python script and display the output in the code_output Text widget
def run():
    if file_path == '':
        # If the file is not saved, show a prompt
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        return
    # Build the command to run the Python script
    command = f'python {file_path}'
    # Execute the command using subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # Capture the output and error
    output, error = process.communicate()
    # Display the output and error in the code_output Text widget
    code_output.insert('1.0', output)
    code_output.insert('1.0', error)


# Create the menu bar
menu_bar = Menu(compiler)

# Create the File menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

# Create the Run menu
run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

# Configure the menu bar for the Tkinter window
compiler.config(menu=menu_bar)

# Create the editor Text widget for code input
editor = Text()
editor.pack()

# Create the code_output Text widget for displaying code output
code_output = Text(height=10)
code_output.pack()

# Start the Tkinter event loop
compiler.mainloop()
