-- Q1 : Délai moyen de livraison et taux de retard global
SELECT
    ROUND(AVG(delivery_days), 1)        AS delai_moyen_jours,
    ROUND(100.0 * SUM(is_late) 
          / COUNT(*), 1)                AS taux_retard_pct,
    COUNT(*)                            AS nb_commandes
FROM orders;

-- Q2 : Délai moyen et taux de retard par état du client
SELECT
    customer_state,
    ROUND(AVG(delivery_days), 1)        AS delai_moyen_jours,
    ROUND(100.0 * SUM(is_late) 
          / COUNT(*), 1)                AS taux_retard_pct,
    COUNT(*)                            AS nb_commandes
FROM orders
GROUP BY customer_state
ORDER BY delai_moyen_jours DESC;

-- Q3 : Evolution mensuelle du volume et des retards
SELECT
    order_month,
    COUNT(*)                            AS nb_commandes,
    ROUND(100.0 * SUM(is_late) 
          / COUNT(*), 1)                AS taux_retard_pct
FROM orders
GROUP BY order_month
ORDER BY order_month;