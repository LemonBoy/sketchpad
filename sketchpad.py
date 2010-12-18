import sys, os, struct

class SketchParser():
    _elements = []
    _data = []
    
    def isInt(self, s):
        try:
            dummy = int(s)
        except:
            return 0
        return 1
    
    def getSketchReport (self):
        report = ''
        for item in self._data:
            report += '0x%08x : %s : %s\n' % (item[0], item[1], item[2])
        return report
    
    def __init__(self, sketchfile, fp):
        line_count = 1
        
        for line in sketchfile.readlines():
            if len(line) == 1:
                continue
            if line.replace(' ', '')[0] == '@':
                continue
            try:
                chunks = line.replace('\n', '').split(':')
                self._elements.append([chunks[0].replace(' ', ''), chunks[1].replace(' ', ''), chunks[2].replace(' ', ''), line_count])
                line_count += 1
            except:
                print 'Error when parsing line %i, make sure the format is <arg1> : <arg2> : <arg3>' % line_count
                sys.exit(1)
            
        found = False
        
        for element in self._elements:
            if element[0].lower() == 'seekto':
                if not self.isInt(element[2]):
                    print 'Invalid numeric constant @ line %i' % element[3]
                    sys.exit(1)
                if not self.isInt(element[1]):
                    for item in self._data:
                        if item[1] == element[1]:
                            if not self.isInt(item[2]):
                                print 'Seek to non numeric-field print @ line %i' % element[3]
                                sys.exit(1)
                            else:
                                found = True
                                fp.seek(int(item[2]), int(element[2]))
                    if not found:
                        print 'Unknown label %s' % element[1]
                        sys.exit(1)
                else:
                    fp.seek(int(element[1]), int(element[2]))
            elif element[0].lower() == 'bytearr':
                if not self.isInt(element[1]):
                    print 'Invalid numeric constant @ line %i' % element[3]
                    sys.exit(1)
                self._data.append([fp.tell(), element[2], '{' + ', '.join("%02x" % ord(c) for c in fp.read(int(element[1]))) + '}'])
            elif element[0].lower() == 'string':
                if not self.isInt(element[1]):
                    print 'Invalid numeric constant @ line %i' % element[3]      
                    sys.exit(1)    
                self._data.append([fp.tell(), element[2], fp.read(int(element[1]))])
            else:
                if element[0].lower() == 'byte':
                    unpack_str = 'B'
                    unpack_size = 1
                elif element[0].lower() == 'hword':
                    unpack_str = 'H'
                    unpack_size = 2
                elif element[0].lower() == 'word':
                    unpack_str = 'I'
                    unpack_size = 4
                elif element[0].lower() == 'dword':
                    unpack_str = 'Q'
                    unpack_size = 8                    
                else:
                    print 'Unsupported type @ line %i' % element[3]
                    sys.exit(1)
                    
                if element[1].lower() == 'be':
                    unpack_str = '<' + unpack_str
                elif element[1].lower() == 'le':
                    unpack_str = '>' + unpack_str
                else:
                    print 'Unsupported endianness @ line %i' % element[3]
                    sys.exit(1)
                           
                self._data.append([fp.tell(), element[2], struct.unpack(unpack_str, fp.read(unpack_size))[0]])

if __name__ == '__main__':
    print 'Sketchpad 0.1'
    print 'The Lemon Man (C) 2010'
    
    if len(sys.argv) != 3:
        print 'Usage:\n\t%s <sketch file> <file>' % sys.argv[0]
        sys.exit(1)
        
    print 'Analyzing file %s with sketch %s' % (sys.argv[2], sys.argv[1])
    
    print '%s' % SketchParser(open(sys.argv[1]), open(sys.argv[2])).getSketchReport()
