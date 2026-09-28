# -*- coding: utf-8 -*-
"""Phase 6: move the button system out of section-hero.css and load the shared
component from the layout instead."""

css = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\assets\section-hero.css"
lay = r"C:\Users\TEST\OneDrive\Documents\GodSquad Website\layout\theme.liquid"

s = open(css, encoding='utf-8').read()

old = """/* --------------------------------------------------------------- the button
   First use of the Phase 2 button system. It lives here because the hero is
   the only section that has one so far; promote it to a shared stylesheet as
   soon as a second section needs it, rather than duplicating it. */

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  min-height: var(--target-min);
  padding: var(--space-4) var(--space-6);
  border: var(--border-width) solid transparent;
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-size: var(--type-label-size);
  font-weight: var(--type-label-weight);
  letter-spacing: var(--type-label-ls);
  text-transform: uppercase;
  text-decoration: none;
  cursor: pointer;
  transition: background-color var(--transition-fast), color var(--transition-fast);
}

/* On the dark hero the primary action is the light one: cream ground, ink
   text. Not a pill, per Phase 2 section 10. */
.button--primary {
  background-color: var(--color-text-primary);
  color: var(--color-text-inverse);
}

.button--primary:hover {
  background-color: var(--color-accent);
  color: var(--color-text-inverse);
}

.hero__cta {
  margin-top: var(--space-7);
}"""

new = """/* --------------------------------------------------------------- the button
   The button system moved to assets/component-button.css in Phase 6, when the
   featured-collection section became its second consumer. Phase 5 section 16
   recorded that promotion as the condition for a second use, and three values
   the copy here had wrong are corrected in the shared file — the gold hover
   fill most importantly, which Phase 2 section 10.3 prohibits on a primary.
   Only the hero's own placement rule stays here. */

.hero__cta {
  margin-top: var(--space-7);
}"""

assert old in s, "button block not found in section-hero.css"
s = s.replace(old, new)

old2 = """/* ---------------------------------------------------------- reduced motion
   The hero has no entrance animation: it must be understandable without one,
   and the photography is the focus. The only transition is on the button,
   which the global reduced-motion rule in design-tokens.css already
   neutralises. This block is here so the intent is explicit. */

@media (prefers-reduced-motion: reduce) {
  .button {
    transition: none;
  }
}"""
new2 = """/* ---------------------------------------------------------- reduced motion
   The hero has no entrance animation: it must be understandable without one,
   and the photography is the focus. Nothing in this file transitions, moves or
   fades at any viewport, so there is nothing for a reduced-motion query to
   switch off. The button's own transition and its reduced-motion rule travel
   with the button, in assets/component-button.css. */"""
assert old2 in s, "reduced-motion block not found in section-hero.css"
s = s.replace(old2, new2)

open(css, 'w', encoding='utf-8', newline='').write(s)
print("section-hero.css: button system removed")

t = open(lay, encoding='utf-8').read()
oldl = """    {{ 'design-tokens.css' | asset_url | stylesheet_tag }}
    {{ 'header.css' | asset_url | stylesheet_tag }}"""
newl = """    {{ 'design-tokens.css' | asset_url | stylesheet_tag }}
    {{ 'header.css' | asset_url | stylesheet_tag }}

    {%- comment -%}
      Shared components load from the layout; section stylesheets load from
      their own section. The button system is used by the hero and by every
      collection section, so it is a component rather than a section asset.
      Phase 5 section 16 recorded the promotion; Phase 6 performed it.
    {%- endcomment -%}
    {{ 'component-button.css' | asset_url | stylesheet_tag }}"""
assert oldl in t, "stylesheet block not found in theme.liquid"
open(lay, 'w', encoding='utf-8', newline='').write(t.replace(oldl, newl))
print("theme.liquid: component-button.css loaded")
