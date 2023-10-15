from sqlalchemy.sql.expression import text

from Backend.sql_app.database import engine_read


def get_depenses_CSP_ClasseArticle():
    with engine_read.connect() as connection:
        query = text("SELECT libelle_CSP as CSP, round(sum(quantite_article*prix_vente), 2) as depenses, libelle_categorie as categorie_vetement \
                        FROM clients c \
                        LEFT JOIN cat_socio_pro csp on csp.ID = c.id_CSP \
                        LEFT JOIN paniers p on p.id_client = c.ID \
                        LEFT JOIN r_panier_article r_pa on r_pa.id_panier = p.ID \
                        LEFT JOIN articles a on a.ID = r_pa.id_article \
                        LEFT JOIN categories_articles ca on a.id_categorie_article = ca.ID \
                        WHERE libelle_categorie IS NOT NULL \
                        GROUP BY libelle_CSP, libelle_categorie \
                        ORDER BY 1, 3;")
        result = connection.execute(query)
        return result.fetchall()
"""     return Exception("Erreur lors de la récupération des données") """

def get_moyenne_du_panier_par_CSP():
    with engine_read.connect() as connection:
        query = text("SELECT libelle_CSP as CSP, round(sum(quantite_article*prix_vente)/count(distinct id_panier),2) as Moy_panier \
                    FROM clients c \
                    LEFT JOIN cat_socio_pro csp on csp.ID = c.id_CSP \
                    left join paniers p on p.id_client = c.ID \
                    left join r_panier_article r_pa on r_pa.id_panier = p.ID \
                    left join articles a on a.ID = r_pa.id_article \
                    where prix_vente is not null \
                    group by libelle_CSP \
                    ;")
        result = connection.execute(query)
        return result.fetchall()
    
