import gradio as gr

from survey.blocksV2 import interactive_block


class TailButtonBlock(interactive_block.InteractiveBlock):
    def __init__(self, parent_survey, parent_server):
        super().__init__("", parent_survey, parent_server)
        self.btn_prev: gr.Button | None = None
        self.btn_next: gr.Button | None = None
        self.btn_send: gr.Button | None = None

        self.prev_warp: gr.Row | None = None
        self.next_warp: gr.Row | None = None
        self.send_warp: gr.Row | None = None

        self._generate_body()

    def _generate_body(self):
        with gr.Row() as self.body:
            gr.Column(min_width=0, scale=1)

            with gr.Column(variant="default", scale=3, min_width=640):
                with gr.Row():
                    with gr.Row(visible=False) as self.prev_warp:
                        self.btn_prev = gr.Button("返回", min_width=75, scale=1)
                    gr.Column(scale=10, min_width=0)
                    with gr.Row(visible=(len(self.parent_survey.bodies) > 2)) as self.next_warp:
                        self.btn_next = gr.Button("繼續", min_width=75, scale=1)
                    with gr.Row(visible=(len(self.parent_survey.bodies) == 2)) as self.send_warp:
                        self.btn_send = gr.Button("送出", min_width=75, scale=1, elem_id="sendButton")

            gr.Column(min_width=0, scale=1)

    def set_interactive_triggered(self):
        def next_click(request: gr.Request):
            if request:
                _ip = request.client.host
                _cur = self.server.clients[(self.parent_survey, _ip)].cur_body_index
                if self.parent_survey.bodies[_cur].must_has_done(_ip):
                    self.server.clients[(self.parent_survey, _ip)].set_cur_body(_cur + 1)
                _cur = self.server.clients[(self.parent_survey, _ip)].cur_body_index
                _result = []
                _body_rows = [_p.page for _p in self.parent_survey.bodies]
                for _i, _r in enumerate(_body_rows):
                    if isinstance(_r, gr.Row):
                        _result.append(
                            _r.update(self.server.clients[(self.parent_survey, _ip)].body_visible_states[_i]))
                _result.extend([self.prev_warp.update(_cur > 0 and _cur != len(
                    _body_rows) - 1),
                                self.next_warp.update((_cur < len(
                                    _body_rows) - 2)),
                                self.send_warp.update((_cur == len(
                                    _body_rows) - 2))])
                return _result
            return None

        def prev_click(request: gr.Request):
            if request:
                _ip = request.client.host
                _cur = self.server.clients[(self.parent_survey, _ip)].cur_body_index
                self.server.clients[(self.parent_survey, _ip)].set_cur_body(_cur - 1)
                _cur = self.server.clients[(self.parent_survey, _ip)].cur_body_index
                _result = []
                _body_rows = [_p.page for _p in self.parent_survey.bodies]
                for _i, _r in enumerate(_body_rows):
                    if isinstance(_r, gr.Row):
                        _result.append(
                            _r.update(self.server.clients[(self.parent_survey, _ip)].body_visible_states[_i]))
                _result.extend([self.prev_warp.update(_cur > 0 and _cur != len(
                    _body_rows) - 1),
                                self.next_warp.update((_cur < len(
                                    _body_rows) - 2)),
                                self.send_warp.update((_cur == len(
                                    _body_rows) - 2))])
                return _result
            return None

        def send_click(request: gr.Request):
            if request:
                _ip = request.client.host
                self.server.clients[(self.parent_survey, _ip)].save_response()

                _cur = self.server.clients[(self.parent_survey, _ip)].cur_body_index
                self.server.clients[(self.parent_survey, _ip)].set_cur_body(_cur + 1)
                _cur = self.server.clients[(self.parent_survey, _ip)].cur_body_index
                _result = []
                _body_rows = [_p.page for _p in self.parent_survey.bodies]
                for _i, _r in enumerate(_body_rows):
                    if isinstance(_r, gr.Row):
                        _result.append(
                            _r.update(self.server.clients[(self.parent_survey, _ip)].body_visible_states[_i]))
                _result.extend([self.prev_warp.update(_cur > 0 and _cur != len(
                    _body_rows) - 1),
                                self.next_warp.update((_cur < len(
                                    _body_rows) - 2)),
                                self.send_warp.update((_cur == len(
                                    _body_rows) - 2))])
                return _result
            return None

        _bodies_update = [_p.page for _p in self.parent_survey.bodies]
        _bodies_update.extend([self.prev_warp, self.next_warp, self.send_warp])
        to_top_js = """
                    function to_top() {
                        window.scrollTo(0,0);
                    }
                    """
        self.btn_next.click(next_click, None, outputs=_bodies_update, js=to_top_js)
        self.btn_prev.click(prev_click, None, outputs=_bodies_update, js=to_top_js)
        self.btn_send.click(send_click, None, outputs=_bodies_update, js=to_top_js)
