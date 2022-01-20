from inspect import currentframe, getframeinfo

def a(): 
    frameinfo = getframeinfo(currentframe())
    print(frameinfo.filename, frameinfo.lineno, frameinfo.function)

a()