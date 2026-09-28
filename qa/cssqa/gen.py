import os
D=os.path.dirname(os.path.abspath(__file__))

CARD = """<li class="product-grid__item"><article class="product-card">
<a class="product-card__link" href="#">
<div class="product-card__media"><img class="product-card__image" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" alt=""></div>
<h3 class="product-card__title">%s</h3></a>
<p class="product-card__price"><span class="product-card__price-current">$1,290.00</span></p>
<div class="product-card__swatches"><span class="visually-hidden">Colour: Black, Cream</span><span class="product-card__swatch" style="--swatch-fill:#0D0C0A" aria-hidden="true"></span><span class="product-card__swatch" style="--swatch-fill:#F3EFE6" aria-hidden="true"></span></div>
</article></li>"""

TITLES=["The Faithful Oversized Hoodie","Walk By Faith Tee","Higher Purpose Cap","Movement Crewneck","Anointed Longsleeve","Grace Cargo Pant"]

def page(sid, layout, cm, ct, cd, surface, n=6):
    cards="\n".join(CARD % TITLES[i%len(TITLES)] for i in range(n))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>t</title>
<link rel="stylesheet" href="assets/design-tokens.css">
<link rel="stylesheet" href="assets/component-button.css">
<link rel="stylesheet" href="assets/component-product-card.css">
<link rel="stylesheet" href="assets/section-featured-collection.css">
<style>body{{margin:0}}.visually-hidden{{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}</style>
</head><body>
<main>
<section id="shopify-section-{sid}" class="shopify-section">
<style>
  #shopify-section-{sid} .product-grid {{ --product-cols: {cm}; }}
  @media (min-width: 768px) {{ #shopify-section-{sid} .product-grid {{ --product-cols: {ct}; }} }}
  @media (min-width: 1024px) {{ #shopify-section-{sid} .product-grid {{ --product-cols: {cd}; }} }}
</style>
<div class="featured-collection {surface} featured-collection--{layout} featured-collection--pt-standard featured-collection--pb-standard">
  <div class="featured-collection__inner">
    <div class="featured-collection__copy">
      <p class="featured-collection__eyebrow">New Drop /</p>
      <h2 class="featured-collection__heading">The Faithful</h2>
      <p class="featured-collection__description">Premium Essentials for a Higher Purpose.</p>
      <a class="featured-collection__cta button button--primary" href="#">View All Products</a>
    </div>
    <div class="featured-collection__products">
      <ul class="product-grid" role="list">
{cards}
      </ul>
    </div>
  </div>
</div>
</section>
</main></body></html>"""

open(os.path.join(D,"newdrop.html"),"w",encoding="utf-8").write(page("newdrop","with-copy-column",2,2,3,"surface-light"))
open(os.path.join(D,"best.html"),"w",encoding="utf-8").write(page("best","full-width",2,2,4,"surface-dark"))
open(os.path.join(D,"cols4mobile.html"),"w",encoding="utf-8").write(page("m1","full-width",1,3,4,"surface-light"))
print("ok")
