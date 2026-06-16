import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genreValue = None

    def fillDDGenre(self):
        generi = self._model.getGenres()
        generiDDoptions = list(map(lambda x: ft.dropdown.Option(
            data= x,
            key = x,
            on_click=self._choiceGenre),
                                   generi))

        self._view._ddGenre.options = generiDDoptions

        self._view.update_page()

    def _choiceGenre(self, e):
        self._genreValue = e.control.data

    def handleCreaGrafo(self, e):
        if self._genreValue is None:
            self._view.create_alert("Selezionare un genere!")
            return

        self._model.buildGraphP(self._genreValue)

        nNodes, nEdges = self._model.getGraphDetails()

        best_artist, best_influence = self._model.getArtistaPiuInfluente()

        top_edges = self._model.getTopEdges()

        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo creato correttamente"))

        self._view._txt_result.controls.append(
            ft.Text(f"Numero di vertici: {nNodes}."
                    f"Numero di archi: {nEdges}"))

        self._view._txt_result.controls.append(
            ft.Text(f"Artista con maggiore influenza: {best_artist} ({best_influence})"))

        self._view._txt_result.controls.append(
            ft.Text(f"Top 5 archi con peso maggiore:"))

        for u, v, data in top_edges:
            peso = data["weight"]
            self._view._txt_result.controls.append(
                ft.Text(f"{u} -> {v} | peso: {peso}"))

        self._view.update_page()


    def handleCammino(self,e):
        pass