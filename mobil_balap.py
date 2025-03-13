import pygame
import random

# Inisialisasi pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Mobil Balap")

# Muat gambar dan ubah ukuran
def load_and_scale_image(path, width, height):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (width, height))

player_car = load_and_scale_image("C:/Users/Acer/Downloads/car.png", 50, 100)
obstacle_image = load_and_scale_image("C:/Users/Acer/Downloads/obstacle.jpg", 50, 100)
background_image = load_and_scale_image("C:/Users/Acer/Downloads/background.png", WIDTH, HEIGHT)

# Ukuran gambar
car_width, car_height = player_car.get_size()
obstacle_width, obstacle_height = obstacle_image.get_size()

# Fungsi untuk menggambar mobil
def draw_car(x, y):
    screen.blit(player_car, (x, y))

# Fungsi untuk menggambar rintangan
def draw_obstacle(obstacle_x, obstacle_y):
    screen.blit(obstacle_image, (obstacle_x, obstacle_y))

# Fungsi untuk menampilkan pesan Game Over
def show_game_over(score, x):
    font = pygame.font.Font(None, 74)
    game_over_text = font.render('GAME OVER', True, (255, 0, 0))
    score_text = font.render(f'Skor Akhir: {score}', True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))

    # Gambar mobil di posisi terakhir sebelum restart
    draw_car(x, HEIGHT * 0.8)
    pygame.display.flip()

# Loop utama game
def game_loop():
    x = (WIDTH * 0.45)
    y = (HEIGHT * 0.8)
    x_change = 0
    score = 0
    obstacle_x = random.randint(0, WIDTH - obstacle_width)
    obstacle_y = -100
    obstacle_speed = 5

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Kembali ke fungsi main untuk keluar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        # Update posisi mobil
        x += x_change
        if x < 0: x = 0
        elif x > WIDTH - car_width: x = WIDTH - car_width

        # Update posisi rintangan
        obstacle_y += obstacle_speed

        # Jika rintangan keluar layar, reset posisi dan tambah skor
        if obstacle_y > HEIGHT:
            obstacle_y = 0 - obstacle_height
            obstacle_x = random.randint(0, WIDTH - obstacle_width)
            score += 1
            # Naikkan kecepatan rintangan setelah setiap skor
            obstacle_speed += 0.5

        # Cek tabrakan
        if y < obstacle_y + obstacle_height:
            if x < obstacle_x + obstacle_width and x + car_width > obstacle_x:
                show_game_over(score, x)  # Tampilkan pesan Game Over
                return True  # Kembali ke fungsi main untuk restart

        # Menggambar latar belakang dan mobil
        screen.blit(background_image, (0, 0))
        draw_car(x, y)
        draw_obstacle(obstacle_x, obstacle_y)

        # Tampilkan skor
        score_text = font.render(f'Skor: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Perbarui tampilan
        pygame.display.flip()
        clock.tick(60)

# Loop untuk menjalankan game dan restart
def main():
    running = True
    while running:
        restart = game_loop()  # Jalankan game_loop
        if not restart:  # Jika tidak ada restart, keluar dari loop
            running = False

        # Setelah game over, tunggu input sebelum restart
        x = (WIDTH * 0.45)  # Posisi awal mobil
        while restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    restart = False  # Keluar dari loop jika pemain menutup jendela
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x -= 5
                    elif event.key == pygame.K_RIGHT:
                        x += 5
                    x = max(0, min(x, WIDTH - car_width))  # Pastikan mobil tetap dalam batas
            
            screen.blit(background_image, (0, 0))
            show_game_over(0, x)  # Tampilkan pesan Game Over dan posisi mobil
            pygame.display.flip()

            # Batasi frame rate agar tidak lag
            pygame.time.delay(30)

# Jalankan game
main()
pygame.quit()