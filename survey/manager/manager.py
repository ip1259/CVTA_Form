import gradio as gr
from survey.themes.themes import SurveyTheme
from survey.pages import PageParser
import json
import os


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
        TEACHERS = ["孔令文", "宋隆佑", "簡進士", "陳柄宏", "林宜芳", "陳冠華", "吳威錫", "吳佳鑫", "吳秉霖", "李淑如",
                    "林瓊嘉", "王綉蘭", "洪綉雯"]
        with gr.Blocks(theme=DEFAULT_THEME[0], css=DEFAULT_THEME[1], js=DEFAULT_THEME[2]) as self._gui:
            with gr.Tab("問卷管理"):
                _survey_list = gr.State()
                _path = os.getcwd()
                _path = os.path.join(_path, "Surveys")
                _files = os.listdir(_path)
                # print(_files)
                _survey_files = []
                for _f in _files:
                    if _f.split('.')[-1] in ["sr", "disable"]:
                        print(os.path.join(_path, _f))
                        _survey_files.append(os.path.join(_path, _f))
                _survey_list.value = _survey_files
                _refresh_btn = gr.Button("讀取問卷清單")

                @gr.render(inputs=[_survey_list], triggers=[_refresh_btn.click])
                def refresh_surveys(data):
                    for f in data:
                        _sur_switch = gr.Checkbox(value=True if f.rsplit(".", 2)[1] == "sr" else False,
                                                  label=f.rsplit(".", 2)[0])

                        def _sf_change(value, data):
                            __f = f.rsplit(".", 2)[0]
                            if value:
                                _old = __f + ".disable"
                                _new = __f + ".sr"
                                os.rename(_old, _new)
                                data.remove(_old)
                                data.append(_new)
                            else:
                                _old = __f + ".sr"
                                _new = __f + ".disable"
                                os.rename(_old, _new)
                                data.remove(_old)
                                data.append(_new)
                            return data

                        _sur_switch.change(_sf_change, [_sur_switch, _survey_list], [_survey_list])

            with gr.Tab("問卷生成器-簡易"):
                _survey_maker_state_basic = gr.State(
                    {"survey_id": "None", "survey_theme": "EMB", "heads": [], "bodies": [],
                     "tail": {"page_type": "tail_btn"}})
                with gr.Row():
                    with gr.Column(scale=2):
                        def update_survey_maker_data(data):
                            __data = data[_survey_maker_state_basic]
                            if _e_s_id in data.keys():
                                __data['survey_id'] = data[_e_s_id]
                            if _e_s_themes in data.keys():
                                __data['survey_theme'] = data[_e_s_themes]
                            if _e_s_class in data.keys():
                                if len(__data['heads']) == 0:
                                    __data['heads'].append(
                                        {"page_type": "head", "title": data[_e_s_class] + " 教師滿意度調查"})
                                else:
                                    __data['heads'][0]['title'] = data[_e_s_class] + " 教師滿意度調查"
                            if _e_s_has_ta in data.keys():
                                if {'page_type': 'ta'} in __data["bodies"]:
                                    if not data[_e_s_has_ta]:
                                        __data["bodies"].remove({'page_type': 'ta'})
                                else:
                                    if data[_e_s_has_ta]:
                                        __data["bodies"].append({'page_type': 'ta'})

                            if _e_s_teachers in data.keys() and _e_s_other_teachers in data.keys():
                                selected_teacher = data[_e_s_teachers]
                                for i in range(len(__data["bodies"]) - 1, -1, -1):
                                    if __data["bodies"][i]['page_type'] == "teacher":
                                        __data["bodies"].pop(i)
                                for teacher in selected_teacher:
                                    __data["bodies"].append({'page_type': 'teacher', 'teacher': teacher})

                                other_teachers = [t.strip() for t in data[_e_s_other_teachers].split(",")]
                                for teacher in other_teachers:
                                    if teacher != "":
                                        __data["bodies"].append({'page_type': 'teacher', 'teacher': teacher})
                            return __data

                        def on_survey_maker_data_change(data):
                            if {'page_type': 'employment'} in data["bodies"]:
                                data["bodies"].remove({'page_type': 'employment'})
                            data["bodies"].append({'page_type': 'employment'})
                            if {'page_type': 'ta'} in data["bodies"]:
                                data["bodies"].remove({'page_type': 'ta'})
                                data["bodies"].append({'page_type': 'ta'})
                            if {'page_type': 'finish'} in data["bodies"]:
                                data["bodies"].remove({'page_type': 'finish'})
                            data["bodies"].append({'page_type': 'finish'})
                            return data

                        _e_s_id = gr.Textbox(interactive=True, label="問卷 ID", max_lines=1,
                                             placeholder="問卷ID 通常設為課程代碼，如:113F01")
                        _e_s_themes = gr.Dropdown(self._theme_items, label="問卷色彩主題",
                                                  info="問卷的配色主題，隨便選即可")
                        _e_s_class = gr.Textbox("", max_lines=1, label="班級名稱", placeholder="OOO班")
                        _e_s_has_ta = gr.Checkbox(False, label="是否有助教")
                        _e_s_teachers = gr.CheckboxGroup(TEACHERS, label="任課老師")
                        _e_s_other_teachers = gr.Textbox("", label="其他老師", info="以 , 區隔",
                                                         placeholder="000, 111, 222...")
                        _e_s_generate_button = gr.Button("Preview", elem_id="sendButton")

                        _e_s_id.change(update_survey_maker_data,
                                       inputs={_e_s_id, _survey_maker_state_basic},
                                       outputs=[_survey_maker_state_basic])
                        _e_s_themes.change(update_survey_maker_data,
                                           inputs={_e_s_themes, _survey_maker_state_basic},
                                           outputs=[_survey_maker_state_basic])
                        _e_s_class.change(update_survey_maker_data,
                                          inputs={_e_s_class, _survey_maker_state_basic},
                                          outputs=[_survey_maker_state_basic])
                        _e_s_has_ta.change(update_survey_maker_data,
                                           inputs={_e_s_has_ta, _survey_maker_state_basic},
                                           outputs=[_survey_maker_state_basic])
                        _e_s_teachers.change(update_survey_maker_data,
                                             inputs={_e_s_teachers, _e_s_other_teachers, _survey_maker_state_basic},
                                             outputs=[_survey_maker_state_basic])
                        _e_s_other_teachers.change(update_survey_maker_data,
                                                   inputs={_e_s_teachers, _e_s_other_teachers,
                                                           _survey_maker_state_basic},
                                                   outputs=[_survey_maker_state_basic])
                        # _e_s_generate_button.click(update_survey_maker_data,
                        #                            inputs={_e_s_id, _e_s_themes, _e_s_class, _e_s_has_ta, _e_s_teachers,
                        #                                    _e_s_other_teachers, _survey_maker_state_basic},
                        #                            outputs=[_survey_maker_state_basic])
                        _survey_maker_state_basic.change(on_survey_maker_data_change, [_survey_maker_state_basic],
                                                         [_survey_maker_state_basic])

                        @gr.render(inputs=[_survey_maker_state_basic], triggers=[_e_s_generate_button.click])
                        def preview_survey(data):
                            for h in data['heads']:
                                PageParser.parse_page(h)
                            for b in data['bodies']:
                                PageParser.parse_page(b)

                    with gr.Column(scale=1):
                        @gr.render(inputs=[_survey_maker_state_basic], triggers=[_survey_maker_state_basic.change])
                        def show_json(data):
                            j_view = gr.JSON(value=json.dumps(data, ensure_ascii=False))
                            if not os.path.exists(os.path.join(os.getcwd(), "temp")):
                                os.mkdir(os.path.join(os.getcwd(), "temp"))
                            with open(os.path.join(os.getcwd(), "temp", "_t_survey.sr"), "w",
                                      encoding="utf8") as tmp_file:
                                json.dump(data, tmp_file, ensure_ascii=False)
                            download_btn = gr.DownloadButton(value=os.path.join(os.getcwd(), "temp", "_t_survey.sr"))

            with gr.Tab("問卷生成器-進階"):
                _survey_maker_state_adv = gr.State(
                    {"survey_id": "None", "survey_theme": "EMB", "heads": [], "bodies": [],
                     "tail": {"page_type": "tail_btn"}})
                with gr.Row():
                    with gr.Column(scale=2, min_width=640):
                        _sid = gr.Textbox(interactive=True, label="問卷 ID",
                                          placeholder="問卷ID 通常設為課程代碼，如:113F01")

                        def _sid_change(value, data):
                            data["survey_id"] = value
                            return data

                        _sid.change(_sid_change, [_sid, _survey_maker_state_adv], [_survey_maker_state_adv])

                        _themes = gr.Dropdown(self._theme_items, label="問卷色彩主題", info="問卷的配色主題，隨便選即可")

                        def _themes_selected(value, data):
                            data["survey_theme"] = value
                            return data

                        _themes.select(_themes_selected, [_themes, _survey_maker_state_adv], [_survey_maker_state_adv])

                        with gr.Accordion("問卷頭版"):
                            gr.Markdown("**不會隨著問卷換頁的區塊**")
                            with gr.Column():
                                @gr.render(inputs=[_survey_maker_state_adv],
                                           triggers=[_survey_maker_state_adv.change])
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
                                                            [_h_index, _h_ptype, _survey_maker_state_adv],
                                                            [_survey_maker_state_adv])
                                            if p["page_type"] == "head":
                                                _h_title = gr.Textbox(p['title'], max_lines=1, label="title",
                                                                      container=False,
                                                                      placeholder="OOO班 教師滿意度調查", scale=6)

                                                def _h_title_change(index, value, _data):
                                                    _data['heads'][index]["title"] = value
                                                    return _data

                                                _h_title.change(_h_title_change,
                                                                [_h_index, _h_title, _survey_maker_state_adv],
                                                                [_survey_maker_state_adv])

                                                _h_desc = gr.Textbox((p['desc'] if 'desc' in p.keys() else ""),
                                                                     max_lines=1, placeholder="說明文字, 選填",
                                                                     container=False, scale=5)

                                                def _h_desc_change(index, value, _data):
                                                    _data['heads'][index]["desc"] = value
                                                    return _data

                                                _h_desc.change(_h_desc_change,
                                                               [_h_index, _h_desc, _survey_maker_state_adv],
                                                               [_survey_maker_state_adv])
                                                _remove_btn = gr.ClearButton(value="-", scale=1)

                                                def _remove_head_click(index, _data):
                                                    _data["heads"].pop(index)
                                                    return _data

                                                _remove_btn.click(_remove_head_click,
                                                                  [_h_index, _survey_maker_state_adv],
                                                                  [_survey_maker_state_adv])

                                with gr.Row():
                                    _heads = _survey_maker_state_adv.value['heads']
                                    _h_index = gr.Number(len(_heads), interactive=False, min_width=20,
                                                         container=False, scale=1)

                                    def _h_index_update(_data):
                                        return len(_data['heads'])

                                    _survey_maker_state_adv.change(_h_index_update, [_survey_maker_state_adv],
                                                                   [_h_index])
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
                                                                           _survey_maker_state_adv],
                                                                          [_h_index, _h_ptype, _last_h_title,
                                                                           _last_h_desc, _survey_maker_state_adv])

                        with gr.Accordion("問卷題目區"):
                            gr.Markdown("**會隨著問卷換頁的答題區塊**")
                            with gr.Column():
                                @gr.render(inputs=[_survey_maker_state_adv],
                                           triggers=[_survey_maker_state_adv.change])
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
                                                            [_b_index, _b_ptype, _survey_maker_state_adv],
                                                            [_survey_maker_state_adv])
                                            match p["page_type"]:
                                                case "teacher":
                                                    _b_teacher = gr.Textbox(p['teacher'], max_lines=1, container=False,
                                                                            scale=6)

                                                    def _b_teacher_change(index, value, _data):
                                                        _data['bodies'][index]["teacher"] = value
                                                        return _data

                                                    _b_teacher.change(_b_teacher_change,
                                                                      [_b_index, _b_teacher, _survey_maker_state_adv],
                                                                      [_survey_maker_state_adv])

                                                    _b_desc = gr.Textbox((p['desc'] if 'desc' in p.keys() else ""),
                                                                         max_lines=1, placeholder="課程, 選填",
                                                                         container=False, scale=5)

                                                    def _b_desc_change(index, value, _data):
                                                        _data['bodies'][index]["desc"] = value
                                                        return _data

                                                    _b_desc.change(_b_desc_change,
                                                                   [_b_index, _b_desc, _survey_maker_state_adv],
                                                                   [_survey_maker_state_adv])
                                                    _remove_btn = gr.ClearButton(value="-", scale=1)

                                                    def _remove_body_click(index, _data):
                                                        _data["bodies"].pop(index)
                                                        return _data

                                                    _remove_btn.click(_remove_body_click,
                                                                      [_b_index, _survey_maker_state_adv],
                                                                      [_survey_maker_state_adv])

                                                case "ta":
                                                    _remove_btn = gr.ClearButton(value="-", scale=1)

                                                    def _remove_body_click(index, _data):
                                                        _data["bodies"].pop(index)
                                                        return _data

                                                    _remove_btn.click(_remove_body_click,
                                                                      [_b_index, _survey_maker_state_adv],
                                                                      [_survey_maker_state_adv])

                                                case "employment":
                                                    _remove_btn = gr.ClearButton(value="-", scale=1)

                                                    def _remove_body_click(index, _data):
                                                        _data["bodies"].pop(index)
                                                        return _data

                                                    _remove_btn.click(_remove_body_click,
                                                                      [_b_index, _survey_maker_state_adv],
                                                                      [_survey_maker_state_adv])

                                                case "finish":
                                                    _remove_btn = gr.ClearButton(value="-", scale=1)

                                                    def _remove_body_click(index, _data):
                                                        _data["bodies"].pop(index)
                                                        return _data

                                                    _remove_btn.click(_remove_body_click,
                                                                      [_b_index, _survey_maker_state_adv],
                                                                      [_survey_maker_state_adv])

                                with gr.Row():
                                    _bodies = _survey_maker_state_adv.value['bodies']
                                    _b_index = gr.Number(len(_bodies), interactive=False, min_width=20,
                                                         container=False, scale=1)

                                    def _b_index_update(_data):
                                        return len(_data['bodies'])

                                    _survey_maker_state_adv.change(_b_index_update, [_survey_maker_state_adv],
                                                                   [_b_index])
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
                                                                           _survey_maker_state_adv],
                                                                          [_b_index, _b_ptype, _last_b_teacher,
                                                                           _last_b_desc, _survey_maker_state_adv])

                                                if _value in ["ta", "employment", "finish"]:
                                                    _last_b_add_btn = gr.Button(value="+", variant="stop", size="sm",
                                                                                min_width=20, scale=1)

                                                    def _last_b_add_btn_click(_type, _data):
                                                        _data["bodies"].append(
                                                            {"page_type": _type})
                                                        return [len(_data["bodies"]), None, _data]

                                                    _last_b_add_btn.click(_last_b_add_btn_click,
                                                                          [_b_ptype, _survey_maker_state_adv],
                                                                          [_b_index, _b_ptype, _survey_maker_state_adv])

                    with gr.Column(scale=1, min_width=0, variant="compact"):
                        @gr.render(inputs=[_survey_maker_state_adv], triggers=[_survey_maker_state_adv.change])
                        def generate_survey(data):
                            gr.Json(data)


if __name__ == '__main__':
    ssm = SurveySystemManager()
    ssm.start_manager()
