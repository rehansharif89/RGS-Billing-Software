from fileinput import filename
import os
import json
from pdb import main
import customtkinter as ctk
from PIL import Image
logo = ctk.CTkImage(
    light_image=Image.open("assets/company_logo.png"),
    dark_image=Image.open("assets/company_logo.png"),
    size=(200, 135)
)
from utils.settings import (
    get_next_quotation,
    get_business,
    save_business,
    get_logo_path,
    save_logo_path
)
from tkinter import filedialog, messagebox
from datetime import datetime

from pdf.pdf_generator import generate_pdf

from ui.item_table import ItemTable
from ui.totals_panel import TotalsPanel


class QuotationGenerator(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("RYHAN GLOBAL SOLUTIONS")
        self.geometry("1000x700")
        self.minsize(900, 600)

        self.build_ui()

    def build_ui(self):

        main = ctk.CTkScrollableFrame(self)
        main.pack(fill="both", expand=True)
        save_logo_path("")  # Reset logo path on startup

        logo = ctk.CTkImage(
            light_image=Image.open("assets/company_logo.png"),
            dark_image=Image.open("assets/company_logo.png"),
            size=(100, 100)
        )

        # ================= HEADER =================

        header = ctk.CTkFrame(main, fg_color="transparent")
        header.pack(fill="x", pady=20)

        # Logo
        logo_label = ctk.CTkLabel(
            header,
            image=logo,
            text=""
        )
        logo_label.pack(side="left", padx=(20, 20))

        # Text container
        text_frame = ctk.CTkFrame(header, fg_color="transparent")
        text_frame.pack(side="left")

        title = ctk.CTkLabel(
            text_frame,
            text="RYHAN GLOBAL SOLUTIONS",
            font=("Segoe UI", 30, "bold")
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            text_frame,
            text="Professional Quotation Management System",
            font=("Segoe UI", 17),
            text_color="red"
        )
        subtitle.pack(anchor="w")

        # ---------------- Company Logo ----------------

        logo_frame = ctk.CTkFrame(main)
        logo_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            logo_frame,
            text="Company Logo",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.logo_name = ctk.CTkLabel(
            logo_frame,
            text="No logo selected"
        )
        self.logo_name.pack(anchor="w", padx=15)

        ctk.CTkButton(
            logo_frame,
            text="Upload Logo",
            command=self.select_logo
        ).pack(anchor="w", padx=15, pady=(10, 15))

        self.logo_path = get_logo_path()

        if self.logo_path and os.path.exists(self.logo_path):
            self.logo_name.configure(
                text=os.path.basename(self.logo_path)
            )       


        # ---------------- Business ----------------

        business = ctk.CTkFrame(main)
        business.pack(fill="x", pady=10)

        ctk.CTkLabel(
            business,
            text="Business Details",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.business_name = ctk.CTkEntry(
            business,
            placeholder_text="Business Name"
        )
        self.business_name.pack(fill="x", padx=15, pady=5)

        self.business_address = ctk.CTkEntry(
            business,
            placeholder_text="Business Address"
        )
        self.business_address.pack(fill="x", padx=15, pady=5)

        self.business_phone = ctk.CTkEntry(
            business,
            placeholder_text="Phone Number"
        )
        self.business_phone.pack(fill="x", padx=15, pady=5)

        self.business_gst = ctk.CTkEntry(
            business,
            placeholder_text="GST Number"
        )
        self.business_gst.pack(fill="x", padx=15, pady=(5, 15))
        business_data = get_business()
        self.logo_path = business_data.get("logo", "")   

        self.business_name.insert(0, business_data["name"])
        self.business_address.insert(0, business_data["address"])
        self.business_phone.insert(0, business_data["phone"])
        self.business_gst.insert(0, business_data["gst"])

        # ---------------- Customer ----------------

        customer = ctk.CTkFrame(main)
        customer.pack(fill="x", pady=10)

        ctk.CTkLabel(
            customer,
            text="Customer Details",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.customer_name = ctk.CTkEntry(
            customer,
            placeholder_text="Customer Name"
        )
        self.customer_name.pack(fill="x", padx=15, pady=5)

        self.customer_address = ctk.CTkEntry(
            customer,
            placeholder_text="Customer Address"
        )
        self.customer_address.pack(fill="x", padx=15, pady=5)

        self.customer_phone = ctk.CTkEntry(
            customer,
            placeholder_text="Customer Phone"
        )
        self.customer_phone.pack(fill="x", padx=15, pady=(5, 15))

        # ---------------- Quotation ----------------

        quotation = ctk.CTkFrame(main)
        quotation.pack(fill="x", pady=10)

        ctk.CTkLabel(
            quotation,
            text="Quotation Details",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.quote_no = ctk.CTkEntry(quotation)
        self.quote_no.pack(fill="x", padx=15, pady=5)

        self.quote_no.insert(0, get_next_quotation())

        self.quote_date = ctk.CTkEntry(quotation)
        self.quote_date.insert(
            0,
            datetime.today().strftime("%d-%m-%Y")
        )
        self.quote_date.pack(fill="x", padx=15, pady=(5, 15))

        # ---------------- Items ----------------

        self.item_table = ItemTable(
            main,
            on_change=self.update_totals
        )
        self.item_table.pack(fill="x", pady=10)

        # ---------------- Totals ----------------

        self.totals = TotalsPanel(
            main,
            on_change=self.update_totals
        )
        self.totals.pack(fill="x", pady=10)

        # Show initial totals
        self.update_totals()

                # ---------------- Terms ----------------

        terms_frame = ctk.CTkFrame(main)
        terms_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            terms_frame,
            text="Terms & Conditions",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.terms = ctk.CTkTextbox(
            terms_frame,
            height=120
        )
        self.terms.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        self.terms.insert(
            "1.0",
            """1. Goods once sold cannot be returned.

2. Payment due within 7 days.

3. Prices are valid for 15 days."""
        )

     
        # ---------------- Buttons ----------------

        buttons = ctk.CTkFrame(main)
        buttons.pack(fill="x", pady=20)

        ctk.CTkButton(
            buttons,
            text="New Quotation",
            command=self.clear_form
        ).pack(side="left", padx=20, pady=15)

        ctk.CTkButton(
            buttons,
            text="Generate PDF",
            command=self.generate_pdf_file
        ).pack(side="right", padx=20, pady=15)
            # ---------------- Totals ----------------

    def update_totals(self):

        subtotal = self.item_table.get_subtotal()
        self.totals.update_totals(subtotal)

    # ---------------- Items ----------------

    def get_items(self):

        items = []

        for row in self.item_table.rows:

            description = row["description"].get().strip()

            # Skip completely empty rows
            if description == "":
                continue

            items.append({
                "sl": row["sl"].cget("text"),
                "description": description,
                "qty": row["qty"].get(),
                "rate": row["rate"].get(),
                "total": row["total"].cget("text")
            })

        return items

    # ---------------- PDF ----------------

    def generate_pdf_file(self):

        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=self.quote_no.get()
        )

        if not filename:
            return

        data = {
            "business_name": self.business_name.get(),
            "business_address": self.business_address.get(),
            "business_phone": self.business_phone.get(),
            "business_gst": self.business_gst.get(),
            "logo": self.logo_path,

            "customer_name": self.customer_name.get(),
            "customer_address": self.customer_address.get(),
            "customer_phone": self.customer_phone.get(),

            "quote_no": self.quote_no.get(),
            "quote_date": self.quote_date.get(),

            "items": self.get_items(),

            "subtotal": self.totals.subtotal.cget("text"),
            "discount": self.totals.discount.get(),
            "tax_type": self.totals.tax_type.get(),
            "gst_amount": self.totals.gst_amount.cget("text"),
            "grand_total": self.totals.grand_total.cget("text"),

            "terms": self.terms.get("1.0", "end").strip()
        }

        try:
            save_business(
                self.business_name.get(),
                self.business_address.get(),
                self.business_phone.get(),
                self.business_gst.get(),
                self.logo_path
            )
            generate_pdf(data, filename)

            messagebox.showinfo(
                "Success",
                "Quotation PDF generated successfully!"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def clear_form(self):

        # Generate a new quotation number
        self.quote_no.delete(0, "end")
        self.quote_no.insert(0, get_next_quotation())

        # Today's date
        self.quote_date.delete(0, "end")
        self.quote_date.insert(
            0,
            datetime.today().strftime("%d-%m-%Y")
        )

        # Clear customer details
        self.customer_name.delete(0, "end")
        self.customer_address.delete(0, "end")
        self.customer_phone.delete(0, "end")

        # Reset terms
        self.terms.delete("1.0", "end")
        self.terms.insert(
            "1.0",
            """1. Goods once sold cannot be returned.

2. Payment due within 7 days.

3. Prices are valid for 15 days."""
        )

        # Remove all item rows
        for row in self.item_table.rows[:]:
            row["frame"].destroy()

        self.item_table.rows.clear()

        # Add one empty row
        self.item_table.add_row()

        # Update totals
        self.update_totals()

    def select_logo(self):

        file = filedialog.askopenfilename(
            title="Select Logo",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg")
            ]
        )

        if file:
            self.logo_path = file 

            save_business(
                self.business_name.get(),
                self.business_address.get(),
                self.business_phone.get(),
                self.business_gst.get(),
                self.logo_path
            )   
      