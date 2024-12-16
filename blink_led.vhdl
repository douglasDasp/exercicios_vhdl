library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- 16/12/2024
-- Douglas Poubel
-- arquivo de teste basico de portas logicas no VIVADO
-- e kit ALINX AX7010

-- declara entradas IN e saida OUT
entity blink_led is
    port (
            f1,f2: in std_logic; 
            a: out std_logic_vector(3 downto 0));
end blink_led;

architecture Behavioral of blink_led is

begin
    -- declara o comportamento de IN e saida OUT
    -- tem que colocar (f1,f2) pois o codigo interno do process
    -- é sensivel a eles, 'necessitam de f1 e f2'
    process(f1,f2) 
    begin
        a(0) <= f1 or f2; -- teste OR
        a(1) <= f1 and f2; -- teste AND
        a(2) <= f1 xor f2; -- teste XOR
        a(3) <= f1 nand f2; -- teste NAND
    end process;

end Behavioral;



-- ## ARQUIVO DE TESTEBENCH, COLOCAR EM SEPARADO, no arquivo para teste 
-- de simulacao do circuito digital  16/12/2024
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity blink_led_tb is
--  Port ( );
end blink_led_tb;

architecture Behavioral of blink_led_tb is

constant PER: time := 100 ns;
-- sinais a ser testado
signal f1_tb: std_logic := '0';
signal f2_tb: std_logic := '0';
signal a_tb: std_logic_vector(3 downto 0); 

-- componente a ser testado

component blink_led is
    port(
        f1: in std_logic;
        f2: in std_logic;
        a: out std_logic_vector(3 downto 0));
    end component;  


begin

-- port map da unidade a ser testada
-- o sinal_tb(a ser testado) é conectado
-- ao 'dispositivo' real logico criado no outro arquivo
uut : blink_led
    port map(
            f1 => f1_tb,
            f2 => f2_tb,
            a => a_tb);

-- estimulo de teste   
process
begin
    f1_tb <= '1';
    f2_tb <= '1';
    wait for PER/2;
    f1_tb <= '0';
    wait for PER/2;
    f1_tb <= '1';
    wait for PER/2;
    f1_tb <= '0';
    
end process;    


end Behavioral;


-- ARQUIVO blink_led.xdc, responsavel por conectar a lOGICA
-- do algoritmo HDL com as portas do CHIP programado
--
set_property IOSTANDARD LVCMOS33 [get_ports {a[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {a[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {a[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {a[0]}]
set_property PACKAGE_PIN J16 [get_ports {a[0]}]
set_property PACKAGE_PIN K16 [get_ports {a[1]}]
set_property PACKAGE_PIN M15 [get_ports {a[2]}]
set_property PACKAGE_PIN M14 [get_ports {a[3]}]

