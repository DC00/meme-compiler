from meme import *

import pdb

try:
    mc  = Compiler.build()

    mc.download(1)

    print("done")
except KeyboardInterrupt:
    exit()
