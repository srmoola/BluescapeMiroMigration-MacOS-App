import tkinter as tk
import threading
import masterscript


def mainCallWrapper():
    # Show loading message and start the action in a separate thread
    call_button.pack_forget()
    loading_label.config(text="Migrating...")
    threading.Thread(target=perform_main_call).start()


def perform_main_call():
    input1_text = entry1.get()
    input2_text = entry2.get()

    try:
        masterscript.mainCall(input1_text, input2_text)
    except:
        pass

    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)

    # Clear loading message
    loading_label.config(text="")
    call_button.pack(side="top", anchor="center", pady=5)
    return


# Create the main window
root = tk.Tk()
root.title("Bluescape to Miro Migrations")
window_width = 400
window_height = 300
root.geometry(f"{window_width}x{window_height}")

# Create labels for the input fields
label1 = tk.Label(root, text="Enter Bluescape Board ID:")
label2 = tk.Label(root, text="Miro Board ID:")

# Create input fields
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)

# Create a button to call mainCall
call_button = tk.Button(root, text="Migrate", command=mainCallWrapper)

# Create a label to display the inputs
display_label = tk.Label(root, text="", font=("Helvetica", 12))

# Create a label for displaying loading message
loading_label = tk.Label(root, text="", font=("Helvetica", 12))

# Pack the labels, input fields, buttons, loading label, and label into the window
label1.pack(pady=5)
entry1.pack(pady=5)
label2.pack(pady=5)
entry2.pack(pady=5)
call_button.pack(side="top", anchor="center", pady=5)
loading_label.pack(pady=5)
display_label.pack(pady=20)

# Run the GUI event loop
root.mainloop()
