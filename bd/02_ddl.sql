-- ==============================================================================
-- 02_dml.sql: Script de Inserção de Dados de Teste (Data Manipulation Language)
-- ==============================================================================

-- Inserindo Pessoas (Adotantes/Voluntários)
INSERT INTO Pessoa (nome, cpf, telefone, logradouro, numero, bairro, cidade, uf) VALUES
('Ana Clara Souza', '11122233344', '16999998888', 'Rua das Flores', '123', 'Centro', 'São Carlos', 'SP'),
('Bruno Mendes', '55566677788', '16988887777', 'Av. São Carlos', '456', 'Jardim Lutfalla', 'São Carlos', 'SP'),
('Carlos Eduardo Lima', '99988877766', '16977776666', 'Rua Sete de Setembro', '789', 'Vila Nery', 'São Carlos', 'SP');

-- Inserindo Animais
INSERT INTO Animal (nome, especie, raca, data_resgate, status_adocao) VALUES
('Rex', 'Cachorro', 'Vira-lata (SRD)', '2026-10-01', 'Disponível'),
('Mial', 'Gato', 'Siamês', '2026-10-15', 'Disponível'),
('Thor', 'Cachorro', 'Labrador', '2026-11-05', 'Em Tratamento'),
('Luna', 'Gato', 'Persa', '2026-11-10', 'Disponível'),
('Bolinha', 'Cachorro', 'Poodle', '2026-09-20', 'Disponível');

-- Inserindo uma Adoção de teste (O trigger mudará o status da Bolinha para 'Adotado')
INSERT INTO Adocao (data_adocao, termo_assinado, id_pessoa, id_animal) VALUES
('2026-11-20', TRUE, 1, 5);
