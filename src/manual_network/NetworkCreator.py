"""
If you want yo use only the nodes of the network:
    remove comments from lines 106 and 107.
"""

import sys, os
import pygame
import cv2
import pickle
from pygame.locals import QUIT, MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, KEYDOWN, K_n, K_l, K_z, K_s, K_1, K_2, K_3, KMOD_CTRL
import math
import tkinter as tk
from tkinter import  filedialog, simpledialog

node_ratio = 9

def draw_arrow(screen, color, start, end, trirad):

    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))
    end = (end[0] - 2*node_ratio*math.cos(math.radians(rotation)), end[1] + 2*node_ratio*math.sin(math.radians(rotation)))
    pygame.draw.line(screen,color,start,end,4)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen,
                         color,
                        ((end[0]+trirad*math.sin(math.radians(rotation)), end[1]+trirad*math.cos(math.radians(rotation))), 
                         (end[0]+trirad*math.sin(math.radians(rotation-120)), end[1]+trirad*math.cos(math.radians(rotation-120))), 
                         (end[0]+trirad*math.sin(math.radians(rotation+120)), end[1]+trirad*math.cos(math.radians(rotation+120)))))

def save_state_with_filename(state_filename, nodes, links, lanes, action_history):
    '''
    This funtion save data to reload in the future if you need to make changes in the network
    '''
    dir_name = "data/processed/from_networkCreator/"
    with open(dir_name + state_filename, "wb") as f:
        pickle.dump({"nodes": nodes, "links": links,"lanes": lanes, "action_history": action_history}, f)

def save_data_about_network(name, node_positions, node_conections, lanes_of_link):
        
        # make a directory to save data
        dir_name = "data/processed/from_networkCreator/"
        if not os.path.isdir(str(dir_name) + str(name)):
            print('Doesn\'t exist directory')
            os.mkdir(str(dir_name) + str(name))
        
        # save data about parameters of nodes in the network
        f_node_positions = open(str(dir_name) + str(name) + "/node_positions.dat", "w")
        f_node_conections = open(str(dir_name) + str(name) + "/node_conections.dat", "w")
        f_lanes_of_link = open(str(dir_name) + str(name) + "/lanes_of_link.dat", "w")
        f_node_positions.write(str(node_positions))
        f_node_conections.write(str(node_conections))
        f_lanes_of_link.write(str(lanes_of_link))
        f_node_positions.close()
        f_node_conections.close() 
        f_lanes_of_link.close()

def browse_pickle_file():
    initial_directory = 'data/processed/from_networkCreator'
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir= initial_directory,
                                           title="Select old network (.pickle)",
                                           filetypes=(("Image files", "*.png"),
                                                      ("All files", "*.*")))
    return file_path

def load_state(state_filename):
    with open(state_filename, "rb") as f:
        data = pickle.load(f)
    return data["nodes"], data["links"], data["lanes"] ,data["action_history"]

def browse_image_file():
    initial_directory = 'data/raw/Images'
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select picture",
                                           initialdir= initial_directory,
                                           filetypes=(("Image files", "*.png"),
                                                      ("Archivos JPEG", "*.jpg")))
    return file_path

def create_initial_menu():
    def on_new_data_click():
        window.destroy()
        IMAGE_FILE = browse_image_file()
        if IMAGE_FILE:
            main_program(IMAGE_FILE, load_previous_data=False)

    def on_load_data_click():
        window.destroy()
        IMAGE_FILE = browse_image_file()
        if IMAGE_FILE:
            main_program(IMAGE_FILE, load_previous_data=True)

    window = tk.Tk()
    window.title("Menu")

    new_data_button = tk.Button(window, text="New", command=on_new_data_click)
    new_data_button.pack(pady=10)

    load_data_button = tk.Button(window, text="    Load network    ", command=on_load_data_click)
    load_data_button.pack(pady=10)

    window.mainloop()

