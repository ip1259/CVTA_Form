import gradio as gr
from survey.themes.themes import SurveyTheme
import survey.blocks as s_blocks
import survey.pages as s_pages


class SurveySystemManager:

    def __init__(self):
        self._gui: gr.Blocks | None = None
        self._theme_items = ["EMB"]
        self.main_gui()
        # set self.gui

    def start_manager(self):
        self._gui.launch()

    def main_gui(self):
        DEFAULT_THEME = SurveyTheme.EMB_THEME, SurveyTheme.EMB_CSS, SurveyTheme.JS
        with gr.Blocks(theme=DEFAULT_THEME[0], css=DEFAULT_THEME[1], js=DEFAULT_THEME[2]) as self._gui:
            with gr.Tab("問卷生成器"):
                _survey_maker_state = gr.State({"survey_id": "None", "survey_theme": "EMB", "heads": [], "bodies": [],
                                                "tail": {"page_type": "tail_btn"}})
                with gr.Row():
                    with gr.Column(scale=2, min_width=640):
                        _sid = gr.Textbox(interactive=True, label="問卷 ID",
                                          placeholder="問卷ID 通常設為課程代碼，如:113F01")

                        def _sid_change(value, data):
                            data["survey_id"] = value
                            return data

                        _sid.change(_sid_change, [_sid, _survey_maker_state], [_survey_maker_state])

                        _themes = gr.Dropdown(self._theme_items, label="問卷色彩主題", info="問卷的配色主題，隨便選即可")

                        def _themes_selected(value, data):
                            data["survey_theme"] = value
                            return data
                        _themes.select(_themes_selected, [_themes, _survey_maker_state], [_survey_maker_state])

                        with gr.Accordion("問卷頭版"):
                            gr.Markdown("**不會隨著問卷換頁的區塊**")
                            with gr.Column():
                                @gr.render(inputs=[_survey_maker_state],
                                           triggers=[_survey_maker_state.change])
                                def _load_heads_input(data):
                                    __heads = data['heads']
                                    for i, p in enumerate(__heads):
                                        with gr.Row():
                                            _h_index = gr.Number(i, container=False, interactive=False, min_width=0,
                                                                 scale=1)
                                            _h_ptype = gr.Dropdown(["head"], value=p["page_type"], container=False,
                                                                   scale=3)

                                            def _h_page_type_selected(index, value, _data):
                                                if value == 'head':
                                                    _data['heads'][index]["page_type"] = value
                                                    return _data

                                            _h_ptype.select(_h_page_type_selected,
                                                            [_h_index, _h_ptype, _survey_maker_state],
                                                            [_survey_maker_state])
                                            if p["page_type"] == "head":
                                                _h_title = gr.Textbox(p['title'], max_lines=1, label="title",
                                                                      container=False,
                                                                      placeholder="OOO班 教師滿意度調查", scale=6)

                                                def _h_title_change(index, value, _data):
                                                    _data['heads'][index]["title"] = value
                                                    return _data

                                                _h_title.change(_h_title_change,
                                                                [_h_index, _h_title, _survey_maker_state],
                                                                [_survey_maker_state])

                                                _h_desc = gr.Textbox((p['desc'] if 'desc' in p.keys() else ""),
                                                                     max_lines=1, placeholder="說明文字, 選填",
                                                                     container=False, scale=5)

                                                def _h_desc_change(index, value, _data):
                                                    _data['heads'][index]["desc"] = value
                                                    return _data

                                                _h_desc.change(_h_desc_change,
                                                               [_h_index, _h_desc, _survey_maker_state],
                                                               [_survey_maker_state])
                                                _remove_btn = gr.ClearButton(value="-", scale=1)

                                                def _remove_head_click(index, _data):
                                                    _data["heads"].pop(index)
                                                    return _data

                                                _remove_btn.click(_remove_head_click, [_h_index, _survey_maker_state],
                                                                  [_survey_maker_state])

                                with gr.Row():
                                    _heads = _survey_maker_state.value['heads']
                                    _h_index = gr.Number(len(_heads), interactive=False, min_width=20,
                                                         container=False, scale=1)

                                    def _h_index_update(_data):
                                        return len(_data['heads'])

                                    _survey_maker_state.change(_h_index_update, [_survey_maker_state], [_h_index])
                                    _h_ptype = gr.Dropdown(["head"], container=False, min_width=20, scale=3)

                                    with gr.Column(scale=12):
                                        with gr.Row():
                                            @gr.render(inputs=[_h_ptype], triggers=[_h_ptype.change])
                                            def _last_h_type_changed(_value):
                                                if _value == "head":
                                                    _last_h_title = gr.Textbox("", max_lines=1,
                                                                               placeholder="OOO班 教師滿意度調查",
                                                                               container=False, min_width=20, scale=6)
                                                    _last_h_desc = gr.Textbox("", max_lines=1,
                                                                              placeholder="說明文字, 選填",
                                                                              container=False,
                                                                              min_width=20, scale=5)
                                                    _last_h_add_btn = gr.Button(value="+", variant="stop", size="sm",
                                                                                min_width=20, scale=1)

                                                    def _last_h_add_btn_click(_type, _title, _desc, _data):
                                                        if _title is None or _title == "":
                                                            return _data
                                                        _data["heads"].append({"page_type": _type, "title": _title})
                                                        if len(_desc) != 0:
                                                            _data["heads"][-1]["desc"] = _desc
                                                        return [len(_data["heads"]), None, "", "", _data]

                                                    _last_h_add_btn.click(_last_h_add_btn_click,
                                                                          [_h_ptype, _last_h_title, _last_h_desc,
                                                                           _survey_maker_state],
                                                                          [_h_index, _h_ptype, _last_h_title,
                                                                           _last_h_desc, _survey_maker_state])

                        with gr.Accordion("問卷題目區"):
                            gr.Markdown("**會隨著問卷換頁的答題區塊**")
                            with gr.Column():
                                @gr.render(inputs=[_survey_maker_state],
                                           triggers=[_survey_maker_state.change])
                                def _load_heads_input(data):
                                    __bodies = data['bodies']
                                    for i, p in enumerate(__bodies):
                                        with gr.Row():
                                            _b_index = gr.Number(i, container=False, interactive=False, min_width=0,
                                                                 scale=1)
                                            _b_ptype = gr.Dropdown(["teacher", "ta", "employment", "finish"],
                                                                   value=p["page_type"], container=False,
                                                                   scale=3)

                                            def _b_page_type_selected(index, value, _data):
                                                if value is not None:
                                                    _data['bodies'][index]["page_type"] = value
                                                    return _data

                                            _b_ptype.select(_b_page_type_selected,
                                                            [_b_index, _b_ptype, _survey_maker_state],
                                                            [_survey_maker_state])
                                            match p["page_type"]:
                                                case "teacher":
                                                    _b_teacher = gr.Textbox(p['teacher'], max_lines=1, container=False,
                                                                            scale=6)

                                                    def _b_teacher_change(index, value, _data):
                                                        _data['bodies'][index]["teacher"] = value
                                                        return _data

                                                    _b_teacher.change(_b_teacher_change,
                                                                      [_b_index, _b_teacher, _survey_maker_state],
                                                                      [_survey_maker_state])

                                                    _b_desc = gr.Textbox((p['desc'] if 'desc' in p.keys() else ""),
                                                                         max_lines=1, placeholder="課程, 選填",
                                                                         container=False, scale=5)

                                                    def _b_desc_change(index, value, _data):
                                                        _data['bodies'][index]["desc"] = value
                                                        return _data

                                                    _b_desc.change(_b_desc_change,
                                                                   [_b_index, _b_desc, _survey_maker_state],
                                                                   [_survey_maker_state])
                                                    _remove_btn = gr.ClearButton(value="-", scale=1)

                                                    def _remove_body_click(index, _data):
                                                        _data["bodies"].pop(index)
                                                        return _data

                                                    _remove_btn.click(_remove_body_click,
                                                                      [_b_index, _survey_maker_state],
                                                                      [_survey_maker_state])

                                                case "ta":
                                                    _remove_btn = gr.ClearButton(value="-", scale=1)

                                                    def _remove_body_click(index, _data):
                                                        _data["bodies"].pop(index)
                                                        return _data

                                                    _remove_btn.click(_remove_body_click,
                                                                      [_b_index, _survey_maker_state],
                                                                      [_survey_maker_state])

                                                case "employment":
                                                    _remove_btn = gr.ClearButton(value="-", scale=1)

                                                    def _remove_body_click(index, _data):
                                                        _data["bodies"].pop(index)
                                                        return _data

                                                    _remove_btn.click(_remove_body_click,
                                                                      [_b_index, _survey_maker_state],
                                                                      [_survey_maker_state])

                                                case "finish":
                                                    _remove_btn = gr.ClearButton(value="-", scale=1)

                                                    def _remove_body_click(index, _data):
                                                        _data["bodies"].pop(index)
                                                        return _data

                                                    _remove_btn.click(_remove_body_click,
                                                                      [_b_index, _survey_maker_state],
                                                                      [_survey_maker_state])

                                with gr.Row():
                                    _bodies = _survey_maker_state.value['bodies']
                                    _b_index = gr.Number(len(_bodies), interactive=False, min_width=20,
                                                         container=False, scale=1)

                                    def _b_index_update(_data):
                                        return len(_data['bodies'])

                                    _survey_maker_state.change(_b_index_update, [_survey_maker_state], [_b_index])
                                    _b_ptype = gr.Dropdown(["teacher", "ta", "employment", "finish"], container=False,
                                                           min_width=20, scale=3)

                                    with gr.Column(scale=12):
                                        with gr.Row():
                                            @gr.render(inputs=[_b_ptype], triggers=[_b_ptype.change])
                                            def _last_b_type_changed(_value):
                                                if _value == "teacher":
                                                    _last_b_teacher = gr.Textbox("", max_lines=1,
                                                                                 container=False, min_width=20, scale=6)
                                                    _last_b_desc = gr.Textbox("", max_lines=1,
                                                                              placeholder="課程, 選填",
                                                                              container=False,
                                                                              min_width=20, scale=5)
                                                    _last_b_add_btn = gr.Button(value="+", variant="stop", size="sm",
                                                                                min_width=20, scale=1)

                                                    def _last_b_add_btn_click(_type, _teacher, _desc, _data):
                                                        if _teacher is None or _teacher == "":
                                                            return _data
                                                        _data["bodies"].append(
                                                            {"page_type": _type, "teacher": _teacher})
                                                        if len(_desc) != 0:
                                                            _data["bodies"][-1]["desc"] = _desc
                                                        return [len(_data["bodies"]), None, "", "", _data]

                                                    _last_b_add_btn.click(_last_b_add_btn_click,
                                                                          [_b_ptype, _last_b_teacher, _last_b_desc,
                                                                           _survey_maker_state],
                                                                          [_b_index, _b_ptype, _last_b_teacher,
                                                                           _last_b_desc, _survey_maker_state])

                                                if _value in ["ta", "employment", "finish"]:
                                                    _last_b_add_btn = gr.Button(value="+", variant="stop", size="sm",
                                                                                min_width=20, scale=1)

                                                    def _last_b_add_btn_click(_type, _data):
                                                        _data["bodies"].append(
                                                            {"page_type": _type})
                                                        return [len(_data["bodies"]), None, _data]

                                                    _last_b_add_btn.click(_last_b_add_btn_click,
                                                                          [_b_ptype, _survey_maker_state],
                                                                          [_b_index, _b_ptype, _survey_maker_state])

                    with gr.Column(scale=1, min_width=0, variant="compact"):
                        @gr.render(inputs=[_survey_maker_state], triggers=[_survey_maker_state.change])
                        def generate_survey(data):
                            gr.Json(data)


if __name__ == '__main__':
    ssm = SurveySystemManager()
    ssm.start_manager()
