from model.fermata import Fermata
from model.modello import Model

m = Model() #chiama il modello --> ma poi devi chiamare il grafo
m.buildGraph()
print(f"Num nodi: {m.getNumNodi()}") #select count(*) from fermata f
print(f"Num archi: {m.getNumArchi()}")

f = Fermata(2,"Abbesses",2.33855,48.8843)
nodesBFS = m.getBFSnodesFromTree(f)
print("---BSF---")
for n in nodesBFS:
    print(n)

f = Fermata(2,"Abbesses",2.33855,48.8843)
nodesBFS = m.getDFSnodesFromTree(f)
print("---BDF---")
for n in nodesBFS:
    print(n)

archiMaggiori = m.getArchiPesoMaggiore()
for a in archiMaggiori:
    print(a)


