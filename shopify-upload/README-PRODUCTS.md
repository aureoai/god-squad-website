# Adding real products to godsquad-intl

`products-TEMPLATE.csv` is a blank import file shaped for this theme. Fill it in
and use **Products → Import** in Shopify admin.

## How the rows work

One product = **one row per size**, all sharing the same `Handle`.

The **first row** of a product carries everything: title, description, vendor,
price, image. Every row after it carries **only** the handle, the size, and that
size's own SKU, stock and price. Repeating the title on later rows creates
duplicate products.

## The columns that matter

| Column | What to put | Why |
|---|---|---|
| `Handle` | `signature-oversized-tee` | Becomes the URL. Lowercase, hyphens, no spaces. Identical on every row of one product. |
| `Title` | First row only | |
| `Body (HTML)` | First row only | Simple `<p>` paragraphs. The theme styles them. |
| `Option1 Name` | `Size` | First row only. Renders as the picker's legend, so "Size" gives you `SIZE XS`. |
| `Option1 Value` | `XS`, `S`, `M`… | **Every row.** One per size. |
| `Variant Price` | e.g. `1290` | Every row. Numbers only — no currency symbol, no comma. |
| `Variant Compare At Price` | usually **blank** | Only fill this if the item genuinely sold at that higher price. It produces the sale treatment, and a reference price you never charged is an advertising problem, not a design choice. |
| `Variant Inventory Qty` | e.g. `25` | Every row. Drives the SOLD OUT badge when it hits 0. |
| `Variant Inventory Tracker` | `shopify` | Every row, or stock is not tracked and nothing ever shows sold out. |
| `Variant SKU` | e.g. `GS-TEE-XS` | Optional but useful. Unique per size. |
| `Variant Grams` | e.g. `230` | Needed for weight-based shipping rates. |
| `Image Src` | a public URL, or leave blank | See below. |
| `Image Alt Text` | describe the photo | The theme never invents alt text. Blank means "decorative". |
| `Status` | `active` | `draft` keeps it hidden while you work. |

## Images

CSV import needs images at a **public URL**. If you have the files locally,
it is easier to import the CSV without images, then add photos on each product
in admin — Products → the product → Media.

Shoot or crop to **one shape** across the whole catalogue. `product_image_ratio`
in Theme settings is global: Square (1:1) by default, or Portrait (4:5). Mixed
shapes make the grid ragged.

## After importing — two steps people forget

1. **Publish to the Online Store channel.** On each product, the *Publishing*
   card. Without it the product appears in collection grids but its own page
   returns 404. Every sample product in this store has this problem right now.
2. **Add each product to a collection.** The homepage pins two handles,
   `new-drop` and `best-sellers`. A product in neither will not appear on the
   home page.

## Colour swatches

Circles come from Shopify, not the theme: **Settings → Products → Variants**,
where a colour or image is attached to an option value. Without that, a colour
option still works — it renders as plain buttons rather than swatches.

## Note on `products.csv`

The other CSV in this folder is **not real data**. It carries five invented
products with invented prices, stock, SKUs and compare-at prices that advertise
a discount from a price never charged. It was generated from the QA harness's
test fixtures. Do not import it.
