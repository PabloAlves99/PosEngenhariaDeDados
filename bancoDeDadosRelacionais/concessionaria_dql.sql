SELECT 
    ve.id_veiculo,
    ve.placa,
    mo.nome_modelo,
    ver.nome_versao,
    ma.nome_marca
FROM Veiculo ve
JOIN Modelo mo ON ve.modelo_id = mo.id_modelo
JOIN Versao ver ON ve.versao_id = ver.id_versao
JOIN Marca ma ON mo.marca_id = ma.id_marca;


SELECT 
    v.id_venda,
    c.nome AS nome_cliente,
    f.nome AS nome_funcionario,
    ve.placa,
    v.valor_venda,
    v.data_venda
FROM Venda v
JOIN Cliente c ON v.id_cliente = c.id_cliente
JOIN Funcionario f ON v.id_funcionario = f.id_funcionario
JOIN Veiculo ve ON v.id_veiculo = ve.id_veiculo;


SELECT 
    id_cliente,
    nome,
    tipo_cliente,
    data_cadastro
FROM Cliente
ORDER BY data_cadastro ASC;


SELECT 
    id_veiculo,
    placa,
    cor,
    ano_modelo,
    quilometragem_atual
FROM Veiculo
WHERE status_veiculo = 'Disponível'
ORDER BY ano_modelo DESC;


SELECT 
    id_funcionario,
    nome,
    cargo,
    salario
FROM Funcionario
ORDER BY salario DESC;


SELECT 
    fp.metodo_pagamento,
    COUNT(v.id_venda) AS total_vendas
FROM FormaPagamento fp
JOIN Venda v ON v.id_pagamento = fp.id_pagamento
GROUP BY fp.metodo_pagamento
ORDER BY total_vendas DESC;


SELECT 
    c.nome,
    c.email,
    pf.cpf,
    pf.sexo,
    pf.data_nascimento
FROM Cliente c
JOIN ClientePF pf ON c.id_cliente = pf.id_cliente;

SELECT 
    v.placa,
    v.cor,
    iser.nome_item,
    iser.categoria
FROM Veiculo v
JOIN VeiculoItemSerie vis ON v.id_veiculo = vis.veiculo_id
JOIN ItemSerie iser ON vis.item_serie_id = iser.id_item
ORDER BY v.placa, iser.categoria;
