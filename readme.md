Sketchpad 0.2b
==============

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
above but instead of the endianness holds the string length. The string
length can be either a constant, a field name or one of the following
special flags:
    
    z      - Reads until a zero char is reached
    uz     - Same as above but for Unicode

Eg. 
    string : <length> : <name>
    
Same goes for the 'bytearr' data type, where the second field holds the
array size.

Eg.
    bytearr : <length> : <name>
    
Remember that you may also use a structure field name instead of a
constant length.
    
A seeking function is implemented too and can be called as follows:

    seekto : <offset> : <whence>
    
You can specify a fixed offset or a structure field name (that has been
already parsed). The whence field works as it does for any programming
language, 0 means the offset is absolute, 1 means that the offset is 
relative to the current position and 2 means that the offset is relative
to the end of file.

As of 0.2 support to loops has been introduced. Declaring a loop is easy
as doing:

    loop : <times>
    ...
    ...
    ...
    repeat
    
and every field included between the two loop markers will be executed
<times>. The field that get parsed in the loop have the prefix '_loop_N'
appended (where N is the iteration number) for better recognizing 'em in
the resulting report. When inside a loop the parser replaces the tag

    {loop} 
    
in the field names with the current iteration number, this is meant for 
accessing indexed fields read in a loop.
See foster.sketch for an useful example.
Nested loops aren't supported.

As of 0.2b the ability of extracting chunks of the file has been added.
The syntax is:

    extract : <file name> : <amount of bytes to extract>
    
The loop prefix is added to file name if the function is called inside a
loop.

See the included pbp.sketch for an example of a simple sketch file, 
foster.sketch is a bit more complicated but shows the full potential of 
the sketchpad.

Todo
----

* Proper Unicode char handling (?)
* EOF checks (?)
* Clean up some parts (?)
