SELECT TOP 10 *
FROM bank_marketing;

SELECT COUNT(*) AS total_rows
FROM bank_marketing;

/* les deux querys au dessus sont juste la pour verifier que tout est ok mais ca reste important de le faire 
TIPS : selectionner avec la souris pour lancer seulement la query que l'on souhaite sans avoir a tout mettre en commentaire */

SELECT
    job,
    COUNT(*) AS total_clients
FROM bank_marketing
GROUP BY job;

-- pour voir le nombre de client par profession, on va maintenant cherche le taux de souscription par client, plus interessant :

SELECT
    job,
    COUNT(*) AS total_clients,
    SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) AS subscribed_clients,
    ROUND(
        100.0 * SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS subscription_rate
FROM bank_marketing
GROUP BY job
ORDER BY subscription_rate DESC;

SELECT
    job,
    ROUND(AVG(CAST(balance AS FLOAT)), 2) AS mean_balance
FROM bank_marketing
GROUP BY job
ORDER BY mean_balance DESC;

-- OK interessant, on remarque en lancant cette query que c'est les etudiants qui souscrivent le plus a l'offre.
-- cela paraissait bizarre donc j'ai ecrit une deuxieme query  avec la mean balance de chaque job et en effet les student sont loin dans le classement.
-- la variable cible ne depend surement pas de la balance mais ca reste une hypothese a verifier

-- Maintenant on va repondre a une autre question le taux de souscription apr tranche d'age :

SELECT
    CASE
        WHEN age < 25 THEN '<25'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        WHEN age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END AS age_group,

    COUNT(*) AS total_clients,

    SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) AS subscribed_clients,

    ROUND(
        100.0 * SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS subscription_rate

FROM bank_marketing

GROUP BY
    CASE
        WHEN age < 25 THEN '<25'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        WHEN age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END

ORDER BY subscription_rate DESC;

-- on remarque avec cette requete qu'il n'y a pas vraiment de logique du genre : plus on est vieux plus on souscrit, ou l'inverse.
-- mais on voit que nos variables ne sont pas fausses car on retrouve un lien entre l'age et le job (student en <25, retired en +65, ...)

-- regardons quelle categorie d'education presente le meilleur taux, meme requete que pour le job juste modifiee :

SELECT
    education,
    COUNT(*) AS total_clients,
    SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) AS subscribed_clients,
    ROUND(
        100.0 * SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS subscription_rate
FROM bank_marketing
GROUP BY education
ORDER BY subscription_rate DESC;
-- tertiary en premier -> enseignement sup, unknown ici ne veut pas dire des etudes inconnues mais plutot que l'utilisateur n'a pas foournie l'info a mon avis

-- question importante a se poser, est ce qu'un client qui a deja souscrit lors d'une ancienne campagne
-- est t il plus susceptible de souscire ou pas ?

SELECT
    poutcome,
    COUNT(*) AS total_clients,
    SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) AS subscribed_clients,
    ROUND(
        100.0 * SUM(CASE WHEN deposit = 'yes' THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS subscription_rate
FROM bank_marketing
GROUP BY poutcome
ORDER BY subscription_rate DESC;
-- wow, ceux qui ont un poutcome succes ont un subscription rate de 91%, c'est enorme, donc oui 
-- pour repondre a notre question en effet il y a plus de chance, mais aussi meme si poutcome est failure
-- le sub rate est tout de meme de 50%, ce qui n'est pas a negliger
-- mais il faut a tout prix prendre en compte ce resultat de 91% sur un poutcome success.


-- derniere qeustion qui peut etre interessante c'est de savoir si le nombre d'appel ou de contact a un client pendant l'ancienne
--campagne a influence son deposit :
SELECT
    poutcome,
    COUNT(*) AS total_clients,
    ROUND(AVG(CAST(campaign AS FLOAT)), 2) AS average_contacts
FROM bank_marketing
GROUP BY poutcome
ORDER BY average_contacts DESC;
-- et la aussi le resultat est aussi surprenant car bien qu'on ne connaisse pas unknown, le poutcome success se place
-- en bas de classement, c'est a dire qu'ils sont ceux qui ont ete le moins appeles, et pourtant c'est eux qui ont souscrit.