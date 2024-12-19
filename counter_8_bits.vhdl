 exemplo retirado do canal TKJ electronics 
--
-- data: 18/12/2024
--
--


library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

entity main is 
	port(
		clk: in std_logic;
		reset: in std_logic;
		led: out std_logic_vector(7 downto 0)
	);
	
	

architecture behavioral of main is	
	
	signal counter: std_logic_vector(7 downto 0);
	signal prescaler: std_logic_vector(22 downto 0);


begin

		counterProcess:process(reset, clk)
		begin
			if rising_edge(clk) then
				if reset = '1' then
					prescaler <= (others => '0'); --'000 ... 000'
					counter <= (others => '0');--'00000000'
				else
					if prescaler < "1100001101010000" then --25MHz 
						prescaler <= prescaler + 1;
					else
						prescaler <= (others => '0');
						counter <= counter + 1;
					end if;	
				end if;
			end if;	
		end process; 

		led <= counter; 
		
end behavioral; 
