`define STRINGIFY(x) `"x`"

`ifdef CS1
`define CS 1
`define CS_ID
`define CS_ID_WIDTH 8
`define CS_EX
`define CS_EX_WIDTH 8
`endif

`ifdef CS2
`define CS 2
`define CS_ID
`define CS_ID_WIDTH 12
`define CS_EX
`define CS_EX_WIDTH 9
`endif
 
`ifdef CS3
`define CS 3
`define CS_ID
`define CS_ID_WIDTH 12
`define CS_EX
`define CS_EX_WIDTH 9
`define CS_WB
`define CS_WB_WIDTH 1
`endif


`ifdef CS4
`define CS 4
`define CS_ID
`define CS_ID_WIDTH 1
`define CS_EX
`define CS_EX_WIDTH 1
`define CS_WB
`define CS_WB_WIDTH 1
`endif

`ifdef CS5
`define CS 5
`define CS_ID
`define CS_ID_WIDTH 12
`define CS_EX
`define CS_EX_WIDTH 10
`define CS_WB
`define CS_WB_WIDTH 1
`endif


`ifdef CS_WB
`define CS_PATCH
`endif

`ifdef CS_EX
`define CS_PATCH
`endif

`ifndef CS_ID_WIDTH
`define CS_ID_WIDTH 0
`endif

`ifndef CS_EX_WIDTH
`define CS_EX_WIDTH 0
`endif

`ifndef CS_WB_WIDTH
`define CS_WB_WIDTH 0
`endif

`define CS_WIDTH `CS_ID_WIDTH + `CS_EX_WIDTH + `CS_WB_WIDTH 
