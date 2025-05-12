from datetime import datetime

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()

        self._idMapFermate = {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate

    #-------------------------------------------------------------------------------------------------------------------------
    def buildGraph(self):

        #aggiungiamo i nodi
        self._grafo.add_nodes_from(self._fermate)

        # tic = datetime.now()
        # self.addArchiCiclo()
        # toc = datetime.now()
        # print(f"Total time 2: {toc - tic}")

        # self._grafo.clear_edges()
        # tic = datetime.now()
        # self.addArchiSapendoSingolaFermata()
        # toc = datetime.now()
        # print(f"Total time 2: {toc - tic}")

        # self._grafo.clear_edges()
        tic = datetime.now()
        self.addAllArchi()
        toc = datetime.now()
        print(f"Total time 3: {toc-tic}")

    # 3 alternative per costruire gli archi: in base alla query otterremo diverse velocità di risoluzione
    # -------------------------------------------------------------------------------------------------------------------------
    def addArchiCiclo(self):
        """ Aggiungo gli archi con doppio ciclo sui nodi, e testando se per ogni coppia esiste una connessione"""
        for u in self._fermate:
            for v in self._fermate:
                if u != v and DAO.hasConnessione(u,v) :
                    self._grafo.add_edge(u, v)
                    print(f"Aggiungo arco fra {u} e {v}")

    def addArchiSapendoSingolaFermata(self):
        """ Ciclo solo una volta e faccio una query per trovare i vicini"""
        for fermataPartenza in self._fermate:
            for conn in DAO.getVicini(fermataPartenza): #sono sicura che ci sia almeno una connessione,
                fermataArrivo = self._idMapFermate.get(conn.id_stazA)
                self._grafo.add_edge(fermataPartenza, fermataArrivo)

    def addAllArchi(self):
        """ Query unica che prende tutti gli archi e poi ciclo qui"""
        allArchi = DAO.getAllArchi()
        for arco in allArchi:
            fPartenza = self._idMapFermate[arco.id_stazP]
            fArrico = self._idMapFermate[arco.id_stazA]
            self._grafo.add_edge(fPartenza, fArrico)

    #4 alternative per ottenere i nodi: una vale l'altra in questo caso
    # -------------------------------------------------------------------------------------------------------------------------
    def getBFSnodesFromTree(self, source):

        #Breadth-first-visit --> visita per livelli
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi[1:]

    # -------------------------------------------------------------------------------------------------------------------------
    def getDFSnodesFromTree(self, source):

        #Depth-first-visit --> visita in profindità
        tree= nx.dfs_tree(self._grafo, source)
        nodi= list(tree.nodes())
        return nodi[1:] #per togliere il nodo da cui parto

    # -------------------------------------------------------------------------------------------------------------------------
    def getBFSbodesFromEdges(self, source):

        archi = nx.bfs_edges(self._grafo, source)
        ris = []
        for nodoPartenza, a in archi:
            ris.append(a)
        return ris

    # -------------------------------------------------------------------------------------------------------------------------
    def getDFSbodesFromEdges(self, source):

        archi = nx.dfs_edges(self._grafo, source)
        ris = []
        for nodoPartenza, a in archi:
            ris.append(a)
        return ris

    # -------------------------------------------------------------------------------------------------------------------------
    def buildGraphPesato(self): #USIAMO QUESTO

        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgesPesati()

    def addEdgesPesati(self):

        self._grafo.clear_edges()
        allArchi = DAO.getAllArchi()
        for arco in allArchi:
            fPartenza = self._idMapFermate[arco.id_stazP]
            fArrico = self._idMapFermate[arco.id_stazA]

            if self._grafo.has_edge(fPartenza,fArrico):
                self._grafo[fPartenza][fArrico]["weight"] += 1
            else:
                self._grafo.add_edge(fPartenza, fArrico, weight=1)

    # -------------------------------------------------------------------------------------------------------------------------
    def addEdgesPesatiMiglioreQuery(self):

        self._grafo.clear_edges()
        allEdgesPesati = DAO.getAllEdgesPesati()
        for e in allEdgesPesati:
            self._grafo.add_edge( self._idMapFermate[e.id_stazP],
                                  self._idMapFermate[e.id_stazP],
                                  weight= e[2] )

    # -------------------------------------------------------------------------------------------------------------------------
    def getArchiPesoMaggiore(self):

        edges = self._grafo.edges(data=True) #data=True: dato che mi servono anche i pesi
        ris=[]
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"]>1:
                ris.append(e)
        print(ris)

    # -------------------------------------------------------------------------------------------------------------------------

