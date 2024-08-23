# Versioning philosophy

Although this project uses a MAJOR.MINOR.PATCH-style version number, I do not subscribe to the use of "semantic versioning." I _do_ believe that communicating what's changing with a version number change is important, and in this, I am in alignment with the semantic versioning project; however, I think that things tend to end up being much more subjective in practice than a pure semantic version number can perfectly capture.

With that in mind, the following is my subjective versioning philosophy:

MAJOR changes indicate a subjectively "large" change in the overall functionality of the project. This can include additions of wide swaths of functionality, brand-new APIs and whole paradigms in the library, new or reworked interfaces, etc. Sometimes, there might be breaking changes; sometimes, there might not be.

When you see a MAJOR change, you should think "new web interface," "completely reworked APIs for managing spells," "integration with external databases for sourcing feats," etc. Incrementing the MAJOR version number should be obviously appropriate from the perspective of a user, whether that be an end user of the web app, or a developer using the library.

MINOR changes indicate, well, "minor" changes. A fresh coat of paint on the interface; a couple of new API endpoints or library functions/namespaces; small tweaks to behavior here and there.

There is some fuzzy overlap between MAJOR and MINOR changes. That is because to me, the primary difference between the two is the _scale_ or _scope_ of the changes. A breaking change to a single function is not really "major," in my mind. Likewise, small additions to the functionality of entire categories or sections of the project are not really "minor." The more things change, in both scope and scale, the more likely I am to increment the MAJOR version number.

Finally, PATCH changes are basically used for bug fixes and non-functional, unnoticeable, internal-only changes. The user is not getting anything "new" with a PATCH change, other than a possible return to intended behavior.
