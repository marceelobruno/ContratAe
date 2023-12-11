"""
Teste validação CPF
"""

from itertools import count
from validate_docbr import CPF

cpf = CPF()

# Validar CPF
cpf.validate("012.345.678-90")  # True
cpf.validate("012.345.678-91")  # False


cpf_me = "01234567890"

# Mascara o CPF
cpf.mask(cpf_me)  # "012.345.678-90"

cpf_mb = '05601332136'

mb_mask = cpf_mb
print(cpf.validate(mb_mask))




id_counter = count(start=1)
def get_id():
    return next(id_counter)

first_id  = get_id() # --> 1
second_id = get_id() # --> 2

print(first_id)
print(second_id)