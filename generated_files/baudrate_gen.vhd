-----------------------------------------------------------------------------
-- Title : 
-- Project : 
-----------------------------------------------------------------------------
-- File : baudrate_gen.vhd
-- Author : 
-- Company :
-- Created : Thu Aug 21 10:54:44 2014
-- Last update : Thu Aug 21 10:54:44 2014
-- Target Device : Cyclone V
-- Standard : VHDL'93
------------------------------------------------------------------------------
-- Description : 
------------------------------------------------------------------------------
-- Generated with MyHDL Version 0.8
------------------------------------------------------------------------------
-- Copyright : (c) 2014
------------------------------------------------------------------------------
-- Revisions :
-- Date     Version     Author    Description
------------------------------------------------------------------------------

-- Libraries and use clauses


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_08.all;

entity baudrate_gen is
    port (
        sysclk: in std_logic;
        reset_n: in std_logic;
        half_baud_rate_tick_o: out std_logic;
        baud_rate_tick_o: out std_logic
    );
end entity baudrate_gen;
-- Serial
-- This module implements a baudrate generator
-- 
-- Ports:
-- -----
-- sysclk: sysclk input
-- reset_n: reset input
-- baud_rate_i: the baut rate to generate
-- baud_rate_tick_o: the baud rate enable
-- -----

architecture MyHDL of baudrate_gen is


constant half_baud_const: integer := 434;
constant baud_rate_i: integer := 868;



signal baud_gen_count_reg: unsigned(9 downto 0);

begin




BAUDRATE_GEN_SEQUENTIAL_PROCESS: process (sysclk, reset_n) is
begin
    if (reset_n = '0') then
        baud_gen_count_reg <= to_unsigned(0, 10);
        baud_rate_tick_o <= '0';
        half_baud_rate_tick_o <= '0';
    elsif rising_edge(sysclk) then
        baud_gen_count_reg <= (baud_gen_count_reg + 1);
        baud_rate_tick_o <= '0';
        half_baud_rate_tick_o <= '0';
        if (baud_gen_count_reg = baud_rate_i) then
            baud_gen_count_reg <= to_unsigned(0, 10);
            baud_rate_tick_o <= '1';
            half_baud_rate_tick_o <= '1';
        end if;
        if (baud_gen_count_reg = half_baud_const) then
            half_baud_rate_tick_o <= '1';
        end if;
    end if;
end process BAUDRATE_GEN_SEQUENTIAL_PROCESS;

end architecture MyHDL;
