import os
import time
import psycopg2


def conectar():
    for tentativa in range(10):
        try:
            return psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                dbname=os.getenv("DB_NAME", "abrigo_db"),
                user=os.getenv("DB_USER", "abrigo_user"),
                password=os.getenv("DB_PASSWORD", "abrigo_pass"),
            )
        except psycopg2.OperationalError:
            print("Aguardando banco de dados ficar pronto...")
            time.sleep(2)
    raise RuntimeError("Não foi possível conectar ao PostgreSQL.")


def cadastrar_pessoa(conn):
    print("\n--- Cadastrar Pessoa ---")
    nome = input("Nome completo: ").strip()
    cpf = input("CPF (somente 11 números): ").strip()
    telefone = input("Telefone: ").strip()
    logradouro = input("Logradouro (Rua/Av): ").strip()
    numero = input("Número: ").strip()
    bairro = input("Bairro: ").strip()
    cidade = input("Cidade: ").strip()
    uf = input("UF (2 letras, ex: SP): ").strip().upper()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Pessoa (nome, cpf, telefone, logradouro, numero, bairro, cidade, uf)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_pessoa;
                """,
                (nome, cpf, telefone, logradouro, numero, bairro, cidade, uf),
            )
            novo_id = cur.fetchone()[0]
        conn.commit()
        print(f"Pessoa cadastrada com sucesso! ID: {novo_id}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro ao cadastrar pessoa: {e.pgerror or e}")


def cadastrar_animal(conn):
    print("\n--- Cadastrar Animal ---")
    nome = input("Nome do animal: ").strip()
    especie = input("Espécie (ex: Cachorro, Gato): ").strip()
    raca = input("Raça: ").strip()
    data_resgate = input("Data de resgate (AAAA-MM-DD): ").strip()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Animal (nome, especie, raca, data_resgate)
                VALUES (%s, %s, %s, %s)
                RETURNING id_animal;
                """,
                (nome, especie, raca, data_resgate),
            )
            novo_id = cur.fetchone()[0]
        conn.commit()
        print(f"Animal cadastrado com sucesso! ID: {novo_id}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erro ao cadastrar animal: {e.pgerror or e}")


def consultar_animais_disponiveis(conn):
    print("\n--- Animais Disponíveis para Adoção ---")
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id_animal, nome, especie, raca, data_resgate FROM vw_animais_disponiveis ORDER BY id_animal;"
        )
        linhas = cur.fetchall()

    if not linhas:
        print("Nenhum animal disponível no momento.")
        return

    for id_animal, nome, especie, raca, data_resgate in linhas:
        print(f"ID: {id_animal} | Nome: {nome} | Espécie: {especie} | Raça: {raca} | Resgate: {data_resgate}")


def registrar_adocao(conn):
    print("\n--- Registrar Adoção ---")
    consultar_animais_disponiveis(conn)

    with conn.cursor() as cur:
        cur.execute("SELECT id_pessoa, nome, cpf FROM Pessoa ORDER BY id_pessoa;")
        pessoas = cur.fetchall()

    print("\n--- Pessoas Cadastradas ---")
    for id_p, nome, cpf in pessoas:
        print(f"ID: {id_p} | Nome: {nome} | CPF: {cpf}")

    try:
        id_pessoa = int(input("\nInforme o ID da Pessoa adotante: ").strip())
        id_animal = int(input("Informe o ID do Animal: ").strip())
        termo = input("Termo de responsabilidade assinado? (S/N): ").strip().upper() == "S"

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO Adocao (termo_assinado, id_pessoa, id_animal)
                VALUES (%s, %s, %s)
                RETURNING id_adocao;
                """,
                (termo, id_pessoa, id_animal),
            )
            id_adocao = cur.fetchone()[0]
        conn.commit()
        print(f"Adoção registrada com sucesso! ID da Adoção: {id_adocao}")
    except ValueError:
        print("ID inválido. Digite apenas números.")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Operação bloqueada pelo banco: {e.pgerror or e}")


def listar_adocoes(conn):
    print("\n--- Histórico de Adoções Realizadas ---")
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT ad.id_adocao, ad.data_adocao, p.nome, a.nome, a.especie, ad.termo_assinado
            FROM Adocao ad
            INNER JOIN Pessoa p ON ad.id_pessoa = p.id_pessoa
            INNER JOIN Animal a ON ad.id_animal = a.id_animal
            ORDER BY ad.id_adocao;
            """
        )
        linhas = cur.fetchall()

    if not linhas:
        print("Nenhuma adoção registrada.")
        return

    for id_ad, data_ad, adotante, animal, especie, termo in linhas:
        status_termo = "Sim" if termo else "Não"
        print(f"Adoção #{id_ad} | Data: {data_ad} | Adotante: {adotante} | Animal: {animal} ({especie}) | Termo: {status_termo}")


def menu():
    conn = conectar()
    try:
        while True:
            print("\n==========================================")
            print("  SISTEMA DE GESTÃO DE ABRIGO DE ANIMAIS  ")
            print("==========================================")
            print("1. Cadastrar Pessoa")
            print("2. Cadastrar Animal")
            print("3. Registrar Adoção")
            print("4. Consultar Animais Disponíveis")
            print("5. Consultar Histórico de Adoções")
            print("0. Sair")
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                cadastrar_pessoa(conn)
            elif opcao == "2":
                cadastrar_animal(conn)
            elif opcao == "3":
                registrar_adocao(conn)
            elif opcao == "4":
                consultar_animais_disponiveis(conn)
            elif opcao == "5":
                listar_adocoes(conn)
            elif opcao == "0":
                print("Encerrando sistema...")
                break
            else:
                print("Opção inválida.")
    finally:
        conn.close()


if __name__ == "__main__":
    menu()