import gradio as gr

from .interactive_block import InteractiveBlock


class TailButtonBlock(InteractiveBlock):
    def __init__(self, body_count: int):
        super().__init__()

        self.prev_warp: gr.Row | None = None
        self.next_warp: gr.Row | None = None
        self.send_warp: gr.Row | None = None

        self._generate_body()
        self.init_btn_visibility(body_count)

    def _generate_body(self):
        with gr.Row(variant="default") as self.body:
            with gr.Row(visible=False) as self.prev_warp:
                btn_prev = gr.Button("返回", min_width=75, scale=1)
                self.interactions.append(btn_prev)
            gr.Column(scale=10, min_width=0)
            with gr.Row(visible=False) as self.next_warp:
                btn_next = gr.Button("繼續", min_width=75, scale=1)
                self.interactions.append(btn_next)
            with gr.Row(visible=False) as self.send_warp:
                btn_send = gr.Button("送出", min_width=75, scale=1, elem_id="sendButton")
                self.interactions.append(btn_send)

    # def set_interactive_triggered(self, user_store: gr.State):
    #     def next_click(_user_store):
    #         _user_store['cur_page'] += 1
    #         return _user_store
    #
    #     def prev_click(_user_store):
    #         _user_store['cur_page'] -= 1
    #         return _user_store
    #
    #     def send_click(_user_store):
    #         _user_store['cur_page'] += 1
    #         return _user_store
    #
    #     to_top_js = """
    #                 function to_top() {
    #                     window.scrollTo(0,0);
    #                 }
    #                 """
    #     self.interactions[0].click(prev_click, inputs=user_store, outputs=user_store, js=to_top_js)
    #     self.interactions[1].click(next_click, inputs=user_store, outputs=user_store, js=to_top_js)
    #     self.interactions[2].click(send_click, inputs=user_store, outputs=user_store, js=to_top_js)

    def init_btn_visibility(self, body_count: int):
        self.next_warp.visible = body_count > 2
        self.send_warp.visible = body_count == 2
