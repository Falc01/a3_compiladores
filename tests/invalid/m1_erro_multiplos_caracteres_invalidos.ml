programa teste_multiplos_erros
  var a: inteiro;
  var b: inteiro;
{
  a = @10;       # Erro na linha 5: @
  b = ~20;       # Erro na linha 6: ~
  a = a ` b;     # Erro na linha 7: `
}
fim.
