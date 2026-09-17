import customtkinter as ctk


class TotalsPanel(ctk.CTkFrame):

    def __init__(self, master, on_change=None):
        super().__init__(master)

        self.on_change = on_change

        title = ctk.CTkLabel(
            self,
            text="Quotation Summary",
            font=("Arial", 18, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # ---------------- Subtotal ----------------

        ctk.CTkLabel(
            self,
            text="Subtotal"
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.subtotal = ctk.CTkLabel(
            self,
            text="0.00",
            font=("Arial", 14, "bold")
        )
        self.subtotal.grid(row=1, column=1, sticky="e", padx=10)

        # ---------------- Discount ----------------

        ctk.CTkLabel(
            self,
            text="Discount"
        ).grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.discount = ctk.CTkEntry(
            self,
            width=120
        )
        self.discount.insert(0, "0")
        self.discount.grid(row=2, column=1, sticky="e", padx=10)

        # ---------------- Tax Type ----------------

        ctk.CTkLabel(
            self,
            text="Tax Type"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.tax_type = ctk.CTkSegmentedButton(
            self,
            values=["None", "GST", "VAT"],
            command=self.change_tax_type
        )

        self.tax_type.grid(
            row=2,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.tax_type.set("GST")

        # ---------------- GST ----------------

        self.tax_label = ctk.CTkLabel(
            self,
            text="GST (%)"
        )
        self.tax_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.gst = ctk.CTkEntry(
            self,
            width=120
        )
        self.gst.insert(0, "0")
        self.gst.grid(row=3, column=1, sticky="e", padx=10)

        # ---------------- GST Amount ----------------

        ctk.CTkLabel(
            self,
            text="GST Amount"
        ).grid(row=4, column=0, sticky="w", padx=10, pady=5)

        self.gst_amount = ctk.CTkLabel(
            self,
            text="0.00"
        )
        self.gst_amount.grid(row=4, column=1, sticky="e", padx=10)

        # ---------------- Grand Total ----------------

        ctk.CTkLabel(
            self,
            text="Grand Total",
            font=("Arial", 15, "bold")
        ).grid(row=5, column=0, sticky="w", padx=10, pady=15)

        self.grand_total = ctk.CTkLabel(
            self,
            text="0.00",
            font=("Arial", 18, "bold")
        )
        self.grand_total.grid(row=5, column=1, sticky="e", padx=10)

        # Live update
        self.discount.bind("<KeyRelease>", lambda e: self.notify())
        self.gst.bind("<KeyRelease>", lambda e: self.notify())

    def notify(self):
        if self.on_change:
            self.on_change()

    def update_totals(self, subtotal):

        try:
            discount = float(self.discount.get() or 0)
        except ValueError:
            discount = 0

        try:
            gst = float(self.gst.get() or 0)
        except ValueError:
            gst = 0

        taxable = max(0, subtotal - discount)

        gst_amount = taxable * gst / 100

        grand_total = taxable + gst_amount

        self.subtotal.configure(text=f"{subtotal:.2f}")
        self.gst_amount.configure(text=f"{gst_amount:.2f}")
        self.grand_total.configure(text=f"{grand_total:.2f}")

    def change_tax_type(self, value):

        if value == "None":

            self.tax_label.configure(text="Tax (%)")

            self.gst.configure(state="disabled")

            self.gst.delete(0, "end")
            self.gst.insert(0, "0")

        elif value == "GST":

            self.tax_label.configure(text="GST (%)")

            self.gst.configure(state="normal")

            if self.gst.get() == "0":
                self.gst.delete(0, "end")
                self.gst.insert(0, "18")

        elif value == "VAT":

            self.tax_label.configure(text="VAT (%)")

            self.gst.configure(state="normal")

            if self.gst.get() == "0":
                self.gst.delete(0, "end")
                self.gst.insert(0, "5")

        if self.on_change:
            self.on_change()    

   