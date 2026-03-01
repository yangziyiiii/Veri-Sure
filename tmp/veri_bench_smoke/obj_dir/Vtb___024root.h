// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtb.h for the primary calling header

#ifndef VERILATED_VTB___024ROOT_H_
#define VERILATED_VTB___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class Vtb__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtb___024root final {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ tb__DOT__wavedrom_enable;
    CData/*0:0*/ tb__DOT__clk;
    CData/*0:0*/ tb__DOT__in;
    CData/*0:0*/ __Vtrigprevexpr___TOP__tb__DOT__clk__0;
    IData/*31:0*/ tb__DOT__stats1__BRA__159__03a128__KET__;
    IData/*31:0*/ tb__DOT__stats1__BRA__127__03a96__KET__;
    IData/*31:0*/ tb__DOT__stats1__BRA__95__03a64__KET__;
    IData/*31:0*/ tb__DOT__stats1__BRA__63__03a32__KET__;
    IData/*31:0*/ tb__DOT__stats1__BRA__31__03a0__KET__;
    VlWide<16>/*511:0*/ tb__DOT__wavedrom_title;
    IData/*31:0*/ tb__DOT__wavedrom_hide_after_time;
    IData/*31:0*/ __VactIterCount;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;
    VlUnpacked<CData/*0:0*/, 2> __Vm_traceActivity;
    VlDelayScheduler __VdlySched;
    VlTriggerScheduler __VtrigSched_hf558b736__0;
    VlTriggerScheduler __VtrigSched_hf558b577__0;

    // INTERNAL VARIABLES
    Vtb__Syms* vlSymsp;
    const char* vlNamep;

    // CONSTRUCTORS
    Vtb___024root(Vtb__Syms* symsp, const char* namep);
    ~Vtb___024root();
    VL_UNCOPYABLE(Vtb___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
