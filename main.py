from meme import *

import pdb

try:
    mc  = Compiler.build()

    mc.ingest(100)

    print("done")
except KeyboardInterrupt:
    exit()
