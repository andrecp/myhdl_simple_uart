from myhdl import *

def baudrate_gen(sysclk, reset_n, baud_rate_i, half_baud_rate_tick_o, baud_rate_tick_o):

    """ Serial
    This module implements a baudrate generator

    Ports:
    -----
    sysclk: sysclk input
    reset_n: reset input
    baud_rate_i: the baut rate to generate
    baud_rate_tick_o: the baud rate enable
    -----

    """
    baud_gen_count_reg = Signal(intbv(0, min = 0, max = 900))
    half_baud_const = baud_rate_i//2

    @always_seq(sysclk.posedge, reset = reset_n)
    def sequential_process():
        baud_gen_count_reg.next = baud_gen_count_reg + 1
        baud_rate_tick_o.next = 0
        half_baud_rate_tick_o.next = 0
        if baud_gen_count_reg == baud_rate_i:
            baud_gen_count_reg.next = 0
            baud_rate_tick_o.next = 1 
        if baud_gen_count_reg == half_baud_const:
            half_baud_rate_tick_o.next = 1 
    

    return sequential_process
