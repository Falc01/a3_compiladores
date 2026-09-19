programa fatorial
  var n: inteiro;
  var fat: inteiro;
  var i: inteiro;
{
  # Leitura de entrada e cálculo do fatorial
  leia(n);
  fat = 1;
  i = 1;
  
  enquanto (i <= n) {
    fat = fat * i;
    i = i + 1;
  };
  
  escreva(fat);
}
fim.
