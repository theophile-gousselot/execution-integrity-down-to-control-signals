`timescale 1ns / 1ps

`include "macro_def.vh"

module patch_mem
#(
    parameter ADDR_WIDTH = 16,
    parameter PATCH_WIDTH = 320
) (
    input logic                     clk_i,
    input logic [ADDR_WIDTH-1:0]    patch_addr_i,
    output logic [PATCH_WIDTH-1:0]   patch_o
);

`ifdef VERILATOR
    string program_path/*verilator public*/;
`endif

    integer i;

    localparam bytes = 2**(ADDR_WIDTH-2);
    (* rom_style="{block}" *) reg [PATCH_WIDTH-1:0] mem [bytes];

    // LOAD PATCHES IN MEMORY 
    initial begin: load_patches
        //for (i=0; i<bytes; i++) begin
        //    mem[i] = '0;
        //end
`ifdef VERILATOR
`ifdef CS
	    $readmemh({program_path,"_encrypted_cs",`STRINGIFY(`CS),"_patches.mem"}, mem);
`else
	    $readmemh({program_path,"_encrypted_patches.mem"}, mem);
`endif
`else
`ifdef CS
`ifdef CS1
	    $readmemh("program_encrypted_cs1_patches.mem", mem);
`endif
`ifdef CS2
	    $readmemh("program_encrypted_cs2_patches.mem", mem);
`endif
`ifdef CS3
	    $readmemh("program_encrypted_cs3_patches.mem", mem);
`endif
`ifdef CS4
	    $readmemh("program_encrypted_cs4_patches.mem", mem);
`endif
`ifdef CS5
	    $readmemh("program_encrypted_cs5_patches.mem", mem);
`endif
`ifdef CS6
	    $readmemh("program_encrypted_cs6_patches.mem", mem);
`endif
`ifdef CS7
	    $readmemh("program_encrypted_cs7_patches.mem", mem);
`endif
`ifdef CS8
	    $readmemh("program_encrypted_cs8_patches.mem", mem);
`endif
`ifdef CS9
	    $readmemh("program_encrypted_cs9_patches.mem", mem);
`endif
`else
	    $readmemh("program_encrypted_patches.mem", mem);
`endif
`endif
    end


    // READ PATCH
    always @(negedge clk_i) begin
        patch_o <= mem[patch_addr_i[ADDR_WIDTH-1:2]];
    end
endmodule

