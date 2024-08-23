# pf-rerole

## What?

`pf-rerole` is a (web app|library|command-line tool) that automatically calculates your character's final roll modifiers based on the state of all of the effects being applied to them. It takes into account:

* Stacking rules (different bonus types, like "enhancement," "alchemical," "dodge," etc., stack in different ways)
* Magic vs extraordinary sources (for anti-magic fields, and the like)
* State (effects can be toggled on and off individually)

This project is an active work-in-progress, and is currently in a pre-alpha state. I provide no guarantees about its function, nor any guarantees to the stability of its API.

## Why?

> "As the party walks through the main double doors, you notice the expansive interior of the cathedral; the vaulted ceilings and intricately detailed stained-glass windows tower over you as you creep towards the distant rows of pews.
>
> "Walking across the thick carpet, you think you hear a faint click. At once, the massive organ at the front of the room blares to life, as a beam of bright light shines from the holy symbol in the glass above it, not only illuminating the dim interior -- but also applying an anti-magic field!"
>
> \*The entire party groans as they recalculate every single stat on their character sheets, taking into account all of their magic items, spells, and other magical effects\*

I decided to create `pf-rerole` because I got tired of this happening to me, and I couldn't find anything that solved this problem for me in the way that I liked.
