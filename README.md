<h1>myhdl_simple_uart </h1>

<h2>A very simple UART implementation in MyHDL</h2>

<p> This projects implements a simple UART in MyHDL and generates the VHDL files. It has been tested in a DE2-115 board.</p>
<p> It's a - very - simple implementation, I've done it to learn a little bit more about MyHDL. </p>

<p>The project has four files:</p>
<ul>
<li>baudrate_gen.py - generates the baudrate</li>
<li>serial_rx.py - recieves info from RX</li>
<li>serial_tx.py - sends info to TX</li>
<li>tb_serial.py - testbench file</li>
</ul>

<h2> Running the project </h2>

<p> To run the test and generate the VHDL Files go the terminal and execute the command: <strong>py.test tb_serial.py</strong> </p>
<p> You can also edit the tb_serial file and just call the toVHDL instructions </p>

<h2> Vieweing the waveforms </h2>

<p> A bench.vcd file can be generated if you use the TraceSignals function at tb_serial.py, in order to do that you have to comment the VHDL Generation. </p>
<p> You can also run it without py.test, just call the test_bench function directly </p>
