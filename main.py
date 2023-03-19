import os
import PySimpleGUI as sg
from PIL import Image


def gif_to_images(gif_file):
    im = Image.open(gif_file)

    n = im.n_frames
    images = []

    if not os.path.exists('output'):
        os.mkdir('output')

    for i in range(n):
        im.seek(i)
        frame = im.copy()
        image_file = f'output/frame{i}.png'
        frame.save(image_file)
        images.append(image_file)
    return images


layout = [
    [sg.Text('分解的图片在 output 目录下')],
    [sg.FileBrowse('选择GIF文件', file_types=(('GIF Files', '*.gif'),),
                   key='-FILE-', target='-FILE-', enable_events=True), sg.Text('未选择', key='-FILENAME-')],
    [sg.Image(key='-IMAGE-')],
    [sg.Text('拖动滑块查看所有图片'), sg.Slider(range=(0, 0), orientation='h', size=(
        20, 15), enable_events=True, key='-SLIDER-')]
]

window = sg.Window('GIF分解器', layout, size=(400, 200), resizable=True,
                   finalize=True)
images = ['']

# 进入主循环
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Escape':
        break

    elif event == '-FILE-':
        gif_file = values['-FILE-']
        window['-FILENAME-'].update(gif_file)
        images = gif_to_images(gif_file)
        window['-IMAGE-'].update(filename=images[0])
        window['-SLIDER-'].update(range=(0, len(images)-1))

    elif event == '-SLIDER-':
        index = int(values['-SLIDER-'])
        image_file = images[index]
        window['-IMAGE-'].update(filename=image_file)

window.close()
