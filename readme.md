Sketchpad
=========

The Lemon Man (C) 2010

An useful tool when you just need to focus on reversing a file format
instead of writing a parser. You can quickly and easily write a sketch
file that describes the file structure and you'll get infos from the
file using the structure you just sketched.

Documentation
-------------
    
You can write comments in newlines by putting @ as first char.

Structure field descriptions are made in this way :

    <data type> : <endianness> : <name>
    
Where <data type> it's one of the supported types for reading, listed 
below.

    byte   - 8bit
    hword  - 16bit
    word   - 32bit
    dword  - 64bit
    
The <endianness> field specifies the field endianness and can assume one
of the following values:

    be     - Big Endian
    le     - Little Endian
    
There's a special notation for the 'string' data type, it's the same as 
above but instead of the endianness holds the string lenght.

Eg. 
    string : <lenght> : <name>
    
Same goes for the 'bytearr' data type, where the second field holds the
array size.

Eg.
    bytearr : <lenght> : <name>
    
A seeking function is implemented too and can be called as follows:

    seekto : <offset or field name> : <whence>
    
You can specify a fixed offset or a structure field name (that has been
already parsed). The whence field works as it does for any programming
language, 0 means the offset is absolute, 1 means that the offset is 
relative to the current position and 2 means that the offset is relative
to the end of file.

See the included pbp.sketch for an example of a sketch file.

Todo
----

Looping support (?)
Clean up some parts (?)
