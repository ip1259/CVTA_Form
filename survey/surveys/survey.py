from gradio.themes.base import Base as grBase
import survey.pages.page as sPage
import survey.pages.pages as sPages
import gradio as gr


class Survey:
    def __init__(self):
        self.survey_id: str = ""
        self.survey_theme: grBase | None = None
        self.heads: list[sPage.Page] = []
        self.bodies: list[sPage.Page] = []
        self.tail: sPage.Page = sPage.Page(self)
        self.survey: gr.Blocks | None = None

    def get_rows_in_bodies(self):
        _results = []
        _results.extend([b.page for b in self.bodies])
        return _results

    def get_survey_input_components(self):
        _results = []
        for p in self.bodies:
            _results.extend(p.get_input_components())
        return _results

    def set_survey(self, file_path: str):
        pass

    def generate_survey(self):
        with gr.Blocks() as _survey:
            for _hp in self.heads:
                _hp.page.render()
            for _bp in self.bodies:
                _bp.page.render()
            self.tail.page.render()


def get_page_type(ptype: str):
    match ptype:
        case "head":
            return sPages.HeadPage


def get_theme(theme: str):
    match theme:
        case "EMB":
