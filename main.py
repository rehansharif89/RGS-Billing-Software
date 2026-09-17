import customtkinter as ctk
from ui.quotation_form import QuotationGenerator

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = QuotationGenerator()
app.mainloop()