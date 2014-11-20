import tempfile
import os
from shutil import rmtree

def withTempDirDo(fun,*args, **keywords):

    current = os.getcwd()
    tmpdir = tempfile.mkdtemp()

    def cleanup():
        os.chdir(current)
        rmtree(tmpdir)


    os.chdir(tmpdir)
    try:
        fun(*args, **keywords)
    except:
        cleanup()
        raise
    cleanup()
    

