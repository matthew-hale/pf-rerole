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

## Versioning philosophy

Although this project uses a MAJOR.MINOR.PATCH-style version number, I do not subscribe to the use of "semantic versioning." I _do_ believe that communicating what's changing with a version number change is important, and in this, I am in alignment with the semantic versioning project; however, I think that things tend to end up being much more subjective in practice than a pure semantic version number can perfectly capture.

With that in mind, the following is my subjective versioning philosophy:

MAJOR changes indicate a subjectively "large" change in the overall functionality of the project. This can include additions of wide swaths of functionality, brand-new APIs and whole paradigms in the library, new or reworked interfaces, etc. Sometimes, there might be breaking changes; sometimes, there might not be.

When you see a MAJOR change, you should think "new web interface," "completely reworked APIs for managing spells," "integration with external databases for sourcing feats," etc. Incrementing the MAJOR version number should be obviously appropriate from the perspective of a user, whether that be an end user of the web app, or a developer using the library.

MINOR changes indicate, well, "minor" changes. A fresh coat of paint on the interface; a couple of new API endpoints or library functions/namespaces; small tweaks to behavior here and there.

There is some fuzzy overlap between MAJOR and MINOR changes. That is because to me, the primary difference between the two is the _scale_ or _scope_ of the changes. A breaking change to a single function is not really "major," in my mind. Likewise, small additions to the functionality of entire categories or sections of the project are not really "minor." The more things change, in both scope and scale, the more likely I am to increment the MAJOR version number.

Finally, PATCH changes are basically used for bug fixes and non-functional, unnoticeable, internal-only changes. The user is not getting anything "new" with a PATCH change, other than a possible return to intended behavior.
