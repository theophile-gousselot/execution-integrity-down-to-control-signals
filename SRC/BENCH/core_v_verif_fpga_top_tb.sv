`timescale 1ns / 1ps

module core_v_verif_fpga_top_tb ();
	logic              clk_core_slow_s = 1;
	logic              clk_ascon_fast_s = 1;
	logic              rst_s;
	logic [7:0]        led_s;
    
    int unsigned       maxcycles_int = 4096;
    int unsigned       clk_core_slow_cyc_cnt_int = 0;
 

    always begin : clk_core_slow_s_generation
        #5 clk_core_slow_s = 0;
        #5 clk_core_slow_s = 1;
        clk_core_slow_cyc_cnt_int = clk_core_slow_cyc_cnt_int + 1;
    end : clk_core_slow_s_generation

    always begin : clk_ascon_fast_s_generation
        #5 clk_ascon_fast_s = 0;
        #5 clk_ascon_fast_s = 1;
    end : clk_ascon_fast_s_generation

    initial begin : rst_s_generation
        rst_s = 0;
        #97 rst_s = 1;
    end : rst_s_generation

    always begin : time_out
        if (clk_core_slow_cyc_cnt_int >= maxcycles_int) begin
			$display("%m @ %0t ps / %0d cycles: MAXIMUM CYCLE LIMIT", $time, clk_core_slow_cyc_cnt_int);
			$finish;
		end
    end

    core_v_verif_fpga_top core_v_verif_fpga_top_i (
        .clk_core_slow_i(clk_core_slow_s),
        .clk_ascon_fast_i(clk_ascon_fast_s),
        .rst_i(rst_s),
        .led_o(led_s)
    );

endmodule
