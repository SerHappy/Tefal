SELECT TOP 5
    DP.IDSku,
    DP.SkuName
FROM
    Sales AS S
    JOIN DIM_Shops AS DS ON S.IDShop = DS.IDShop
    JOIN DIM_Products AS DP ON S.IDSku = DP.IDSku
WHERE
    DS.ChainName = 'ДНС'
GROUP BY
    DP.IDSku,
    DP.SkuName
ORDER BY
    SUM(S.Quantity) DESC;
