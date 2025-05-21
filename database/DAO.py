from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():

        conn = DBConnect.get_connection()
        ris = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            ris.append(Fermata(**row)) #oggetti di tipo fermata
        cursor.close()
        conn.close()
        return ris

    #-----------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def hasConnessione(nodo1: Fermata, nodo2: Fermata):

        conn = DBConnect.get_connection()
        ris = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                from connessione c
                where c.id_stazP = %s
                and c.id_stazA = %s"""

        cursor.execute(query, (nodo1.id_fermata, nodo2.id_fermata))

        for row in cursor:
            ris.append(row)  #qui non ci interessa

        cursor.close()
        conn.close()
        return len(ris) > 0 #True: se è maggiore di zero

    # -----------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getVicini(nodo: Fermata):

        conn = DBConnect.get_connection()
        ris = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                   from connessione c
                   where c.id_stazP = %s"""

        cursor.execute(query, (nodo.id_fermata,))

        for row in cursor:
            ris.append( Connessione(**row))  # oggetti connessione

        cursor.close()
        conn.close()
        return ris

    # -----------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllArchi():

        conn = DBConnect.get_connection()
        ris = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                   from connessione c"""

        cursor.execute(query)

        for row in cursor:
            ris.append(Connessione(**row))  # oggetti connessione

        cursor.close()
        conn.close()
        return ris

    # -----------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllEdgesPesati():

        conn = DBConnect.get_connection()
        ris = []

        cursor = conn.cursor(dictionary=True)
        query = """select id_stazP, id_stazA , count(*) as n
                   from connessione c
                   group by id_stazP, id_stazA 
                   order by n desc"""

        cursor.execute(query)

        for row in cursor:
            ris.append(( row["id_stazP"], row["id_stazA"], row["n"]))  #tupla

        cursor.close()
        conn.close()
        return ris

    # -----------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllEdgesVelocita():

        conn = DBConnect.get_connection()
        ris = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.id_stazP, c.id_stazA, max(l.velocita) as velocita
                   from connessione c , linea l 
                   where c.id_linea = l.id_linea
                   group by c.id_stazP, c.id_stazA 
                   order by c.id_stazP asc , c.id_stazA asc"""

        cursor.execute(query)

        for row in cursor:
            ris.append((row["id_stazP"], row["id_stazA"], row["velocita"]))  # tupla

        cursor.close()
        conn.close()
        return ris