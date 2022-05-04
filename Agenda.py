'''
Criando uma agenda de Contatos

Tabela e índices no SQLite:
CREATE TABLE contatos (
    codigo   INTEGER      PRIMARY KEY AUTOINCREMENT,
    nome     VARCHAR (50) NOT NULL,
    telefone VARCHAR (15) NOT NULL,
    email    VARCHAR (50)
);
CREATE INDEX idx_codigo ON contatos (
    codigo ASC
);

CREATE INDEX idx_nome ON contatos (
    nome ASC
);
'''
import os
import sqlite3

# ############################################################################
# Funções que exibem informações na tela
# ############################################################################
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def cabecalho(texto=''):
    cls()
    print('╔' + '═' * 78 + '╗')
    print('║ {:^76} ║'.format('A G E N D A   D E   C O N T A T O S'))
    print('╚' + '═' * 78 + '╝')
    if texto != '':
        #print("\n{:^80}\n".format(texto))
        print("\n\033[1m{:^80}\033[m".format(texto))
        print("─" * 80)

# Menu para selecionar o que será realizado na agenda
def menu():
    cls()
    cabecalho()
    print(' 1. Listar seus contatos')
    print(' 2. Incluir um contato')
    print(' 3. Alterar um contato')
    print(' 4. Apagar um contato')
    print(' 5. Sair')
    opcao = input('\nSelecione a opção: ')

    if opcao == '':
        opcao=0
    opcao = int(opcao)

    while opcao < 1 or opcao > 5:
        print('\n\033[91mOpção inválida\033[m')
        opcao = input('\nSelecione a opção: ')
        if opcao == '':
            opcao=0
        opcao = int(opcao)

    return opcao

def listar():
    cabecalho('Lista de Contatos')

    cursor = conn.cursor()

    # lendo os dados
    try:
        cursor.execute("""
        SELECT * FROM contatos;
        """)

        print('\n Id   Nome                      Telefone          E-mail')
        print('───── ───────────────────────── ───────────────── ──────────────────────────────')
        for linha in cursor.fetchall():
            regid = str(linha[0])
            regNome = str(linha[1])
            regTelefone = str(linha[2])
            regEmail = str(linha[3])
            print('{:>3}   {:25} {:17} {:30}'.format(regid, regNome[:25], regTelefone[:17], regEmail[:30]))
        input('\nPressione uma tecla para voltar.')
    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')

def incluir():
    cabecalho('Incluir um Contato')
    regNome     = str(input('\n Nome......: '))
    while regNome.__len__() == 0:
        print('\033[91m O nome precisa ser preenchido.\033[m')
        regNome = str(input('\n Nome......: '))

    regTelefone = str(input(' Telefone..: '))
    while regTelefone.__len__() == 0:
        print('\033[91m O telefone precisa ser preenchido\033[m')
        regTelefone = str(input('\n Telefone..: '))

    regEmail    = str(input(' E-mail....: '))

    cursor = conn.cursor()

    try:
        # Inserindo dados na tabela
        cursor.execute("""
        INSERT INTO contatos (nome, telefone, email)
        VALUES (?,?,?)
        """, (regNome, regTelefone, regEmail))
        conn.commit()
        input('\nContato incluído. Pressione uma tecla para voltar.')

    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')

def alterar():
    cabecalho('Alterar um Contato')

    regId = str(input('\n Id do contato.: '))
    while regId.__len__() == 0:
        print('\033[91m O Id precisa ser preenchido.\033[m')
        regId = str(input('\n Id do contato.: '))

    cursor = conn.cursor()

    try:
        # Lendo as informações do contato
        cursor.execute("""
            SELECT nome, telefone, email FROM contatos WHERE codigo=?;
            """, (regId))

        linha = cursor.fetchall()
        if linha.__len__() > 0:
            regAntNome = linha[0][0]
            regAntTelefone = linha[0][1]
            regAntEmail = linha[0][2]

            print('\n─ Dados Antigos ' + '─' * 64)
            print(' Nome......: {}'.format(regAntNome))
            print(' Telefone..: {}'.format(regAntTelefone))
            print(' E-mail....: {}'.format(regAntEmail))

            print('\n─ Novos Dados '  + '─' * 66)
            regNome     = str(input(' Nome......: '))
            while regNome.__len__() == 0:
                print('\033[91m O nome precisa ser preenchido.\033[m')
                regNome = str(input('\n Nome......: '))

            regTelefone = str(input(' Telefone..: '))
            while regTelefone.__len__() == 0:
                print('\033[91m O telefone precisa ser preenchido\033[m')
                regTelefone = str(input('\n Telefone..: '))

            regEmail    = str(input(' E-mail....: '))

            # Alterando os dados da tabela
            try:
                cursor.execute("""
                UPDATE contatos
                SET nome = ?, telefone = ?, email = ?
                WHERE codigo = ?
                """, (regNome, regTelefone, regEmail, regId))
                conn.commit()
                input('\nContato alterado. Pressione uma tecla para voltar.')
            except sqlite3.Error as er:
                print('Erro :', er.message)
                input('Pressione <ENTER>')
        else:
            input('\n\033[91mNenhum Contato com esse Id.\033[m\nPressione uma tecla para voltar.')
    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')

