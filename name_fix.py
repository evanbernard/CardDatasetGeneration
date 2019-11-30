import os

i = 0
for filename in os.listdir("Cards"):
    src = "Cards\\" + filename
    cardName = filename[filename.find("[")+1:filename.find("]")]
    dst = "NewCards\\" + cardName + ".jpg"
    #os.rename(src, dst)
    i += 1
