library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity reset_bridge is
    Port ( clk_dst : in STD_LOGIC;
           rst_in : in STD_LOGIC;
           rst_out : out STD_LOGIC);
end reset_bridge;

architecture Behavioral of reset_bridge is

begin
    process(clk_dst, rst_in)
        variable rst_meta : std_logic := 'U';
    begin
        if rst_in = '1' then 
            rst_meta := '1';
            rst_out <= '1';
        elsif (rising_edge(clk_dst)) then
            rst_out <= rst_meta;
            rst_meta := '0';
        end if;

    end process;

end Behavioral;
