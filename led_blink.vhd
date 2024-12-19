-- exemplo de led_blink simples
-- 19/12/2024
-- Douglas


-- testar codigo vhdl na placa direto, depois fazer um testbench


library ieee; 
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

--definindo a entidade
entity led_blink is
  port(
    clk_50: in std_logic; -- 50Mhz
    led: out std_logic;
    );
end led_blink;

-- definindo comportamento da entidade led_blink
architecture behavioral of led_blink is
  signal
  signal

begin

end behavioral;




  