def excluir():
    cabecalho('Apagar um Contato')

    regId = str(input('\n Id do contato.: '))
    while regId.__len__() == 0:
        print('\033[91m O Id precisa ser preenchido.\033[m')
        regId = str(input('\n Id do contato.: '))

    cursor = conn.cursor()

    # Lendo as informações do contato
    try:
        cursor.execute("""
            SELECT nome, telefone, email FROM contatos WHERE codigo=?;
            """, (regId))

        linha = cursor.fetchall()
        if linha.__len__() > 0:
            regAntNome = linha[0][0]
            regAntTelefone = linha[0][1]
            regAntEmail = linha[0][2]

            print('\n─ Dados do Contato '  + '─' * 61)
            print(' Nome......: {}'.format(regAntNome))
            print(' Telefone..: {}'.format(regAntTelefone))
            print(' E-mail....: {}'.format(regAntEmail))
            print('\n\033[7mConfirma a exclusão ?\033[m')
            confirmar   = str(input('S/N ? '))

            if confirmar == 's' or confirmar == 'S':
                # Apagando o contato da tabela
                try:
                    cursor.execute("""
                    DELETE FROM contatos 
                    WHERE codigo = ?
                    """, (regId))
                    conn.commit()
                except sqlite3.Error as er:
                    print('Erro :', er.message)
                    input('Pressione <ENTER>')
                input('\nContato apagado. Pressione uma tecla para voltar.')
            else:
                input('\nPressione uma tecla para voltar.')
        else:
            input('\n\033[91mNenhum Contato com esse Id.\033[m\nPressione uma tecla para voltar.')
    except sqlite3.Error as er:
        print('Erro :', er.message)
        input('Pressione <ENTER>')

# ############################################################################
# Funções que trabalham com o SQLite
# ############################################################################
def conectar(arquivo='contatos.db'):
    return sqlite3.connect(arquivo)

def desconectar(conexao=''):
    if conexao != '':
        conexao.close()

def verificarArquivoBanco():
    if os.path.exists('contatos.db') == False:
        # Conectando
        conn = sqlite3.connect('contatos.db')

        # Definindo um cursor
        cursor = conn.cursor()

        try:
            # Criando a tabela (schema)
            cursor.execute("""
                CREATE TABLE contatos (
                    codigo   INTEGER      PRIMARY KEY AUTOINCREMENT,
                    nome     VARCHAR (50) NOT NULL,
                    telefone VARCHAR (15) NOT NULL,
                    email    VARCHAR (50)
                );
            """)
            conn.commit()

            cursor.execute("""
                CREATE INDEX idx_codigo ON contatos (
                    codigo ASC
                );
            """)
            conn.commit()

            cursor.execute("""
                CREATE INDEX idx_nome ON contatos (
                    nome ASC
                );
            """)
            conn.commit()
        except sqlite3.Error as er:
            print('Erro :', er.message)
            input('Pressione <ENTER>')

        conn.close()

# ############################################################################
# Execução do script
# ############################################################################

# Verificando se o arquivo dd banco de dados existe
verificarArquivoBanco()

# Laço de execução da agenda
opcaoSelecionbada = menu()

# Conectando com a base de dados SQLite3
conn = conectar('contatos.db')

while opcaoSelecionbada != 5:
    print(opcaoSelecionbada)

    if opcaoSelecionbada == 1:
        listar()
    elif opcaoSelecionbada == 2:
        incluir()
    elif opcaoSelecionbada == 3:
        alterar()
    else:
        excluir()

    opcaoSelecionbada = menu()

# Desconectando
desconectar(conn)