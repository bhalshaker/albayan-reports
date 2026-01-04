# Creating Templates in LibreOffice Writer (ODT Format)

This guide intends to explain how to design reusable templates in **LibreOffice Writer**. Templates allow you to standardize documents with variables, placeholders, dynamic images, and tables. All templates should be saved in **ODT format**.

---

## 📝 Saving Templates in ODT Format

1. Open **LibreOffice Writer**.
2. Design your document with the desired layout.
3. Go to **File → Save As**.
4. Choose **ODF Text Document (.odt)** as the file type.
5. Save the file in your preferred location.

---

## 🔑 Adding Variables and Placeholders

Variables and placeholders make templates dynamic by allowing you to replace text later.

### Steps to Add Variables

1. Place your cursor where you want the variable.
2. Go to **Insert → Field → More Fields**.
3. In the **Variables** tab:
   - Select **User Field**.
   - Enter a **Name** (e.g., `CustomerName`).
   - Enter a **Value** (optional).
4. Click **Insert**.
5. The variable will appear in your document. You can update its value later via **Edit → Fields**.

### Using Unique Text Placeholders

Instead of conventional placeholders, use **unique text markers** that won’t be confused with normal content. Examples:

- `{{CustomerName}}`
- `{{InvoiceNumber}}`
- `<<Address>>`
- `"PlaceholderText"`

---

## 🖼️ Adding and Naming Dynamic Images

Dynamic images can be inserted and named for easy reference.

### Steps to Add and Name Images

1. Place your cursor where the image should appear.
2. Go to **Insert → Image → From File** and select your image.
3. Right-click the image and choose **Properties**.
4. In the **Name** field, assign a descriptive name (e.g., `LogoImage`).
5. This name can be used to reference or replace the image dynamically.

---

## 📊 Adding and Naming Tables

Tables are useful for structured data. Naming them helps with automation and referencing.

### Steps to Add and Name Tables

1. Place your cursor where the table should go.
2. Go to **Table → Insert Table**.
3. Choose the number of rows and columns.
4. Right-click the table and select **Table Properties**.
5. In the **Name** field, assign a descriptive name (e.g., `SalesDataTable`).

---

## 📑 Footer Data Placeholders in Tables

To ensure footer data placeholders are properly aligned:

1. Insert your table with headers in the first row.
2. Directly **below the header row**, insert a new row.
3. Use this row for **footer placeholders** (e.g., totals, dynamic values).

---

## ✅ Summary

- Save all templates in **ODT format**.
- Use **variables** and **placeholders** for dynamic text.
- Add **dynamic images** and assign names for easy reference.
- Insert and **name tables** for structured data.
- Place **footer placeholders** in a row immediately after the header row.

By following these steps, you can create flexible, reusable templates in LibreOffice Writer that adapt to different contexts and data inputs.
