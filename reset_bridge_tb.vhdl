library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
library UNISIM;
use UNISIM.VComponents.all;

entity reset_bridge_tb is
--  Port ( );
end reset_bridge_tb;

architecture Behavioral of reset_bridge_tb is

constant periodo : time := 100 ns;

--sinais a serem testados
signal clk_tb : std_logic := '0';
signal rst_i_tb : std_logic := '0';
signal rst_o_tb : std_logic;

--componente de HW a ser testado
component reset_bridge is
    port(clk_dst : in std_logic;
         rst_in : in std_logic;
         rst_out : out std_logic);
end component;


--Unit Under test definida
uut : reset_bridge
    port map(clk_dst => clk_tb, rst_in => rst_i_tb, rst_out => rst_o_tb);
    
              
begin

process
    begin
        clk_tb <= '1';
        wait for periodo/2;
        clk_tb <= '0';
        wait for periodo/2;
    end process;

   




end Behavioral;
