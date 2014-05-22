import glob
from distutils.core import setup
import py2exe
DATA_FILES = []
OPTIONS = {'argv_emulation': True}

setup(
  version = "0.6.3",
  description = "Gitso is to support Others",
  name="Gitso",
  
  windows=[{"script":"Gitso.py", "icon_resources":[(1,"icon.ico")]}],
  data_files=[(".", ["icon.ico"])],
  py_modules = ['AboutWindow', 'ConnectionWindow', 'ArgsParser', 'GitsoThread', 'Processes', 'NATPMP'],
)