def main_program(IMAGE_FILE, load_previous_data=False):
    if load_previous_data:
        state_filename = browse_pickle_file()
        if state_filename:
            nodes, links, lanes, action_history = load_state(state_filename)
            #links = []
            #lanes = []
        else:
            nodes = []
            links = []
            lanes = []
            action_history = []
    else:
        nodes = []
        links = []
        lanes = []
        action_history = []

    # Constantes y configuraciones iniciales
    BACKGROUND_COLOR = (0, 0, 0)
    img = cv2.imread(IMAGE_FILE)
    SCREEN_SIZE = (img.shape[1], img.shape[0])
    circle_color = (0,0,0)
    line_color = (0, 0, 0)

    # Inicializa Pygame
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("NetworkPaint")
    clock = pygame.time.Clock()

    # Carga la imagen de fondo
    background_image = pygame.image.load(IMAGE_FILE).convert()
        
    image_rect = background_image.get_rect()

    zoom = 1.0
    dragging = False
    offset = [0, 0]
    node_creation_mode = False
    link_creation_mode = False
    selected_node = None

    # Inicializa las fuentes
    pygame.font.init()
    font = pygame.font.Font(None, 24)

    
    # Bucle principal del programa
    N_pistas = 1
    show_save_message_until = 0
    show_save_message_pistas_until = 0
    state_filename = None
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_n or (event.key == K_z and node_creation_mode == True):
                    node_creation_mode = not node_creation_mode
                    link_creation_mode = False
                elif event.key == K_l or (event.key == K_z and link_creation_mode == True):
                    link_creation_mode = not link_creation_mode
                    node_creation_mode = False
                elif event.key == K_z and event.mod & KMOD_CTRL:
                    if action_history:
                        last_action = action_history.pop()
                        if last_action[0] == "node":
                            nodes.pop()
                        elif last_action[0] == "link":
                            links.remove(last_action[1])
                            lanes.pop()
                elif event.key == K_s and event.mod & KMOD_CTRL:
                    if state_filename is None:
                        root = tk.Tk()
                        root.withdraw()
                        state_filename = simpledialog.askstring("Save data", "Name:")
                        if state_filename is None:
                            continue
                        state_filename += ""

                    save_data_about_network(state_filename, nodes, links, lanes)
                    save_state_with_filename(state_filename, nodes, links, lanes, action_history)
                    show_save_message_until = pygame.time.get_ticks() + 2000  # Mostrar mensaje durante 2 segundos
                elif link_creation_mode == True:
                    if event.key == K_1:
                        N_pistas = 1
                        show_save_message_pistas_until = pygame.time.get_ticks() + 2000  # Mostrar mensaje durante 2 segundos

                    elif event.key == K_2:
                        N_pistas = 2
                        show_save_message_pistas_until = pygame.time.get_ticks() + 2000  # Mostrar mensaje durante 2 segundos

                    elif event.key == K_3:
                        N_pistas = 3
                        show_save_message_pistas_until = pygame.time.get_ticks() + 2000  # Mostrar mensaje durante 2 segundos


            elif event.type == MOUSEBUTTONDOWN:
                #print(event.b
                if event.button in [4, 5]:  # Scroll up/down
                    if not node_creation_mode:
                        mouse_x, mouse_y = event.pos
                        # Calcular la posición relativa del mouse en la imagen
                        rel_x = (mouse_x - image_rect.x) / (zoom * image_rect.width)
                        rel_y = (mouse_y - image_rect.y) / (zoom * image_rect.height)

                        if event.button == 4:  # Scroll up
                            new_zoom  = zoom * 1.1
                            if new_zoom <= 20:
                                zoom = new_zoom
                        elif event.button == 5:  # Scroll down
                            new_zoom = zoom / 1.1
                            if new_zoom >= 1.0:
                                zoom = new_zoom
                            if new_zoom <= 1.1:
                                zoom = 1.0
                        # Ajustar la posición de la imagen según el nuevo zoom y el punto focal
                        image_rect.x = mouse_x - rel_x * zoom * image_rect.width
                        image_rect.y = mouse_y - rel_y * zoom * image_rect.height

                        # Limitar el movimiento de la imagen cuando se aleja el zoom
                        if image_rect.x > 0:
                            image_rect.x = 0
                        if image_rect.y > 0:
                            image_rect.y = 0
                        if image_rect.x < SCREEN_SIZE[0] - image_rect.width * zoom:
                            image_rect.x = int(SCREEN_SIZE[0] - image_rect.width * zoom)
                        if image_rect.y < SCREEN_SIZE[1] - image_rect.height * zoom:
                            image_rect.y = int(SCREEN_SIZE[1] - image_rect.height * zoom)

                elif event.button == 1:  # Left mouse button
                    if node_creation_mode:
                        # Agrega un nodo en la ubicación del mouse
                        mouse_x, mouse_y = event.pos
                        rel_x = (mouse_x - image_rect.x) / (zoom * image_rect.width)
                        rel_y = (mouse_y - image_rect.y) / (zoom * image_rect.height)
                        new_node = (rel_x, rel_y)
                        print(new_node)

                        can_create_node = True
                        for existing_node in nodes:
                            distance = ((new_node[0] - existing_node[0]) ** 2 + (new_node[1] - existing_node[1]) ** 2) ** 0.5
                            if distance * zoom * image_rect.width <= 2*node_ratio:  # Radio de 5 para cada nodo
                                can_create_node = False
                                break
                        
                        if can_create_node:
                            nodes.append(new_node)
                            action_history.append(("node", new_node))

                    elif link_creation_mode:

                        mouse_x, mouse_y = event.pos
                        clicked_node = None

                        # Buscar el nodo que fue clickeado
                        for i, node in enumerate(nodes):
                            screen_x = int(image_rect.x + node[0] * zoom * image_rect.width)
                            screen_y = int(image_rect.y + node[1] * zoom * image_rect.height)
                            distance = ((mouse_x - screen_x) ** 2 + (mouse_y - screen_y) ** 2) ** 0.5

                            if distance <= 5:
                                clicked_node = i
                                break

                        if clicked_node is not None:
                            if selected_node is None:
                                selected_node = clicked_node
                            else:
                                if selected_node != clicked_node:
                                    new_link = (selected_node, clicked_node)
                                    if new_link not in links:
                                        links.append(new_link)
                                        action_history.append(("link", new_link))
                                        lanes.append(N_pistas)
                                selected_node = None
                    else:
                        dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = mouse_x - image_rect.x
                        offset_y = mouse_y - image_rect.y

            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == MOUSEMOTION:
                if dragging and not node_creation_mode:
                    mouse_x, mouse_y = event.pos
                    new_x = mouse_x - offset_x
                    new_y = mouse_y - offset_y

                    # Limitar el movimiento de la imagen dentro de la ventana
                    if new_x <= 0 and new_x >= SCREEN_SIZE[0] - image_rect.width * zoom:
                        image_rect.x = new_x
                    if new_y <= 0 and new_y >= SCREEN_SIZE[1] - image_rect.height * zoom:
                        image_rect.y = new_y

        screen.fill(BACKGROUND_COLOR)

        # Dibuja la imagen escalada en la ventana
        scaled_image = pygame.transform.scale(background_image, (int(image_rect.width * zoom), int(image_rect.height * zoom)))
        scaled_rect = scaled_image.get_rect()
        scaled_rect.x = image_rect.x
        scaled_rect.y = image_rect.y
        screen.blit(scaled_image, scaled_rect)

        # Dibuja los nodos
        for link in links:
            start_node = nodes[link[0]]
            end_node = nodes[link[1]]
            start_x = int(image_rect.x + start_node[0] * zoom * image_rect.width)
            start_y = int(image_rect.y + start_node[1] * zoom * image_rect.height)
            end_x = int(image_rect.x + end_node[0] * zoom * image_rect.width)
            end_y = int(image_rect.y + end_node[1] * zoom * image_rect.height)

            draw_arrow(screen, line_color,(start_x, start_y), (end_x, end_y), 5 )
            pygame.draw.line(screen, line_color, (start_x, start_y), (end_x, end_y), 2)
            pygame.draw.circle(screen, circle_color, (start_x, start_y), node_ratio)
            pygame.draw.circle(screen, circle_color, (end_x, end_y), node_ratio)

        for node in nodes:
            screen_x = int(image_rect.x + node[0] * zoom * image_rect.width)
            screen_y = int(image_rect.y + node[1] * zoom * image_rect.height)
            pygame.draw.circle(screen, circle_color, (screen_x, screen_y), node_ratio)

        # Dibuja el texto del modo actual
        mode_text = "Mode: "
        if node_creation_mode:
            mode_text += "Creation of nodes (press 'n' to out)"
        elif link_creation_mode:
            if selected_node is None:
                mode_text += "Creation of links (press 'l' to out)"
            elif selected_node is not None:
                mode_text += "Do click in other node"
        else:
            mode_text += "Move (press 'n' to make nodes or 'l' to make links)"

        text_surface = font.render(mode_text,True, (0, 0, 0))
        screen.blit(text_surface,(10, SCREEN_SIZE[1]-35))
        
        # Dibuja el mensaje de guardado si es necesario
        if pygame.time.get_ticks() < show_save_message_until:
            save_message = font.render("Saved...", True, (0, 0, 0))
            screen.blit(save_message, (SCREEN_SIZE[0]- 140, SCREEN_SIZE[1]-35))
        
        # Dibuja el mensaje de Numero de Pistas si es necesario
        if pygame.time.get_ticks() < show_save_message_pistas_until:
            save_message = font.render("Have " +str(N_pistas)+" Lanes" , True, (0, 0, 0))
            screen.blit(save_message, (SCREEN_SIZE[0]- 140, SCREEN_SIZE[1]-35))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    create_initial_menu()