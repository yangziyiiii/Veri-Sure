// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Tracing implementation internals

#include "verilated_vcd_c.h"
#include "Vtb__Syms.h"


void Vtb___024root__trace_chg_0_sub_0(Vtb___024root* vlSelf, VerilatedVcd::Buffer* bufp);

void Vtb___024root__trace_chg_0(void* voidSelf, VerilatedVcd::Buffer* bufp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb___024root__trace_chg_0\n"); );
    // Body
    Vtb___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vtb___024root*>(voidSelf);
    Vtb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    if (VL_UNLIKELY(!vlSymsp->__Vm_activity)) return;
    Vtb___024root__trace_chg_0_sub_0((&vlSymsp->TOP), bufp);
}

void Vtb___024root__trace_chg_0_sub_0(Vtb___024root* vlSelf, VerilatedVcd::Buffer* bufp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb___024root__trace_chg_0_sub_0\n"); );
    Vtb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    VlWide<5>/*159:0*/ __Vtemp_3;
    // Body
    uint32_t* const oldp VL_ATTR_UNUSED = bufp->oldp(vlSymsp->__Vm_baseCode + 1);
    if (VL_UNLIKELY((vlSelfRef.__Vm_traceActivity[1U]))) {
        __Vtemp_3[0U] = vlSelfRef.tb__DOT__stats1__BRA__31__03a0__KET__;
        __Vtemp_3[1U] = vlSelfRef.tb__DOT__stats1__BRA__63__03a32__KET__;
        __Vtemp_3[2U] = vlSelfRef.tb__DOT__stats1__BRA__95__03a64__KET__;
        __Vtemp_3[3U] = (IData)((((QData)((IData)(vlSelfRef.tb__DOT__stats1__BRA__159__03a128__KET__)) 
                                  << 0x00000020U) | (QData)((IData)(vlSelfRef.tb__DOT__stats1__BRA__127__03a96__KET__))));
        __Vtemp_3[4U] = (IData)(((((QData)((IData)(vlSelfRef.tb__DOT__stats1__BRA__159__03a128__KET__)) 
                                   << 0x00000020U) 
                                  | (QData)((IData)(vlSelfRef.tb__DOT__stats1__BRA__127__03a96__KET__))) 
                                 >> 0x00000020U));
        bufp->chgWData(oldp+0,(__Vtemp_3),160);
    }
    bufp->chgBit(oldp+5,(vlSelfRef.tb__DOT__clk));
    bufp->chgBit(oldp+6,(vlSelfRef.tb__DOT__in));
    bufp->chgBit(oldp+7,((1U & (~ (IData)(vlSelfRef.tb__DOT__in)))));
}

void Vtb___024root__trace_cleanup(void* voidSelf, VerilatedVcd* /*unused*/) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtb___024root__trace_cleanup\n"); );
    // Body
    Vtb___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vtb___024root*>(voidSelf);
    Vtb__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    vlSymsp->__Vm_activity = false;
    vlSymsp->TOP.__Vm_traceActivity[0U] = 0U;
    vlSymsp->TOP.__Vm_traceActivity[1U] = 0U;
}
