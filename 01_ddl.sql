-- ==============================================================================
-- 01_ddl.sql: Script de Criação do Esquema (Data Definition Language)
-- ==============================================================================

-- 1. Criação das Tabelas
CREATE TABLE Pessoa (
    id_pessoa SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    telefone VARCHAR(15),
    logradouro VARCHAR(100),
    numero VARCHAR(10),
    bairro VARCHAR(50),
    cidade VARCHAR(50),
    uf CHAR(2)
);

CREATE TABLE Animal (
    id_animal SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raca VARCHAR(50),
    data_resgate DATE NOT NULL,
    status_adocao VARCHAR(20) NOT NULL DEFAULT 'Disponível'
    CHECK (status_adocao IN ('Disponível', 'Em Tratamento', 'Adotado'))
);

CREATE TABLE Adocao (
    id_adocao SERIAL PRIMARY KEY,
    data_adocao DATE NOT NULL DEFAULT CURRENT_DATE,
    termo_assinado BOOLEAN NOT NULL,
    id_pessoa INTEGER NOT NULL,
    id_animal INTEGER UNIQUE NOT NULL, -- Garante cardinalidade 1:1 para o animal
    
    FOREIGN KEY (id_pessoa) REFERENCES Pessoa(id_pessoa) ON DELETE RESTRICT,
    FOREIGN KEY (id_animal) REFERENCES Animal(id_animal) ON DELETE RESTRICT
);

-- ==============================================================================
-- 2. Lógica no Banco (Views, Functions e Triggers)
-- ==============================================================================

-- VIEW: Simplifica a busca por animais disponíveis, ocultando regras complexas
CREATE VIEW vw_animais_disponiveis AS
SELECT id_animal, nome, especie, raca, data_resgate
FROM Animal
WHERE status_adocao = 'Disponível';

-- FUNCTION: Lógica para impedir adoção de animal doente ou já adotado
CREATE OR REPLACE FUNCTION trg_valida_adocao()
RETURNS TRIGGER AS $$
DECLARE
    v_status VARCHAR(20);
BEGIN
    -- Busca o status atual do animal
    SELECT status_adocao INTO v_status FROM Animal WHERE id_animal = NEW.id_animal;
    
    IF v_status <> 'Disponível' THEN
        RAISE EXCEPTION 'Adoção bloqueada: O animal não está disponível para adoção (Status: %)', v_status;
    END IF;
    
    -- Atualiza automaticamente o status do animal para 'Adotado'
    UPDATE Animal SET status_adocao = 'Adotado' WHERE id_animal = NEW.id_animal;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- TRIGGER: Dispara a validação antes de inserir uma nova adoção
CREATE TRIGGER trigger_valida_adocao
BEFORE INSERT ON Adocao
FOR EACH ROW
EXECUTE FUNCTION trg_valida_adocao();