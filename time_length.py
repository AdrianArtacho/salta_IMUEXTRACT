# import PySimpleGUI as sg

def parse_time_string(time_str):
    # time_str = '39:32.032'
    parts = time_str.split(':')
    minutes = int(parts[0])
    seconds, milliseconds = map(float, parts[1].split('.'))
    time_list = [minutes, int(seconds), int(milliseconds)]
    print(time_list)
    return time_list


def get_input_with_gui(mm='00', ss='00', ms='000'):
    layout = [
        [sg.InputText(default_text=mm,size=(2, 1), key='-TWO_DIGIT1-'),
         sg.Text(':'), sg.InputText(default_text=ss, size=(2, 1), key='-TWO_DIGIT2-'),
         sg.Text('.'), sg.InputText(default_text=ms, size=(3, 1), key='-THREE_DIGIT-')],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]

    window = sg.Window('Enter Cyphers', layout)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Cancel'):
            window.close()
            return None, None, None

        if event.endswith('_INPUT'):
            element_key = event.split('_')[1]
            if len(values[event]) > 2 and element_key != 'THREE_DIGIT':
                window[element_key].update(values[event][:2])
            elif len(values[event]) > 3 and element_key == 'THREE_DIGIT':
                window[element_key].update(values[event][:3])

        if event == 'Ok':
            two_digit_cypher1 = values['-TWO_DIGIT1-']
            two_digit_cypher2 = values['-TWO_DIGIT2-']
            three_digit_cypher = values['-THREE_DIGIT-']
            
            if len(two_digit_cypher1) == 2 and len(two_digit_cypher2) == 2 and len(three_digit_cypher) == 3:
                window.close()
                return two_digit_cypher1, two_digit_cypher2, three_digit_cypher
            else:
                sg.popup("Please enter valid cyphers.")

def main(time_str='00:00.000', 
         verbose=False):
    
    time_string_parsed = parse_time_string(time_str = time_str)
    if verbose:
        print("time_string_parsed", time_string_parsed)
    # exit()
    two_digit_cypher1, two_digit_cypher2, three_digit_cypher = get_input_with_gui(mm=time_string_parsed[0],
                                                                                  ss=time_string_parsed[1],
                                                                                  ms=time_string_parsed[2])

    if two_digit_cypher1 is not None and two_digit_cypher2 is not None and three_digit_cypher is not None:
        output_string = "{}:{}.{:03}".format(two_digit_cypher1, two_digit_cypher2,three_digit_cypher)
        sg.popup("Output string:", output_string)

    time_str_list = (two_digit_cypher1, two_digit_cypher2, three_digit_cypher)

    return output_string, time_str_list

if __name__ == "__main__":
    main(time_str='12:34.567',verbose=True)
