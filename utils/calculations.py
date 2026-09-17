def calculate_total(rows, discount=0, gst=0):
    subtotal = 0

    for row in rows:
        try:
            qty = float(row["qty"].get() or 0)
            rate = float(row["rate"].get() or 0)

            total = qty * rate

            row["total"].configure(text=f"{total:.2f}")

            subtotal += total

        except:
            row["total"].configure(text="0.00")

    taxable = subtotal - discount

    gst_amount = taxable * gst / 100

    grand_total = taxable + gst_amount

    return (
        round(subtotal,2),
        round(gst_amount,2),
        round(grand_total,2)
    )