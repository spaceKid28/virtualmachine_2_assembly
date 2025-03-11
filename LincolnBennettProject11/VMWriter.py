class VMWriter:
    def __init__(self, xml_output):
        self.xml_output = xml_output
    
    def writePush(segment : str, Index : int):
        pass
    
    def writePop(Segment : str, Index : int):
        pass

    def WriteArithmetic(command : str):
        pass

    def WriteLabel(label : str):
        pass

    def WriteGoto(label : str):
        pass

    def WriteIf(label : str):
        pass

    def writeCall(name : str, nArgs : int):
        pass

    def writeFunction(name : str, nLocal : int):
        pass

    def writeReturn():
        pass

    def close():
        pass