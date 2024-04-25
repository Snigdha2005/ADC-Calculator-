import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 720, 520
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Calculator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
FONT = pygame.font.SysFont('Arial', 28)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_input_box(surface, x, y, width, height, text_input, x1, y1):
    text_box = pygame.draw.rect(surface, GRAY, (x, y, width, height), 2)
    text_surface = FONT.render(text_input, True, BLACK)
    screen.blit(text_surface, (x1, y1))
    return text_box

def draw_button(surface, x, y, width, height, text):
    box = pygame.draw.rect(surface, GRAY, (x, y, width, height))
    draw_text(text, FONT, BLACK, surface, x + 10, y + 10)
    return box

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
active_input = 0
adc_bits = ""
analog_voltage = ""
ref_voltage = ""
digital_out = ""
bin_digital_out = ""

running = True
while(running):
    screen.fill(WHITE)

    draw_text('Number of bits in ADC: ', FONT, BLACK, screen, 10, 20)
    adc_box = draw_input_box(screen, 450, 20, 200, 40, adc_bits, 450, 20)  # Draw input box for ADC bits

    draw_text('Analog Voltage Input for ADC: ', FONT, BLACK, screen, 10, 80)
    Vin_box = draw_input_box(screen, 450, 80, 200, 40, analog_voltage, 450, 80)  # Draw input box for analog voltage input

    draw_text('Reference Voltage Input for ADC: ', FONT, BLACK, screen, 10, 140)
    ref_box = draw_input_box(screen, 450, 140, 200, 40, ref_voltage, 450, 140)  # Draw input box for reference voltage input

    calculate_box = draw_button(screen, 100, 250, 200, 50, "CALCULATE")
    reset_box = draw_button(screen, 400, 250, 200, 50, "RESET")

    draw_text('Numeric Digital Output: ', FONT, BLACK, screen, 10, 380)
    dec_box = draw_input_box(screen, 450, 380, 200, 40, digital_out, 450, 380)  # Draw input box for reference voltage input

    draw_text('Binary Digital Output: ', FONT, BLACK, screen, 10, 440)
    bin_box = draw_input_box(screen, 450, 440, 200, 40, bin_digital_out, 450, 440)  # Draw input box for reference voltage input

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                #print("Entered text:", adc_bits)
                #print("Entered text:", analog_voltage)
                #print("Entered text:", ref_voltage)
                pass
            elif event.key == pygame.K_BACKSPACE:
                if active_input == 1:
                    adc_bits = adc_bits[:-1]
                elif active_input == 2:
                    analog_voltage = analog_voltage[:-1]
                elif active_input == 3:
                    ref_voltage = ref_voltage[:-1]
            else:
                if active_input == 1:
                    adc_bits += event.unicode
                elif active_input == 2:
                    analog_voltage += event.unicode
                elif active_input == 3:
                    ref_voltage += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if adc_box.collidepoint(mouse_pos):
                active_input = 1
            elif Vin_box.collidepoint(mouse_pos):
                active_input = 2
            elif ref_box.collidepoint(mouse_pos):
                active_input = 3
            elif calculate_box.collidepoint(mouse_pos):
                if adc_bits and analog_voltage and ref_voltage:
                    if float(ref_voltage) != 0:
                        x = 2**(int(adc_bits)) * float(analog_voltage) / float(ref_voltage)
                        if math.ceil(x) == x:
                            digital_out = str(x)
                            bin_digital_out = str(bin(int(x))[2:])
                    else:
                        digital_out = "Infinity"
                        bin_digital_out = "Infinity"       
            elif reset_box.collidepoint(mouse_pos):
                adc_bits = ""
                analog_voltage = ""
                ref_voltage = ""  
                digital_out = ""
                bin_digital_out = ""            
pygame.quit()
sys.exit()