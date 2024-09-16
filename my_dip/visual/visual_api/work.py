import sys
import FreeCAD as App
import BOLTS as bolts
import Mesh

arg1 = sys.argv[2]
arg2 = sys.argv[3]
arg3 = sys.argv[4]

doc = App.newDocument()
doc.FileName = "test.FCStd"
bolts.add_part_by_classid(arg1, {arg2: arg3})
__objs__=[]
__objs__.append(App.ActiveDocument.getObject("BOLTS_part"))
Mesh.export(__objs__,u"/home/vadim/diplom2024/my_dip/visual/media/detail.stl")
del __objs__

