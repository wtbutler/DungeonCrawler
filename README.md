# DungeonCrawler
A simple text-adventure game I've been working on from scratch.

Required Libraries:
 * Tkinter
 * Pickle
 * Pillow

To install, just have Python 3.6, clone the repo, and checkout the Items branch. Then you should be able to run `filethatruns.py` and it should work.

I'd actually made a lot more progress, but then I saw a better way to structure the whole thing, and I had to redesign the entire movement engine based on that. I am still working on that. That is why there is a ton more stuff in the code than actually works right now.

**This is the list of things that existed that need changing**  
There are a lot of bugs:
  * Monsters needs to be transferred to new method of movement.
  * Attacking needs to be area based instead of target based.

**This is the list of things I plan to add**
 * Items in general
 * Randomly generating monsters(definately) and maps(?)
 * An actual storyline, instead of just debugging feedback
 * Whatever else I thing of! ¯\\_(ツ)_/¯

I work on this in my spare time, so any updates will be sporadic at best.

I am working in the Items branch for now, but hopefully this will change once I actually figure out how I want the tile structure to go.

**Update Log**
 * walking is fixed!
 * DOORS ARE FIXED! *(that was more because I was glad to be done than any kind of pride)*
 * Save/Load functionality still exists, just added a bugfix
