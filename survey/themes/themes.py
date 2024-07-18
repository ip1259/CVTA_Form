import gradio as gr


class SurveyTheme:
    JS = """
        function refresh() {
            const url = new URL(window.location);
        
            if (url.searchParams.get('__theme') !== 'light') {
                url.searchParams.set('__theme', 'light');
                window.location.href = url.href;
            }
        }
        """

    EMB_CSS = """#sendButton {background-color: #4EFEB3}
                #sendButton:hover {background-color: #02F78E}
    """

    EMB = gr.themes.Soft(
        primary_hue="emerald",
        neutral_hue="sky",
        text_size="lg",
        spacing_size="lg",
        radius_size="lg",
        font=[gr.themes.GoogleFont('Noto Sans'), 'ui-sans-serif', 'system-ui', 'sans-serif'],
    ).set(
        block_background_fill='*primary_50',
        block_border_width='2px'
    )
