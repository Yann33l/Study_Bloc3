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
    
def get_Collecte():
    with engine_read.connect() as connection:
        query = text("SELECT ROW_NUMBER() OVER (ORDER BY id_panier, libelle_categorie) AS collecte, \
                    id_panier AS num_panier,  \
                    prix_panier.PPA as Prix_panier,  \
                    ROUND(SUM(quantite_article * prix_vente), 2) AS montant,  \
                    libelle_categorie AS categorie_article  \
                    FROM clients c  \
                    LEFT JOIN cat_socio_pro csp ON csp.ID = c.id_CSP \
                    LEFT JOIN paniers p ON p.id_client = c.ID \
                    LEFT JOIN r_panier_article r_pa ON r_pa.id_panier = p.ID \
                    LEFT JOIN articles a ON a.ID = r_pa.id_article \
                    LEFT JOIN categories_articles ca ON ca.id = a.id_categorie_article \
                    LEFT JOIN ( \
                        SELECT r_pa.id_panier AS panier_id, \
                            ROUND(SUM(quantite_article * prix_vente), 2) AS PPA \
                        FROM paniers p \
                        LEFT JOIN r_panier_article r_pa ON r_pa.id_panier = p.ID \
                        LEFT JOIN articles a ON a.ID = r_pa.id_article \
                        WHERE prix_vente IS NOT NULL \
                        GROUP BY r_pa.id_panier) as prix_panier  \
                        ON r_pa.id_panier = prix_panier.panier_id \
                    WHERE prix_vente IS NOT NULL \
                    GROUP BY libelle_CSP, libelle_categorie, ca.ID, id_panier, prix_panier.PPA \
                    ORDER BY id_panier, libelle_categorie;") 
        result = connection.execute(query)
        return result.fetchall()
         

def get_visu_ensemble():
    with engine_read.connect() as connection:
        query = text("SELECT num_client, nbr_enfants, libelle_CSP, id_panier, date_achat, id_article, quantite_article, prix_vente, cout, libelle_categorie \
                    FROM clients c \
                    LEFT JOIN cat_socio_pro csp on csp.ID = c.id_CSP \
                    LEFT JOIN paniers p on p.id_client = c.ID \
                    LEFT JOIN r_panier_article r_pa on r_pa.id_panier = p.ID \
                    LEFT JOIN articles a on a.ID = r_pa.id_article \
                    LEFT JOIN categories_articles ca on a.id_categorie_article = ca.ID \
                    ;") 
        result = connection.execute(query)
        return result.fetchall()

