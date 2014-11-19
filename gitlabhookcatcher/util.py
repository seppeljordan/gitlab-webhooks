import tempfile
import os

def withTempDirDo(fun,*args, **keywords):
    current = os.getcwd()
    tmpdir = mkdtemp()
    os.chdir(tmpdir)
    fun(args, keywords)
    os.chdir(current)
    shutil.rmtree(tmpdir)
    

