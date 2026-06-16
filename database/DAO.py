from database.DB_connect import DBConnect
from model.Artist import Artist


class DAO():

    @staticmethod
    def getGenres():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select g.name
                from Genre g"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["name"])

        cursor.close()
        conn.close()

        return results

    @staticmethod
    def getNodes(genre):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.ArtistId , a.Name 
                    from Artist a 
                    join Album a2  on a2.ArtistId = a.ArtistId 
                    join track t on t.AlbumId = a2.AlbumId 
                    join genre g on g.GenreId = t.GenreId 
                    where g.Name = %s """

        cursor.execute(query, (genre,))

        for row in cursor:
            results.append(Artist(row["ArtistId"], row["Name"]))

        cursor.close()
        conn.close()

        return results

    @staticmethod
    def getEdges(genre):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct
                    q1.ArtistId as ArtistIdA,
                    q1.Name as NameA,
                    p1.Popolarita as PopA,
                    q2.ArtistId as ArtistIdB,
                    q2.Name as NameB,
                    p2.Popolarita as PopB,
                    p1.Popolarita + p2.Popolarita as Peso
                from (
                    select distinct 
                        i.CustomerId,
                        a.ArtistId,
                        a.Name
                    from Invoice i
                    join InvoiceLine il on il.InvoiceId = i.InvoiceId
                    join Track t on t.TrackId = il.TrackId
                    join Album al on al.AlbumId = t.AlbumId
                    join Artist a on a.ArtistId = al.ArtistId
                    join Genre g on g.GenreId = t.GenreId
                    where g.Name = %s
                ) q1
                join (
                    select distinct 
                        i.CustomerId,
                        a.ArtistId,
                        a.Name
                    from Invoice i
                    join InvoiceLine il on il.InvoiceId = i.InvoiceId
                    join Track t on t.TrackId = il.TrackId
                    join Album al on al.AlbumId = t.AlbumId
                    join Artist a on a.ArtistId = al.ArtistId
                    join Genre g on g.GenreId = t.GenreId
                    where g.Name = %s
                ) q2 on q1.CustomerId = q2.CustomerId
                join (
                    select 
                        a.ArtistId,
                        sum(il.Quantity) as Popolarita
                    from Artist a
                    join Album al on al.ArtistId = a.ArtistId
                    join Track t on t.AlbumId = al.AlbumId
                    join InvoiceLine il on il.TrackId = t.TrackId
                    join Genre g on g.GenreId = t.GenreId
                    where g.Name = %s
                    group by a.ArtistId
                ) p1 on p1.ArtistId = q1.ArtistId
                join (
                    select 
                        a.ArtistId,
                        sum(il.Quantity) as Popolarita
                    from Artist a
                    join Album al on al.ArtistId = a.ArtistId
                    join Track t on t.AlbumId = al.AlbumId
                    join InvoiceLine il on il.TrackId = t.TrackId
                    join Genre g on g.GenreId = t.GenreId
                    where g.Name = %s
                    group by a.ArtistId
                ) p2 on p2.ArtistId = q2.ArtistId
                where q1.ArtistId < q2.ArtistId
                order by q1.Name, q2.Name"""

        cursor.execute(query, (genre,genre,genre,genre))

        for row in cursor:
            results.append(row)

        cursor.close()
        conn.close()

        return results