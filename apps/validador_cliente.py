import re


class ValidadorCliente:

    def __init__(self, nome, email, idade, cpf, cep):
        self.nome = nome
        if self.validar_email(email):
            self.email = email
        else:
            raise ValueError("Email invalido")
        if self.validador_idade(idade):
            self.idade = idade
        else:
            raise ValueError("Idade invalida (abaixo de 18 anos ou acima de 120 anos)")
        if self.validar_cpf(cpf):
            self.cpf = cpf
        else:
            raise ValueError("Cpf invalido")
        if self.validar_cep(cep):
            self.cep = cep
        else:
            raise ValueError("CEP invalido")

    @staticmethod
    def validar_email(email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        # O padrão acima verifica se o email tem o formato adequado

        if re.match(padrao, email):
            print(f"EMAIL : {email} Validada")
            return True
        else:
            return False

    @staticmethod
    def validador_idade(idade):
        idade = int(idade)
        if idade > 18 or idade <= 120:
            print(f"IDADE : {idade} Validada")
            return True
        else:
            return False

    @staticmethod
    def validar_cpf(cpf):
        cpf = str(cpf)
        # Removendo caracteres especiais
        cpf = cpf.replace(".", "").replace("-", "")

        # Verificando se o CPF possui 11 dígitos
        if len(cpf) != 11:
            return False

        # Verificando se todos os dígitos são iguais (CPF inválido)
        if cpf == cpf[0] * 11:
            return False

        # Verificando o primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        digito1 = 11 - (soma % 11)
        if digito1 > 9:
            digito1 = 0
        if int(cpf[9]) != digito1:
            return False

        # Verificando o segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        digito2 = 11 - (soma % 11)
        if digito2 > 9:
            digito2 = 0
        if int(cpf[10]) != digito2:
            return False

        print(f"CPF : {cpf} Validado")

        return True

    @staticmethod
    def validar_cep(cep):
        # Remove quaisquer caracteres que não sejam dígitos
        cep = str(cep)
        cep = re.sub(r'\D', '', cep)

        # Verifica se o CEP possui exatamente 8 dígitos
        if len(cep) != 8:
            return False

        # Verifica se o CEP não possui todos os dígitos iguais
        if len(set(cep)) == 1:
            return False

        # Verifica se o CEP é válido de acordo com o padrão
        if re.match(r'^[0-9]{8}$', cep):
            print(f"CEP : {cep} Validado")
            return True

        return False

