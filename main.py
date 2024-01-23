import math
import pygame
import sqlite3

pygame.init()

# определение размеров окна
screen_info = pygame.display.Info()
size = width, height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('автокликер')

# установка начальных значений
running = True
start = False
label = pygame.font.Font(None, 36)
start_run_label = label.render('начать!', False, (115, 132, 148))
start_run_label_rect = start_run_label.get_rect(topleft=(width // 2 + 1, height // 2 + 1))

circle_color = polygon_color = counter_color = pygame.Color('white')
circle_x = width // 2 + 1
circle_y = height // 2 + 1
circle_pos = (circle_x, circle_y)
circle_radius = 30
circle_width = 0
r = 180
speed = 0
polygon_width = 0
angle = 35 / 360
rotation_count = 0
counter = 0

conn = sqlite3.connect('counter.db')
cursor = conn.cursor()

cursor.execute("SELECT counter FROM pk ORDER BY counter DESC LIMIT 1")
kx = cursor.fetchone()
max_score = kx[0]
conn.close()


# шрифт для отображения максимального счета
font = pygame.font.Font(None, 36)

while True:

    if running:
        # заполнение экрана черным цветом
        screen.fill(pygame.Color('black'))

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # обработка нажатия мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed = pygame.mouse.get_pressed()
                if event.button == 3:
                    speed += 10 / 180
                elif event.button == 1:
                    speed -= 10 / 180

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    speed = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    conn = sqlite3.connect('counter.db')
                    cursor = conn.cursor()

                    cursor.execute("SELECT start FROM pk ORDER BY start DESC LIMIT 1")
                    result = cursor.fetchone()



                    updated_result = result[0] + 1
                    # Update the value in the table
                    cursor.execute('INSERT INTO pk (start, counter) VALUES (?, ?)', (str(updated_result),str(max_score)))




                    conn.commit()

                    # Закрываем соединение с базой данных
                    conn.close()
                    pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    running = False
                    start = True

        # рисование центрального круга
        circle_pos = (circle_x + 10, circle_y)
        pygame.draw.circle(screen, circle_color, circle_pos, circle_radius, circle_width)

        # рисование вращающихся полигонов
        for i in range(3):
            # расчет координат вершин полигонов
            point_1 = (circle_x + r * math.cos(angle * math.pi), circle_y + r * math.sin(angle * math.pi))
            point_2 = (
                circle_x + r * math.cos((angle + 1 / 6) * math.pi), circle_y + r * math.sin((angle + 1 / 6) * math.pi))
            polygon_points = [circle_pos, point_1, point_2]

            # рисование полигона
            pygame.draw.polygon(screen, polygon_color, polygon_points, polygon_width)

            # изменение угла поворота для следующего полигона
            angle += 120 / 180

        # изменение угла поворота для анимации вращения
        angle += speed
        if speed > 0:
            speed -= speed * 0.02
        if speed < 0:
            speed += speed * -0.02
        if speed == 0:
            speed = 0
        rotation_count += speed ** 2 ** 0.5

        # обновление счетчиков
        rotation_count += speed
        if (speed ** 2) ** 0.5 >= 0.0005:
            counter += round(((speed ** 2) ** 0.5) * 2)
        else:
            counter = 0

        if counter > max_score:
            max_score = counter

        # отображение счетчиков на экране
        max_score_text = font.render("максимальный счет: " + str(max_score), True, counter_color)
        counter_text = font.render("счет: " + str(counter), True, counter_color)
        screen.blit(max_score_text, (50, 50))
        screen.blit(counter_text, (50, 100))

        # обновление экрана
        pygame.display.flip()

        # ограничение частоты обновления экрана
        clock.tick(60)

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
