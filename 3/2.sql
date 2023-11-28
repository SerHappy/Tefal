SELECT
    SUM(S.Amount) AS TotalSalesAmount
FROM
    Sales AS S
    JOIN DIM_Shops AS DS ON S.IDShop = DS.IDShop
WHERE
    DS.ChainName = 'METRO'
    AND MONTH(S.Date) = 2
    AND YEAR(S.Date) = 2021;
