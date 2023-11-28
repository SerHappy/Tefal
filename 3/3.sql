SELECT
    COUNT(*) AS NumOfShops
FROM
    Sales AS S
    JOIN DIM_Shops AS DS ON S.IDShop = DS.IDShop
WHERE
    DS.ChainName = 'Эльдорадо'
    AND S.Date = '2021-02-12';
