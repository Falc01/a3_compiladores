# Teste da Extensão Obrigatória Oficial (Opção D): Comandos 'para' e 'repita ... até'

programa teste_extensao
  var contador: inteiro;
  var limite: inteiro;
  var acumulador: inteiro;
{
  limite = 10;
  acumulador = 0;

  # Laço determinado 'para'
  para (contador = 1; contador <= limite; contador = contador + 1) {
    acumulador = acumulador + contador;
  };

  # Laço pós-testado 'repita ... até'
  repita {
    acumulador = acumulador - 1;
  } até (acumulador <= 0);

  escreva(acumulador);
}
fim.
