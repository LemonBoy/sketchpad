import sys, os, struct, string

class SketchParser():
    TYPE_ARR = 1
    TYPE_STR = 2
    TYPE_HEX = 3
    
    _data = []
    
    def isInt (self, s):
        try:
            dummy = int(s)
        except:
            return False
        return True
    
    def expandConstant (self, s):
        if not self.isInt(s):
            if self.loop_current != -1:
                s = s.replace('{loop}', '%i' % self.loop_current)
            for item in self._data:
                if item[0] == s:
                    return int(item[1])
            self._parserDie('Lookup of constant "%s" failed' % s)
        else:
            return int(s)
    
    def getSketchReport (self):
        report = ''
        for item in self._data:                
            if item[2] == self.TYPE_ARR:
                report += '%s : %s\n' % (item[0], self._formatArray(item[1]))
            elif item[2] == self.TYPE_STR:
                report += '%s : "%s"\n' % (item[0], item[1])
            else:
                report += '%s : 0x%08x\n' % (item[0], item[1])
                
        return report
        
    def _formatArray (self, array):
        return '{' + ', '.join("0x%02x" % ord(c) for c in array) + '}'
        
    def _parserDie (self, error):
        print '%s @ line %i' % (error, self.line_count + 1)
        sys.exit(1)
    
    def __init__(self, sketchfile, fp):
        self.line_count = 0
        
        sketch_lines = sketchfile.readlines()
        
        self.loop_start = self.loop_times = self.loop_current = -1

        while self.line_count < len(sketch_lines):
            # Skip the lines starting with a @
            if sketch_lines[self.line_count].strip(' ')[0] == '@' or \
               sketch_lines[self.line_count].strip(' ')[0] == '\n' or \
               sketch_lines[self.line_count].strip(' ')[0] == '\r':
                self.line_count += 1
                continue
                
            # Split the lines
            try:
                chunks = sketch_lines[self.line_count].replace('\n', '').split(':')
            except:
                self._parserDie('Wrong entry format')
                
            # Clean the chunks
            for i in range(len(chunks)):
                chunks[i] = chunks[i].strip(' ').lower()
                
            if chunks[0] == 'loop':
                if self.loop_current != -1 or self.loop_times != -1:
                    self._parserDie('Nested loop detected')
                        
                self.loop_start = self.line_count
                self.loop_times = self.expandConstant(chunks[1])
                self.loop_current = 1
            elif chunks[0] == 'repeat':
                if self.loop_times < 0:
                    self._parserDie('loop:end outside a loop')
                if self.loop_current < self.loop_times:
                    # We are inside a loop, increment the counter and restart
                    self.loop_current += 1
                    self.line_count = self.loop_start
                else:
                    # The loop is finished, reset the counters
                    self.loop_current = -1
                    self.loop_times = -1

            elif chunks[0] == 'seekto':
                if not self.isInt(chunks[2]):
                    self._parserDie('Incorrect whence parameter')

                seek_pos = self.expandConstant(chunks[1])
                
                fp.seek(seek_pos, int(chunks[2]))
                
            elif chunks[0] == 'bytearr':
                if self.loop_current != -1:
                    chunks[2] += '_loop_%i' % self.loop_current
                
                array_lenght = self.expandConstant(chunks[1])
                self._data.append([chunks[2], fp.read(array_lenght), self.TYPE_ARR])
                
            elif chunks[0] == 'string':
                if self.loop_current != -1:
                    chunks[2] += '_loop_%i' % self.loop_current
                    
                string = ''
                
                if chunks[1] == 'uz':
                    while 1:
                        c = fp.read(1)
                        fp.seek(1, 1) # Skip the second byte
                        string += c
                        if ord(c) == 0:
                            break
                elif chunks[1] == 'z':
                    while 1:
                        c = fp.read(1)
                        string += c
                        if ord(c) == 0:
                            break
                else:
                    string_lenght = self.expandConstant(chunks[1])
                    string = fp.read(string_lenght)
                
                self._data.append([chunks[2], string, self.TYPE_STR])
                
            else:
                if chunks[0] == 'byte':
                    unpack_str = 'B'
                    unpack_size = 1
                elif chunks[0] == 'hword':
                    unpack_str = 'H'
                    unpack_size = 2
                elif chunks[0] == 'word':
                    unpack_str = 'I'
                    unpack_size = 4
                elif chunks[0] == 'dword':
                    unpack_str = 'Q'
                    unpack_size = 8                    
                else:
                    self._parserDie('Incorrect type parameter')
                    
                if chunks[1].lower() == 'be':
                    unpack_str = '<' + unpack_str
                elif chunks[1].lower() == 'le':
                    unpack_str = '>' + unpack_str
                else:
                    self._parserDie('Incorrect endianness parameter')
                        
                if self.loop_current != -1:
                    chunks[2] += '_loop_%i' % self.loop_current
                    
                self._data.append([chunks[2], struct.unpack(unpack_str, fp.read(unpack_size))[0], self.TYPE_HEX])
                
            self.line_count += 1

if __name__ == '__main__':
    print 'Sketchpad 0.2'
    print 'The Lemon Man (C) 2010'
    
    if len(sys.argv) != 3:
        print 'Usage:\n\t%s <sketch file> <file>' % sys.argv[0]
        sys.exit(1)
        
    print 'Analyzing file %s with sketch %s' % (sys.argv[2], sys.argv[1])
    print '%s' % SketchParser(open(sys.argv[1]), open(sys.argv[2])).getSketchReport()
