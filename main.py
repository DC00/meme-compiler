from meme import *

import pdb

try:
    mc  = Compiler.build()

    mc.download(5)

    print("done")
except KeyboardInterrupt:
    exit()
