from meme import *

import pdb

try:
    mc  = Compiler.build()

    mc.download(1)

except KeyboardInterrupt:
    exit()
