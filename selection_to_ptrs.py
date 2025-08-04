import ida_kernwin
import idc

# Small utility to add a hotkey to convert a selected region to pointers

def to_pointers(widget, tp0, tp1):
    print(f"Converting selection from {tp0.at.toea():x} to {tp1.at.toea():x} in widget {widget}")
    for ea in range(tp0.at.toea(), tp1.at.toea() + 1):
        idc.SetType(ea, "void *")

class selection_to_ptrs_handler_t(ida_kernwin.action_handler_t):
    def activate(self, ctx):
        if ctx.has_flag(ida_kernwin.ACF_HAS_SELECTION):
            to_pointers(ctx.widget, ctx.cur_sel._from, ctx.cur_sel.to)
        return 1

    def update(self, ctx):
        ok_widgets = [
            ida_kernwin.BWN_DISASM
        ]
        return ida_kernwin.AST_ENABLE_FOR_WIDGET \
            if ctx.widget_type in ok_widgets \
            else ida_kernwin.AST_DISABLE_FOR_WIDGET


# -----------------------------------------------------------------------
# create actions (and attach them to IDA View-A's context menu if possible)
ACTION_NAME = "selection_to_ptrs"
ACTION_SHORTCUT = "Ctrl+Shift+S"

if ida_kernwin.unregister_action(ACTION_NAME):
    print("Unregistered previously-registered action \"%s\"" % ACTION_NAME)

if ida_kernwin.register_action(
        ida_kernwin.action_desc_t(
            ACTION_NAME,
            "Selection to Pointers",
            selection_to_ptrs_handler_t(),
            ACTION_SHORTCUT)):
    print("Registered action \"%s\"" % ACTION_NAME)
