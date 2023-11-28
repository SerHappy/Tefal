SELECT DISTINCT
    DP.Brand
FROM
    Sales AS S
    JOIN DIM_Shops AS DS ON S.IDShop = DS.IDShop
    JOIN DIM_Products as DP ON S.IDSku = DP.IDSku
WHERE
    DS.ChainName = 'Глобус';
