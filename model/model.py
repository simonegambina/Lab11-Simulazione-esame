import networkx as nx

from database.DAO import DAO
from model.Artist import Artist


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodes = []

    def buildGraphP(self, genre):
        self._grafo.clear()

        self._nodes = DAO.getNodes(genre)
        self._grafo.add_nodes_from(self._nodes)

        edges = DAO.getEdges(genre)

        for row in edges:
            artistA = Artist(row["ArtistIdA"], row["NameA"])
            artistB = Artist(row["ArtistIdB"], row["NameB"])

            popA = row["PopA"]
            popB = row["PopB"]
            peso = row["Peso"]

            if popA > popB:
                self._grafo.add_edge(artistA, artistB, weight=peso)
            elif popB > popA:
                self._grafo.add_edge(artistB, artistA, weight=peso)
            else:
                self._grafo.add_edge(artistA, artistB, weight=peso)
                self._grafo.add_edge(artistB, artistA, weight=peso)

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getArtistaPiuInfluente(self):
        best_artista = None
        best_influenza = None

        for artista in self._grafo.nodes:
            peso_uscenti = 0
            peso_entranti = 0

            for u, v, data in self._grafo.out_edges(artista, data=True):
                peso_uscenti += data["weight"]

            for u, v, data in self._grafo.in_edges(artista, data=True):
                peso_entranti += data["weight"]

            influenza = peso_uscenti - peso_entranti

            if best_influenza is None or influenza > best_influenza:
                best_influenza = influenza
                best_artista = artista

        return best_artista, best_influenza

    def getTopEdges(self):
        edges = list(self._grafo.edges(data=True))

        edges_sorted = sorted(edges,
                              key = lambda x: x[2]["weight"],
                              reverse=True)
        return edges_sorted[:5]


    def getGenres(self):
        return DAO.getGenres()

