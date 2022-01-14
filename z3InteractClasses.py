import subprocess
import os

class z3Runner ():
    INOUTDIRNAME = "InOut"
    def __init__(self, fileName, outFileName, defaultFile=None, storeInOut=False):
        #Check filenames
        if fileName[-4:] != ".smt":
            print("Input filename must end with '.smt'")
            exit()
        self.fileName = fileName

        if outFileName[-4:] != ".txt":
            print("Output filename must end with '.txt'")
            exit()
        self.outFileName = outFileName

        if defaultFile != None:
            self.defaultText = self.readDefaultFile(defaultFile)

        self.storeInOut = storeInOut
        self.InOutCounter = 0
        if self.storeInOut:
            try: 
                os.mkdir(os.path.join(os.getcwd(), self.INOUTDIRNAME)) 
            except OSError as e: 
                print(e)  

    def readDefaultFile(self, defaultFile):
        with open (defaultFile, 'r') as df:
            textList = [t for t in df.read().replace("$\n", "$").split("$") if len(t) != 0]
        return textList

    def getTextBlock(self, textBlockID):
        return self.defaultText[textBlockID]

    def runz3(self, inputText):
        with open (self.fileName, 'w') as f:
            f.write(inputText)
        
        try:
            sp = subprocess.run(f'z3 {self.fileName}', shell=True, capture_output=True, text=True)
        except Exception as e:
            print(e)
            exit()

        if self.storeInOut:
            with open (os.path.join(self.INOUTDIRNAME, f'InOut_{self.InOutCounter}.txt'), "w") as f:
                f.write(inputText)
                f.write("\n\n$$$$$$$$$$$$$$$\n\n")
                f.write(sp.stdout)
                self.InOutCounter = self.InOutCounter + 1

        if 'unsat' in sp.stdout:
            return False
        elif sp.returncode != 0:
            print("z3 encountered an error, but he stupid")
            print(sp)
            print(sp.stdout)
            return False
        
        with open (self.outFileName, 'w') as f:
            f.write(sp.stdout)

        return True

#testing
if __name__ == "__main__":
    test = z3Runner("temp.smt", "out.txt", "default.txt")
    test.runz3("(declare-const a Int) (assert (and (= a 4) (= a 5)))\n(check-sat)(get-model)")