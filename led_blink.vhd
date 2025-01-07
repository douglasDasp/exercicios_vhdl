-- exemplo de led_blink simples
-- 19/12/2024
-- Douglas

-- testado e OK no VIVADO 2024.2 p/ FPGA Xilinx

-- TESTADO NO CODIGO:
    -- > SINTESE  = OK
    -- > IMPLEMENTACAO  = OK
    -- > SIMULACAO/TESTBENCH  = PENDENTE
    -- > BITSTREAM (arquivo.bit) = OK
    -- > PROGRAMADO NO KIT AX7010 = OK
    -- > CARREGADO DO FLASH QSPI = NOK



-- testar codigo vhdl na placa direto, depois fazer um testbench
-- clock de 50Mhz real que vem do Oscilador
-- PG_CLK de 50Mhz = pin U18
-- PL led1 = pin M14
-- PL led2 = pin M15
-- PL led3 = pin K16
-- PL led4 = pin J16

library ieee; 
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

--definindo a entidade
entity led_blink is
  port(
    clk_50: in std_logic; -- clock de 50Mhz real que vem do Oscilador
    led1, led2, led3, led4: out std_logic
    );
end led_blink;

-- definindo comportamento da entidade led_blink
architecture behavioral of led_blink is
  signal counter: std_logic_vector (24 downto 0);
  signal clk_1: std_logic; -- clock de 1Hz "para alcançar"


-- o processo definido abaixo, do tipo concorrente
-- monitorar clk_50 e ver SE acontece a 'subida' do clk_50
-- SE OK, entao VERIFICA SE counter < 25mil, que seria
-- 50MHz / 2 = 25MHz no formato em binario
-- SE OK, vai incrementando o "counter"
-- SE NOK, clk_1 RECEBE seu INVERSO
-- e counter vai para ZERO, "000000000000..." 
-- com o "others" que vai 'mandar' zero para counter

begin
  prescaler: process(clk_50)
    begin
      if rising_edge(clk_50) then
        if counter < "1011111010111100001000000" then
          counter <= counter + 1;
        else
          clk_1 <= not clk_1;
          counter <= (others => '0');
        end if;
      end if;
    end process prescaler;
        -- LED ON = '0' nivel logico ZERO
        -- LED OFF = '1' nivel logico UM
        -- desliga leds nao operacionais no PL 
    -- o led1 vai variar de acordo com que chegar no clk_1
    led1 <= clk_1;
    led2 <= not clk_1;
    led3 <= clk_1 xor clk_1;
    led4 <= '1'; 
   


  
end behavioral;
  




  
