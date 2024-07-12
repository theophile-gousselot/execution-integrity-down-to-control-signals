`define STRINGIFY(x) `"x`"

`ifdef CS1
`define CS 1
`define CS_WB
`define CS_WB_WIDTH 1
`define CS_WB_EX
`define CS_WB_EX_WIDTH 1
`endif

`ifdef CS2
`define CS 2
`define CS_ID
`define CS_ID_WIDTH 6
`define CS_EX
`define CS_EX_WIDTH 6
`define CS_WB
`define CS_WB_WIDTH 1
`define CS_WB_EX
`define CS_WB_EX_WIDTH 1
`endif
 
`ifdef CS3
`define CS 3
`define CS_ID
`define CS_ID_WIDTH 17
`define CS_EX
`define CS_EX_WIDTH 9
`define CS_WB
`define CS_WB_WIDTH 1
`define CS_WB_EX
`define CS_WB_EX_WIDTH 1
`endif


`ifdef CS4
`define CS 4
`define CS_ID
`define CS_ID_WIDTH 7
`define CS_EX
`define CS_EX_WIDTH 2
`define CS_WB
`define CS_WB_WIDTH 1
`define CS_WB_EX
`define CS_WB_EX_WIDTH 1
`endif

`ifdef CS5
`define CS 5
`define CS_ID
`define CS_ID_WIDTH 16
`define CS_EX
`define CS_EX_WIDTH 13
`define CS_WB
`define CS_WB_WIDTH 1
`define CS_WB_EX
`define CS_WB_EX_WIDTH 1
`endif

`ifdef CS6
`define CS 6
`define CS_ID
`define CS_ID_WIDTH 1
`define CS_EX
`define CS_EX_WIDTH 1
`define CS_WB
`define CS_WB_WIDTH 1
`define CS_WB_EX
`define CS_WB_EX_WIDTH 1
`endif


`ifdef CS7
`define CS 7
`define CS_ID
`define CS_ID_WIDTH 12
`define CS_EX
`define CS_EX_WIDTH 8
`define CS_WB
`define CS_WB_WIDTH 6
`define CS_WB_EX
`define CS_WB_EX_WIDTH 1
`define CS_WB_LSU
`define CS_WB_LSU_WIDTH 5
`endif

`ifdef CS8
`define CS 8
`define CS_ID
`define CS_ID_WIDTH 1
`define CS_EX
`define CS_EX_WIDTH 1
`define CS_WB
`define CS_WB_WIDTH 1
`define CS_WB_LSU
`define CS_WB_LSU_WIDTH 1
`endif

`ifdef CS9
`define CS 9
`define CS_ID
`define CS_ID_WIDTH 8
`define CS_EX
`define CS_EX_WIDTH 8
`define CS_WB
`define CS_WB_WIDTH 1
`define CS_WB_EX
`define CS_WB_EX_WIDTH 1
`endif

`ifdef CS_WB
`define CS_PATCH
`define CS_CYCPLUS1
`endif

`ifdef CS_EX
`define CS_PATCH
`define CS_CYCPLUS1
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
