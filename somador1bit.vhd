library ieee;
use ieee.std_logic_1164.all;

-- tentativa de fazer codigo para somador de 1 bit e testbench para 
-- testar
-- data:10/12/2024 -- Douglas
-- usar o codigo no VIVADO, de forma correta organizada no programa


--### TESTBENCH

entity somador1bit_tb is
end somador1bit_tb;


architecture arch of somador1bit_tb is

constant periodo : time := 100ns;
--sinais a serem testados do SOMADOR 
signal a : std_logic := '0';
signal b : std_logic := '1';
signal c_in : std_logic := '0'; 
signal s : std_logic;
signal c_out : std_logic;


-- "componente" a ser TESTADO
component somador1bit is
  port(A : in std_logic;
	   B : in std_logic;
	   C_in : in std_logic;
	   S : out std_logic;
	   C_out : out std_logic);

end component;


-- Instancia para realizar a copia do "componente"
-- uut = Unit Under Test = unidade sob teste
--
--


uut : somador1bit
  port map(A => a, B => b, C_in => c_in, S => s, C_out => c_out);

begin

process
  begin
    a <= '0';
	wait for periodo/2;
	a <= '1';
    wait for periodo/2;
  end process; 

end arch



--### FIM DO ARQUIVO DO TESTBENCH somador de 1 bit


--### ARQUIVO: somador de 1 bit

--bibliotecas


entity somador1bit is
  port(a : in std_logic;
       b : in std_logic;
	   c_in : in std_logic;
	   s : out std_logic;
	   c_out : out std_logic);

end somador1bit;


architecture arch of somador1bit is


begin

process(a,b,c_in)
  begin
    s <= a xor b xor c_in;
	c_out <= (a and b) or (a and c_in) or (b and c_in);
    
  end process; 

end arch




-- APRIMORAMENTO DO TESTBENCH PELO CHAT GPT, para testar todas as portas
--
-- 10/12/2024


entity somador1bit_tb is
end somador1bit_tb;

architecture arch of somador1bit_tb is

  constant periodo : time := 100ns;

  -- Sinais de teste
  signal a      : std_logic := '0';
  signal b      : std_logic := '0';
  signal c_in   : std_logic := '0'; 
  signal s      : std_logic;
  signal c_out  : std_logic;

  -- Componente a ser testado
  component somador1bit is
    port(
      A     : in std_logic;
      B     : in std_logic;
      C_in  : in std_logic;
      S     : out std_logic;
      C_out : out std_logic
    );
  end component;

begin

  -- Instancia o somador1bit
  uut : somador1bit
    port map(
      A => a, 
      B => b, 
      C_in => c_in, 
      S => s, 
      C_out => c_out
    );

  -- Processo de estímulo
  process
  begin
    -- Testar todas as combinações de entradas (a, b, c_in)
    for i in 0 to 7 loop
      -- Desempacotar as combinações para a, b, c_in
      a <= std_logic'(i mod 2); -- i mod 2 para alternar entre 0 e 1
      b <= std_logic'((i / 2) mod 2); -- (i / 2) mod 2 para alternar entre 0 e 1
      c_in <= std_logic'((i / 4) mod 2); -- (i / 4) mod 2 para alternar entre 0 e 1

      -- Esperar um ciclo de clock
      wait for periodo;
    end loop;

    -- Fim da simulação
    wait;
  end process;

end arch;
