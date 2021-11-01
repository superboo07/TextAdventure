# Python Text Adventure

## Why I wrote this
I wrote this for a small school assignment, it was technically way more then I needed to write for said assignment. However I'd been wanting to write a text adventure engine in this language for a while now, and it technically fit the parameters of the assignment so here we are. 

## Improvements i've made since
Since the version I submitted for my assignment i've improved the strictness of the engine, and added the ability to use multiple lines in room descriptions. The TA files are not case sensitive, however the room names placed in direction blocks might be since they read from external files.

## File format

All room files must go into the `[Rootfolder]/Game/folder`, and the starting room must be named `StartingRoom.TA`. Any lines in the examples starting with an # are comments, the format itself does not have any kind of comments at the moment

### Description block
All I have to say about this block is: while the engine will *technically* accept multiple description blocks, please don't do this. 

Format:

```
Description {
    [Description goes here]
}
```

### Directions block

When typing out the file name of the room do not include the .TA extension, as the script automatically adds this itself. Any directions that have an  `!` in them will be excluded from display when the player types "Look around". 

Format:

```
Directions {
    # The direction below is not displayed in the look around prompt
    ![Direction]: [Name of file room is contained in]

    # The direction below is displayed in the look around prompt
    [Direction]: [Name of file room is contained in]
}
```

Example:

```
Directions {
    !Left: Hallway
    Hallway: Hallway
    !Right: Crawlspace1
    Crawlspace: Crawlspace1
}
```