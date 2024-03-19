`timescale 1ns / 1ps

module patch_mem
#(
    parameter ADDR_WIDTH = 16,
    parameter PATCH_WIDTH = 320
) (
    input logic                     clk_i,
    input logic [ADDR_WIDTH-1:0]    patch_addr_i,
    output logic [PATCH_WIDTH-1:0]   patch_o
);

    string program_path/*verilator public*/;

    integer i;

    localparam bytes = 2**(ADDR_WIDTH-2);
    (* rom_style="{block}" *) reg [PATCH_WIDTH-1:0] mem [bytes];

    // LOAD PATCHES IN MEMORY 
    initial begin: load_patches
        //for (i=0; i<bytes; i++) begin
        //    mem[i] = '0;
        //end
	    $readmemh({program_path,"_c_patches.hex"}, mem);
    end


    // READ PATCH
    always @(negedge clk_i) begin
        patch_o <= mem[patch_addr_i[ADDR_WIDTH-1:2]];
    end
endmodule

