import io

from prutils.pr_pilhelper import get_im_size
import PySimpleGUI as sg
from PIL import Image

class DMHelper:
    def __init__(self):
        pass

    def _update_im(self, window, im_path):
        graph = window.Element("graph")
        self._draw_frame(graph, im_path)

    def dialog(self, im_path, get_next_im_path, verify_code):
        img_w, img_h = get_im_size(im_path)
        layout = [
            [sg.Text('请输入验证码,点击图片切换')],
            [
                sg.Graph(
                    canvas_size=(img_w, img_h),
                    graph_bottom_left=(0, 0),
                    graph_top_right=(img_w, img_h),
                    key="graph",
                    enable_events=True
                    # background_color="red"
                )
            ],
            [sg.InputText(size=(25, 1), key="code"), sg.Button("确定", key="ok")],
        ]

        window = sg.Window("验证码", layout, return_keyboard_events=True)
        window.Finalize()
        self._update_im(window, im_path)

        while True:
            event, values = window.Read()
            if event == "graph":
                self._update_im(window, get_next_im_path())
                continue
            if event == "ok" or event == '\r':
                if not verify_code(values["code"]):
                    self._update_im(window, get_next_im_path())
                    window.Element("code").Update("")
                    continue
                else:
                    return True
            if event is None:
                return False

    def _draw_frame(self, target, im_path):
        img = Image.open(im_path).convert("RGBA")
        b = io.BytesIO()
        img.save(b, 'PNG')

        target.DrawImage(data=b.getvalue(), location=(0, 30))


