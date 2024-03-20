class Query:
    def query_dados_treino(self, client_id: str) -> str:
        """Query para filtro das transações do cliente especificado"""
        return f""" WITH DistinctCategories AS (
                    SELECT DISTINCT
                        t.id,
                        cat.descricao
                    FROM
                        transactionitem ti
                        INNER JOIN [transaction] t ON t.id = ti.transaction_id
                        INNER JOIN client cli ON cli.id = t.client_id
                        INNER JOIN product p ON ti.sku = p.sku
                        INNER JOIN category cat ON p.categoria_id = cat.id
                    WHERE
                        cli.id = '{client_id}'
                )
                SELECT
                    id,
                    JSON_QUERY('[' + STRING_AGG('"' + descricao + '"', ',') + ']') AS categorias
                FROM
                    DistinctCategories
                GROUP BY
                    id;"""

    def delete_regras_associacao_old(self, client_id: int) -> str:
        """Deleta regras antigas do cliente antes da atualização"""
        return f""" WITH seleciona_id_regrarun AS (
                    SELECT TOP 1
                        id
                    FROM
                        regrarun
                    WHERE
                        client_id = {client_id}
                    ORDER BY
                        dt_inclusao DESC
                    ),
                    seleciona_id_regra AS (
                    SELECT
                        id
                    FROM
                        regra
                    WHERE
                        client_id IN (
                            SELECT
                                id
                            FROM
                            seleciona_id_regrarun)
                            )

                    DELETE FROM regra
                    WHERE id IN (
                    SELECT
                        id
                    FROM
                        seleciona_id_regra);"""

    def save_params_on_data_base(
        self,
        *,
        algorithm: str,
        params: dict,
        client_id: int,
    ) -> str:
        return f""" INSERT INTO regrarun (algoritmo, params, dt_inclusao, client_id)
                    VALUES ('{algorithm}', '{params}', GETDATE(), {client_id});"""

    def cria_tabelas_temporarias(self) -> str:
        return """  CREATE TABLE tempantecedente (
                        descricao_regra VARCHAR (255) NOT NULL,
                        antecedentes_list VARCHAR (255) NOT NULL);
                                                
                    CREATE TABLE tempconsequente (
                        descricao_regra VARCHAR (255) NOT NULL,
                        consequentes_list VARCHAR (255) NOT NULL);"""

    def atualiza_tabela_regra_categoria(self) -> str:
        """Atualiza a tabela de regra categoria a partir da tabela de regra
        e tabelas temporárias"""
        return """ INSERT INTO regracategoria (
                        regra_id
                        ,categoria_id
                        ,tipo
                        ,dt_inclusao
                        )
                    SELECT r.id
                        ,c.id
                        ,'A'
                        ,current_timestamp
                    FROM tempantecedente tempant
                    JOIN regra r ON r.descricao_regra = tempant.descricao_regra
                    JOIN category c on tempant.antecedentes_list = c.descricao;
                    
                    INSERT INTO regracategoria (
                        regra_id
                        ,categoria_id
                        ,tipo
                        ,dt_inclusao
                        )
                    SELECT r.id
                        ,c.id
                        ,'C'
                        ,current_timestamp
                    FROM tempconsequente tempcon
                    JOIN regra r ON r.descricao_regra = tempcon.descricao_regra
                    JOIN category c on tempcon.consequentes_list = c.descricao;"""

    def remove_tabelas_temporarias(self) -> str:
        return """  DROP TABLE IF EXISTS tempantecedente;
                    DROP TABLE IF EXISTS tempconsequente;"""

    def regras_formatadas_para_cache(self, client_id: int) -> str:
        return f""" SELECT
                        id,
                        confianca,
                        suporte,
                        lift,
                        MAX(CASE WHEN tipo = 'C' THEN categories_agg END) AS consequentes,
                        MAX(CASE WHEN tipo = 'A' THEN categories_agg END) AS antecedentes
                    FROM (SELECT
                            r.id,
                            r.confianca,
                            r.suporte,
                            r.lift,
                            rc.tipo,
                            JSON_QUERY('[' + string_agg(rc.categoria_id, ',') + ']') AS categories_agg
                        FROM
                            regra r
                            INNER JOIN regracategoria rc ON r.id = rc.regra_id
                            AND r.client_id = {client_id}
                        GROUP BY
                                        r.id,
                                        r.confianca,
                                        r.suporte,
                                        r.lift,
                                        rc.tipo) t
                    GROUP BY id, confianca, suporte, lift;"""
