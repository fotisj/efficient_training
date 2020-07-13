"""
Converts TEI version of the Droc corpus to a simplified version of Conll 2003
"""

import argparse
from xml.sax import make_parser, handler
from pathlib import Path

class TEI2Conll(handler.ContentHandler):
    def __init__(self):
        self.current_content = ""
        self.content = ""
        self.APP = False
        self.PPN = False
        
    def startDocument(self):
        self.current_content = ""
        self.content = ""
        
    
    def startElement(self, name, attrs):
        if name == 'persName':
            if 'AppTdfW' in attrs.values():
                self.APP = True
            elif 'Core' in attrs.values():
                self.PPN = True
        if name == 'w':
            self.current_content = ""
        
    def endElement(self, name):
        if name == 'w':
            self.content += self.current_content+'\t'
            if self.APP:
                self.content += 'APP\n'
            elif self.PPN:
                self.content += 'PER\n'          
            else:
                self.content += 'O\n'
    
        elif name == 'persName':
            if self.APP:            
                self.APP = False            
            elif self.PPN:
                self.PPN = False                

    def characters(self, content):
        self.current_content += content

        
    def get_content(self):
        return self.content


def fix_name(name):
    return name[:-15] + 'tsv'


def convert(data_dir, target_dir):
    parser = make_parser()
    tei2conll = TEI2Conll()
    parser.setContentHandler(tei2conll)

    for filename in data_dir.glob('*.xml'):
        parser.parse(f'{filename}')
        with open(target_dir / fix_name(filename.name), 'w') as fout:
            fout.write(tei2conll.get_content())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', type=str, help="directory containing the xml files")
    parser.add_argument('target_dir', type=str, help="directory where to write the conll files")
    args = parser.parse_args()
    convert(Path(args.data_dir), Path(args.target_dir))    
    

if __name__ == '__main__':
    main()

