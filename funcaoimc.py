# Calcula como a pessoa se enquadra baseado no IMC
def calculaImc(alt, pes):

  # Converte altura para metro
  altmetros = alt / 100

  # Cálculo do IMC jogado a uma variável
  imc = pes / (altmetros * altmetros)

  estado = ''
  if imc < 17:
    estado = 'Muito abaixo do Peso'
  elif imc >= 17 and imc < 18.5:
    estado = 'Abaixo do Peso'
  elif imc >= 18.5 and imc <= 24.99:
    estado = 'Peso Normal'
  elif imc >= 25 and imc <= 29.99:
    estado = 'Acima do Peso'
  elif imc >= 30 and imc <= 34.99:
    estado = 'Obesidade I'
  elif imc >= 35 and imc <= 39.99:
    estado = 'Obesidade Severa'
  elif imc >= 40:
    estado = 'Obesidade Mórbida'

  lista = []
  lista.append(imc)
  lista.append(estado)
  lista.append(altmetros)
  return lista
