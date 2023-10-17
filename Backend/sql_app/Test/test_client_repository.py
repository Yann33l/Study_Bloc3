from datetime import date

from Backend.sql_app import client_repository

ENV="local_test"

# Verification des types de données de la table clients

def test_get_depenses_CSP_ClasseArticle():
    result = client_repository.get_depenses_CSP_ClasseArticle()
    assert len(result) > 0
    assert all(isinstance(row[0], str) for row in result)
    assert all(isinstance(row[1], float) for row in result)
    assert all(isinstance(row[2], str) for row in result)
    print(result)


def test_get_moyenne_du_panier_par_CSP():
    result = client_repository.get_moyenne_du_panier_par_CSP()
    assert len(result) > 0
    assert all(isinstance(row[0], str) for row in result)
    assert all(isinstance(row[1], float) for row in result)


def test_get_Collecte():
    result = client_repository.get_Collecte()
    assert len(result) > 0
    assert all(isinstance(row[0], int) for row in result)
    assert all(isinstance(row[1], int) for row in result)
    assert all(isinstance(row[2], float) for row in result)
    assert all(isinstance(row[3], float) for row in result)
    assert all(isinstance(row[4], str) for row in result)


def test_get_visu_ensemble():
    result = client_repository.get_visu_ensemble()
    assert len(result) > 0
    assert all(isinstance(row[0], int) for row in result)
    assert all(isinstance(row[1], int) for row in result)
    assert all(isinstance(row[2], str) for row in result)
    assert all(isinstance(row[3], int) or row[3] is None for row in result)
    assert all(isinstance(row[4], date) for row in result)
    assert all(isinstance(row[5], int) or row[5] is None for row in result)
    assert all(isinstance(row[6], int) or row[6] is None for row in result)
    assert all(isinstance(row[7], float) or row[7] is None for row in result)
    assert all(isinstance(row[8], float) or row[8] is None for row in result)
    assert all(isinstance(row[9], str) or row[9] is None for row in result)

# Vérification du nombre de résultats par colonne
def test_check_column_counts_visu_ensemble():
    expected_column_counts = {
        0: 14028,
        1: 14028,
        2: 14028,
        3: 13704,
        4: 14028,
        5: 13704,
        6: 13704,
        7: 13704,
        8: 13704,
    }

    result = client_repository.get_visu_ensemble()

    column_counts = {}

    for row in result:
        for column_index, value in enumerate(row):
            if value is not None:
                if column_index not in column_counts:
                    column_counts[column_index] = 1
                else:
                    column_counts[column_index] += 1

    # Vérifiez le nombre de lignes pour chaque colonne
    for column_index, expected_count in expected_column_counts.items():
        assert column_index in column_counts, f"la colonne à l'index {column_index} n'est pas présente dans le résultat"
        actual_count = column_counts[column_index]
        assert actual_count == expected_count, f"Le nombre de linges pour la colonne à l'index {column_index} est incorrect. Attendu: {expected_count}, Reçu: {actual_count}"
