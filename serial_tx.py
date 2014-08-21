from myhdl import *

t_State = enum('ST_WAIT_START', 'ST_SEND_START_BIT', 'ST_SEND_DATA' , 'ST_SEND_STOP_BIT' )


def serial_tx(sysclk, reset_n, start_i, data_i, n_stop_bits_i, baud_rate_tick_i, transmit_o):

    """ Serial
    This module implements a transmitter serial interface

    Ports:
    -----
    sysclk: sysclk input
    reset_n: reset input
    baud_rate_tick_i: the baud rate
    start_i: start sending data
    data_i: the data to send
    n_stop_bits_i: number of stop bits
    transmit_o: data output
    -----

    """
    END_OF_BYTE = 7
    
    state_reg = Signal(t_State.ST_WAIT_START)
    state = Signal(t_State.ST_WAIT_START)

    transmit_reg = Signal(bool(0))
    transmit = Signal(bool(0))

    count_8_bits_reg = Signal(intbv(0, min = 0, max = 8))
    count_8_bits = Signal(intbv(0, min = 0, max = 8))

    count_stop_bits_reg = Signal(intbv(0, min = 0, max = 8))
    count_stop_bits = Signal(intbv(0, min = 0, max = 8))

    @always_comb
    def outputs():
        transmit_o.next = transmit_reg

    @always_seq(sysclk.posedge, reset = reset_n)
    def sequential_process():
        state_reg.next   = state
        transmit_reg.next  = transmit
        count_8_bits_reg.next = count_8_bits
        count_stop_bits_reg.next = count_stop_bits
    
    @always_comb
    def combinational_process():
        state.next  = state_reg
        transmit.next = transmit_reg
        count_8_bits.next = count_8_bits_reg
        count_stop_bits.next = count_stop_bits_reg

        if state_reg == t_State.ST_WAIT_START:
            transmit.next = True
            if start_i == True:
                state.next = t_State.ST_SEND_START_BIT

        elif state_reg == t_State.ST_SEND_START_BIT:
            transmit.next = False
            if baud_rate_tick_i == True:
                state.next = t_State.ST_SEND_DATA

        elif state_reg == t_State.ST_SEND_DATA:
            transmit.next = data_i[count_8_bits_reg]
            if baud_rate_tick_i == True:
                if count_8_bits_reg == END_OF_BYTE:
                    count_8_bits.next = 0
                    state.next = t_State.ST_SEND_STOP_BIT
                else:
                    count_8_bits.next = count_8_bits_reg + 1
                    state.next = t_State.ST_SEND_DATA
                

        elif state_reg == t_State.ST_SEND_STOP_BIT:
            transmit.next = True
            if baud_rate_tick_i == True:
                if count_stop_bits_reg == (n_stop_bits_i - 1):
                    count_stop_bits.next = 0
                    state.next = t_State.ST_WAIT_START
                else:
                    count_stop_bits.next = count_stop_bits_reg + 1
        else:
            raise ValueError("Undefined State")

            

    return outputs, sequential_process, combinational_process
