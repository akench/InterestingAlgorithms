from numpy import arange
import PySimpleGUI as sg


def get_weights(weight, denoms, idx, denom_freq, chosen, result):
    if idx >= len(denoms):
        return
    if weight == 0:
        result.append(list(chosen))
        return
    
    # choose denom
    denom = denoms[idx]
    if denom <= weight and denom_freq[denom] > 0:
        denom_freq[denom] -= 1
        chosen.append(denom)

        get_weights(weight - denom, denoms, idx, denom_freq, chosen, result)
        
        chosen.pop()
        denom_freq[denom] += 1
    
    # dont choose
    get_weights(weight, denoms, idx+1, denom_freq, chosen, result)


def get_plate_weights(target_weight, plate_count):
    '''
    options:
    two dumbells (or bar)
    single dumbell
    '''
    denoms = [2.5, 2, 1.5, 1.25]

    denom_freq = dict()
    for denom in denoms:
        denom_freq[denom] = plate_count

    # 0, 0.25, 0.5, ..... 1.75, 2.0
    for diff in arange(0.0, 2.0, 0.25):
        for w_diff in [diff, -diff]:
            sols = []
            get_weights(target_weight + w_diff, denoms, 0, denom_freq, [], sols)
            
            if sols:
                result = min(sols, key=lambda s: len(s))
                print('each side', result)
                print('sum', sum(result) * 2)
                return result
    return []


def ui():
    # Define the window's contents
    layout = [[sg.Text('weight on each dumbell:'), sg.Input(key='#target_weight', size=(10,1))],
            [sg.Text('number of dumbells:     '), sg.Radio('one', 1, key='#one'), sg.Radio('two', 1, key='#two', default=True)],
            [sg.Text(size=(40,1), key='#plates')],
            [sg.Button('Calculate plates')]]

    # Create the window
    window = sg.Window('Lifting Calculator', layout)

    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        print(event, values)
        # See if user wants to quit or window was closed
        if event == sg.WINDOW_CLOSED:
            break
        
        if values['#two']:
            plate_count = 1
        elif values['#one']:
            plate_count = 2

        target_weight = float(values['#target_weight']) / 2
        plate_weights = get_plate_weights(target_weight, plate_count)
        # Output a message to the window
        window['#plates'].update("each side=" + str(plate_weights) + ', sum=' + str(2 * sum(plate_weights)))

    # Finish up by removing from the screen
    window.close()
        

if __name__ == '__main__':
    ui()
