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

    #-------------------------------------------------------------------------------------------------------------------------
    def buildGraph(self):
        #aggiungiamo i nodi
        self._grafo.add_nodes_from(self._fermate)

        # tic = datetime.now()
        # self.addArchiCiclo()
        # toc = datetime.now()
        # print(f"Total time 2: {toc - tic}")
        #
        # self._grafo.clear_edges()
        # tic = datetime.now()
        # self.addArchiSapendoSingolaFermata()
        # toc = datetime.now()
        # print(f"Total time 2: {toc - tic}")
        #
        # self._grafo.clear_edges()
        tic = datetime.now()
        self.addAllArchi()
        toc = datetime.now()
        print(f"Total time 3: {toc-tic}")

    def addArchiCiclo(self):
        """ Aggiungo gli archi con doppio ciclo sui nodi, e testando se per ogni coppia esiste una connessione"""
        for u in self._fermate:
            for v in self._fermate:
                if u != v and DAO.hasConnessione(u,v) : #potresti aggiungere un controllo che guarda che u e v non siano uguali
                    self._grafo.add_edge(u, v)
                    print(f"Aggiungo arco fra {u} e {v}")

    def addArchiSapendoSingolaFermata(self):
        """ Ciclo solo una volta e faccio una query per trovare i vicini"""
        for fermataPartenza in self._fermate:
            for conn in DAO.getVicini(fermataPartenza): #sono sicura che ci sia almeno una connessione, u=stazione di partenza
                fermataArrivo = self._idMapFermate.get(conn.id_stazA)
                self._grafo.add_edge(fermataPartenza, fermataArrivo)

    def addAllArchi(self):
        """ Query unica che prende tutti gli archi e poi ciclo qui"""
        allArchi = DAO.getAllArchi()
        for arco in allArchi:
            fPartenza = self._idMapFermate[arco.id_stazP]
            fArrico = self._idMapFermate[arco.id_stazA]
            self._grafo.add_edge(fPartenza, fArrico)


    # -------------------------------------------------------------------------------------------------------------------------
    @property
    def fermate(self):
        return self._fermate