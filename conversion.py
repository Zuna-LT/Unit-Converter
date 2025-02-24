import tkinter as tk
from tkinter import ttk

# Conversion Functions
def convert_length(value, from_unit, to_unit):
    conversions = {
        ('m', 'ft'): 3.28084, ('ft', 'm'): 1 / 3.28084,
        ('m', 'km'): 0.001, ('km', 'm'): 1000
    }
    return value * conversions.get((from_unit, to_unit), None)

def convert_energy(value, from_unit, to_unit):
    conversions = {
        ('j', 'wh'): 1 / 3600, ('wh', 'j'): 3600,
        ('j', 'kj'): 0.001, ('kj', 'j'): 1000
    }
    return value * conversions.get((from_unit, to_unit), None)

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'c' and to_unit == 'f': return (value * 9/5) + 32
    elif from_unit == 'f' and to_unit == 'c': return (value - 32) * 5/9
    elif from_unit == 'c' and to_unit == 'k': return value + 273.15
    elif from_unit == 'k' and to_unit == 'c': return value - 273.15
    return None

# GUI Logic
def update_units(*args):
    category = combo_category.get().lower()
    units = {
        'length': ['m', 'ft', 'km'],
        'energy': ['j', 'wh', 'kj'],
        'temperature': ['c', 'f', 'k']
    }
    new_units = units.get(category, ['m', 'ft'])
    combo_from['values'] = new_units
    combo_to['values'] = new_units
    combo_from.set(new_units[0])
    combo_to.set(new_units[1] if len(new_units) > 1 else new_units[0])

def convert():
    try:
        value = float(entry_value.get())
        from_unit = combo_from.get()
        to_unit = combo_to.get()
        category = combo_category.get().lower()
        print(f"Debug: value={value}, from={from_unit}, to={to_unit}, category={category}")
        if category == 'length':
            result = convert_length(value, from_unit, to_unit)
        elif category == 'energy':
            result = convert_energy(value, from_unit, to_unit)
        elif category == 'temperature':
            result = convert_temperature(value, from_unit, to_unit)
        else:
            result = None
        print(f"Debug: result={result}")
        if result is not None:
            new_text = f"{value} {from_unit} = {result:.2f} {to_unit}"
            result_label.config(text=new_text)
            print(f"Debug: Label set to '{new_text}'")
        else:
            result_label.config(text="Error: Invalid conversion")
            print("Debug: Label set to 'Error: Invalid conversion'")
    except ValueError:
        result_label.config(text="Error: Please enter a valid number")
        print("Debug: Label set to 'Error: Please enter a valid number'")

# GUI Setup with Scrolling
root = tk.Tk()
root.title("Unit Converter")
root.geometry("400x400")

# Create a main frame with scrollbar
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Widgets in scrollable frame
ttk.Label(scrollable_frame, text="Unit Converter", font=("Arial", 16, "bold"), background="#f0f0f0").pack(pady=10)

ttk.Label(scrollable_frame, text="Enter Value:", background="#f0f0f0").pack(pady=5)
entry_value = ttk.Entry(scrollable_frame)
entry_value.pack(pady=5)

ttk.Label(scrollable_frame, text="Category:", background="#f0f0f0").pack(pady=5)
combo_category = ttk.Combobox(scrollable_frame, values=["Length", "Energy", "Temperature"])
combo_category.pack(pady=5)
combo_category.set("Length")
combo_category.bind("<<ComboboxSelected>>", update_units)

ttk.Label(scrollable_frame, text="From Unit:", background="#f0f0f0").pack(pady=5)
combo_from = ttk.Combobox(scrollable_frame, values=['m', 'ft', 'km'])
combo_from.pack(pady=5)
combo_from.set("m")

ttk.Label(scrollable_frame, text="To Unit:", background="#f0f0f0").pack(pady=5)
combo_to = ttk.Combobox(scrollable_frame, values=['m', 'ft', 'km'])
combo_to.pack(pady=5)
combo_to.set("ft")

ttk.Button(scrollable_frame, text="Convert", command=convert).pack(pady=10)

result_label = ttk.Label(scrollable_frame, text="Result: N/A", background="#f0f0f0", font=("Arial", 12))
result_label.pack(pady=15)

root.mainloop()