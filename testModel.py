from model.modello import Model

m = Model() #chiama il modello --> ma poi devi chiamare il grafo
m.buildGraph()
print(f"Num nodi: {m.getNumNodi()}") #select count(*) from fermata f
print(f"Num archi: {m.getNumArchi()}")
