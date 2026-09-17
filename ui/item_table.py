import customtkinter as ctk


class ItemTable(ctk.CTkFrame):

    def __init__(self, master, on_change=None):
        super().__init__(master)

        self.on_change = on_change
        self.rows = []

        title = ctk.CTkLabel(
            self,
            text="Quotation Items",
            font=("Arial", 18, "bold")
        )
        title.pack(anchor="w", padx=10, pady=(10, 5))

        # ---------------- Header ----------------

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10)

        columns = [
            ("Sl", 40),
            ("Description", 330),
            ("Qty", 70),
            ("Rate", 100),
            ("Total", 100),
            ("", 80)
        ]

        for text, width in columns:
            ctk.CTkLabel(
                header,
                text=text,
                width=width,
                anchor="w",
                font=("Arial", 14, "bold")
            ).pack(side="left", padx=5)

        self.rows_frame = ctk.CTkFrame(self)
        self.rows_frame.pack(fill="x", padx=10, pady=10)

        add_btn = ctk.CTkButton(
            self,
            text="+ Add Item",
            command=self.add_row
        )
        add_btn.pack(anchor="w", padx=10, pady=(0, 10))

        self.add_row()

    def add_row(self):

        row_frame = ctk.CTkFrame(self.rows_frame)
        row_frame.pack(fill="x", pady=3)

        sl_label = ctk.CTkLabel(
            row_frame,
            text=str(len(self.rows) + 1),
            width=40
        )
        sl_label.pack(side="left", padx=5)

        description = ctk.CTkEntry(
            row_frame,
            width=330,
            placeholder_text="Description"
        )
        description.pack(side="left", padx=5)

        qty = ctk.CTkEntry(
            row_frame,
            width=70,
            placeholder_text="0"
        )
        qty.pack(side="left", padx=5)

        rate = ctk.CTkEntry(
            row_frame,
            width=100,
            placeholder_text="0"
        )
        rate.pack(side="left", padx=5)

        total = ctk.CTkLabel(
            row_frame,
            text="0.00",
            width=100
        )
        total.pack(side="left", padx=5)

        row = {
            "frame": row_frame,
            "sl": sl_label,
            "description": description,
            "qty": qty,
            "rate": rate,
            "total": total
        }

        qty.bind("<KeyRelease>", lambda e: self.calculate_row(row))
        rate.bind("<KeyRelease>", lambda e: self.calculate_row(row))

        def remove():

            row_frame.destroy()

            if row in self.rows:
                self.rows.remove(row)

            self.renumber_rows()
            self.notify_change()

        remove_btn = ctk.CTkButton(
            row_frame,
            text="Remove",
            width=70,
            fg_color="red",
            hover_color="#aa0000",
            command=remove
        )

        remove_btn.pack(side="left", padx=5)

        self.rows.append(row)

    def renumber_rows(self):

        for index, row in enumerate(self.rows, start=1):
            row["sl"].configure(text=str(index))

    def calculate_row(self, row):

        try:
            qty = float(row["qty"].get() or 0)
            rate = float(row["rate"].get() or 0)

            total = qty * rate

            row["total"].configure(
                text=f"{total:.2f}"
            )

        except ValueError:
            row["total"].configure(text="0.00")

        self.notify_change()

    def get_subtotal(self):

        subtotal = 0

        for row in self.rows:
            try:
                subtotal += float(row["total"].cget("text"))
            except ValueError:
                pass

        return subtotal

    def notify_change(self):

        if self.on_change:
            self.on_change()