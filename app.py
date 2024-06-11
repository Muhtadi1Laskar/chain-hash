import mesop as me

from chain import Chain


@me.stateclass
class State:
    input: str = ""
    chain = Chain()
    data: str
    markle_data = []


def button_click(e: me.ClickEvent):
    state = me.state(State)
    initiate_chain(state.input)


def clear_button(e: me.ClickEvent):
    state = me.state(State)
    state.input = ""
    state.data = ""
    state.chain.empty_list()


def on_input(e: me.InputEvent):
    state = me.state(State)
    state.input = e.value


def initiate_chain(value):
    state = me.state(State)
    state.chain.append(value)
    state.data = state.chain.html_format()
    state.markle_data = state.chain.get_merkle_data()
    


@me.page(
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io"]
    ),
    path="/",
    title="Linked Chain",
)
def app():
    state = me.state(State)

    me.input(
        label="Data",
        on_input=on_input,
        placeholder="Enter the Data",
    )
    me.button("Submit", type="flat", on_click=button_click)
    me.button("Clear", type="flat", on_click=clear_button)

    if isinstance(state.data, str):
        me.markdown(state.data)
    else:
        with me.box(
            style=me.Style(
                display="grid", 
                grid_template_columns="1fr",
                row_gap="5rem",
                justify_items="center",
                justify_content="space-evenly",
                align_content="space-evenly",
                align_items="center"
            )
        ):
            for index, data in enumerate(state.data):
                with me.box(style=me.Style(
                    color="#3572EF",
                    border_radius="10",
                    box_sizing="border-box",
                    background= "#FFFFFF",
                    box_shadow=" 0px 4px 4px rgba(0, 0, 0, 0.25)",
                    width="55rem",
                    justify_content="center",
                    line_height="50px",
                    font_family="sans serif",
                    font_size="17px",
                    font_weight="bold",
                )):
                    me.markdown(data)
