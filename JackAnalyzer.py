import sys
import os
import CompilationEngine

def main(dir):
    if os.path.isfile(dir):
        f = open(dir, 'r')
        out = dir[:-4] + "xml"
        out_file = open(out, 'w')
        generateXML(f, out_file)
    else:
        for p in os.listdir(dir):
            if p.endswith(".jack"):
                f = open(os.path.join(dir,p), 'r')
                out = p[:-4] + "xml"
                out_file = open(out, 'w')
                generateXML(f, out_file)

def generateXML(in_file, out_file):
    compilationEngine = CompilationEngine.CompilationEngine(in_file, out_file)
    compilationEngine.compileClass()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("enter file dir / only dir")
        exit(0)
    main(sys.argv[1])
