from myhdl import *

t_State = enum('ST_WAIT_START_BIT', 'ST_GET_DATA_BITS', 'ST_GET_STOP_BITS' )


def serial_rx(sysclk, reset_n, n_stop_bits_i, half_baud_rate_tick_i, baud_rate_tick_i, recieve_i, data_o, ready_o):

    """ Serial
    This module implements a reciever serial interface

    Ports:
    -----
    sysclk: sysclk input
    reset_n: reset input
    half_baud_rate_tick_i: half baud rate tick
    baud_rate_tick_i: the baud rate
    n_stop_bits_i: number of stop bits
    recieve_i: rx
    data_o: the data output in 1 byte
    ready_o: indicates data_o is valid
    -----

    """
    END_OF_BYTE = 7
    
    state_reg = Signal(t_State.ST_WAIT_START_BIT)
    state = Signal(t_State.ST_WAIT_START_BIT)

    data_reg = Signal(intbv(0, min = 0, max = 256))
    data = Signal(intbv(0, min = 0, max = 256))
    ready_reg = Signal(bool(0))
    ready = Signal(bool(0))
    
    count_8_bits_reg = Signal(intbv(0, min = 0, max = 8))
    count_8_bits = Signal(intbv(0, min = 0, max = 8))

    count_stop_bits_reg = Signal(intbv(0, min = 0, max = 8))
    count_stop_bits = Signal(intbv(0, min = 0, max = 8))

    @always_comb
    def outputs():
        data_o.next = data_reg
        ready_o.next = ready_reg


    @always_seq(sysclk.posedge, reset = reset_n)
    def sequential_process():
        state_reg.next   = state
        data_reg.next  = data
        ready_reg.next = ready
        count_8_bits_reg.next = count_8_bits
        count_stop_bits_reg.next = count_stop_bits
    
    @always_comb
    def combinational_process():
        state.next  = state_reg
        data.next = data_reg
        ready.next = ready_reg
        count_8_bits.next = count_8_bits_reg
        count_stop_bits.next = count_stop_bits_reg

        if state_reg == t_State.ST_WAIT_START_BIT:
            ready.next = False
            if baud_rate_tick_i == True:
                if recieve_i == False:
                    state.next = t_State.ST_GET_DATA_BITS

        elif state_reg == t_State.ST_GET_DATA_BITS:
            if baud_rate_tick_i == True:
                data.next[count_8_bits_reg] = recieve_i
                if count_8_bits_reg == END_OF_BYTE:
                    count_8_bits.next = 0
                    state.next = t_State.ST_GET_STOP_BITS
                else:
                    count_8_bits.next = count_8_bits_reg + 1
                    state.next = t_State.ST_GET_DATA_BITS
                

        elif state_reg == t_State.ST_GET_STOP_BITS:
            if baud_rate_tick_i == True:
                if count_stop_bits_reg == (n_stop_bits_i - 1):
                    count_stop_bits.next = 0
                    ready.next = True
                    state.next = t_State.ST_WAIT_START_BIT
                else:
                    count_stop_bits.next = count_stop_bits_reg + 1
        else:
            raise ValueError("Undefined State")

            

    return outputs, sequential_process, combinational_process

