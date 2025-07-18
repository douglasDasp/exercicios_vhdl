-- programa de teste para gerar 4 clocks diferentes freq.
-- para piscar 1 led em 4 frequencias diferentes selecionadas no MUX
-- retirado do site  https://nandland.com/your-first-vhdl-program-an-led-blinker/
-- TESTAR na pratica no devKit ZCU102



library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
 
entity tutorial_led_blink is
  port (
    i_clock      : in  std_logic;
    i_enable     : in  std_logic;
    i_switch_1   : in  std_logic;
    i_switch_2   : in  std_logic;
    o_led_drive  : out std_logic
    );
end tutorial_led_blink;
 
architecture rtl of tutorial_led_blink is
 
  -- Constants to create the frequencies needed:
  -- Formula is: (25 MHz / 100 Hz * 50% duty cycle)
  -- So for 100 Hz: 25,000,000 / 100 * 0.5 = 125,000
  constant c_CNT_100HZ : natural := 125000;
  constant c_CNT_50HZ  : natural := 250000;
  constant c_CNT_10HZ  : natural := 1250000;
  constant c_CNT_1HZ   : natural := 12500000;

  -- These signals will be the counters:
  signal r_CNT_100HZ : natural range 0 to c_CNT_100HZ;
  signal r_CNT_50HZ  : natural range 0 to c_CNT_50HZ;
  signal r_CNT_10HZ  : natural range 0 to c_CNT_10HZ;
  signal r_CNT_1HZ   : natural range 0 to c_CNT_1HZ;
   
  -- These signals will toggle at the frequencies needed:
  signal r_TOGGLE_100HZ : std_logic := '0';
  signal r_TOGGLE_50HZ  : std_logic := '0';
  signal r_TOGGLE_10HZ  : std_logic := '0';
  signal r_TOGGLE_1HZ   : std_logic := '0';
 
  -- One bit select wire.
  signal w_LED_SELECT : std_logic;

begin
 
  -- All processes toggle a specific signal at a different frequency.
  -- They all run continuously even if the switches are
  -- not selecting their particular output.

  -- explicação dos codigos nos blocos de process
  -- o clock principal é o i_clock que vem do hardware usado 
  -- no momento, como o de OSCilador a 50MHZ
  -- é um clock rápido, então a cada subida de clock "rising_edge(i_clock)
  -- o "IF 1" acontece, de forma "infinita", enquanto i_clock ativo
  -- o "IF 2" testa se o valo da constante atual é igual a constante final
  -- a atual começa em 0 (no exemplo p_100_HZ) 
  -- e vai até (c_CNT_100HZ - 1) = 125000 - 1 (FIM DA CONTAGEM NESSE CLOCK 100HZ)
  -- desta forma, a interação fica no "else" de 0 até 12498
  -- incrementando o r_CNT_100HZ. 0, 1, 2, 3, 4... 12498
  -- ao chegar no 12499, o IF 2 acontece, o r_TOGGLE_100HZ INVERTE SEU NIVEL LOGICO
  -- e o contador r_CNT_100HZ volta pra ZERO
  -- e assim se repete a contagem novamente

  -- i_clock = 50MHZ = 25 000 000 
   
  p_100_HZ : process (i_clock) is
  begin
    if rising_edge(i_clock) then
      if r_CNT_100HZ = c_CNT_100HZ-1 then  -- -1, since counter starts at 0
        r_TOGGLE_100HZ <= not r_TOGGLE_100HZ;
        r_CNT_100HZ    <= 0;
      else
        r_CNT_100HZ <= r_CNT_100HZ + 1;
      end if;
    end if;
  end process p_100_HZ;

p_50_HZ : process (i_clock) is
  begin
    if rising_edge(i_clock) then
      if r_CNT_50HZ = c_CNT_50HZ-1 then  -- -1, since counter starts at 0
        r_TOGGLE_50HZ <= not r_TOGGLE_50HZ;
        r_CNT_50HZ    <= 0;
      else
        r_CNT_50HZ <= r_CNT_50HZ + 1;
      end if;
    end if;
  end process p_50_HZ;
     
p_10_HZ : process (i_clock) is
 begin
    if rising_edge(i_clock) then
      if r_CNT_10HZ = c_CNT_10HZ-1 then  -- -1, since counter starts at 0
        r_TOGGLE_10HZ <= not r_TOGGLE_10HZ;
        r_CNT_10HZ    <= 0;
      else
        r_CNT_10HZ <= r_CNT_10HZ + 1;
      end if;
    end if;
  end process p_10_HZ;
 
   
  p_1_HZ : process (i_clock) is
  begin
    if rising_edge(i_clock) then
      if r_CNT_1HZ = c_CNT_1HZ-1 then  -- -1, since counter starts at 0
        r_TOGGLE_1HZ <= not r_TOGGLE_1HZ;
        r_CNT_1HZ    <= 0;
      else
        r_CNT_1HZ <= r_CNT_1HZ + 1;
      end if;
    end if;
  end process p_1_HZ;

  -- Create a multiplexor based on switch inputs
  w_LED_SELECT <= r_TOGGLE_100HZ when (i_switch_1 = '0' and i_switch_2 = '0') else
                  r_TOGGLE_50HZ  when (i_switch_1 = '0' and i_switch_2 = '1') else
                  r_TOGGLE_10HZ  when (i_switch_1 = '1' and i_switch_2 = '0') else
                  r_TOGGLE_1HZ;
 
   
  -- Only allow o_led_drive to drive when i_enable is high (and gate).
  o_led_drive <= w_LED_SELECT and i_enable;
 
end rtl;

      


      


   
