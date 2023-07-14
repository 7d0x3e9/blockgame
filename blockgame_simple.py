import pygame
import sys
import random

class BreakoutGame:
    def __init__(self):
        # 게임 화면 크기 설정
        self.screen_width = 400
        self.screen_height = 300

        # 공, 패들, 블록의 크기 설정
        self.ball_radius = 10
        self.paddle_width = 80
        self.paddle_height = 10
        self.block_width = 60
        self.block_height = 20

        # 공, 패들, 블록의 색상 설정
        self.ball_color = (255, 165, 0)
        self.paddle_color = (255, 255, 255)

        # 블록 사이의 간격 설정
        self.block_gap = 5

        # 게임 요소 초기화
        self.ball = None
        self.paddle = None
        self.blocks = []
        self.lives = 3
        self.dx = 1.2
        self.dy = -1.2
        self.is_gameover = False
        self.is_congratulation = False
        self.font = None
        self.button_font = None
        self.exit_button = None
        self.paddle_speed = 2

    def setup(self):
        # pygame 초기화
        pygame.init()

        # 게임 폰트 설정
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 22)

        # 게임 화면 설정
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        # 로딩 문구 표시
        loading_text = self.font.render("Break the Blocks!", True, (255, 255, 255))
        self.screen.blit(loading_text, (self.screen_width // 2 - loading_text.get_width() // 2, self.screen_height // 2 - loading_text.get_height() // 2))
        pygame.display.flip()

        # 2초 동안 코드 실행 지연
        pygame.time.delay(2000)

        # 공, 패들, 블록 초기 위치 설정
        self.ball = pygame.Rect(
            self.screen_width // 2 - self.ball_radius, self.screen_height // 2 - self.ball_radius,
            self.ball_radius * 2, self.ball_radius * 2
        )
        self.paddle = pygame.Rect(
            self.screen_width // 2 - self.paddle_width // 2, self.screen_height - self.paddle_height - 10,
            self.paddle_width, self.paddle_height
        )
        self.blocks = [
            {
                'rect': pygame.Rect(
                    i * (self.block_width + self.block_gap), j * (self.block_height + self.block_gap),
                    self.block_width, self.block_height
                ),
                'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            }
            for i in range(self.screen_width // (self.block_width + self.block_gap))
            for j in range(self.screen_height // (self.block_height + self.block_gap) // 2)
        ]

    def reset_ball(self):
        # 공 초기 위치 및 속도 재설정
        self.ball.left, self.ball.top = self.screen_width // 2 - self.ball_radius, self.screen_height // 2 - self.ball_radius
        self.dx, self.dy = 1.2, -1.2
        self.lives -= 1

    def run(self):
        # 게임 설정 초기화
        self.setup()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.lives <= 0:
                self.is_gameover = True

            if not self.is_gameover and not self.is_congratulation:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    # 왼쪽 화살표 키를 누르면 패들을 왼쪽으로 이동
                    self.paddle.left -= self.paddle_speed
                    if self.paddle.left < 0:
                        self.paddle.left = 0
                if keys[pygame.K_RIGHT]:
                    # 오른쪽 화살표 키를 누르면 패들을 오른쪽으로 이동
                    self.paddle.right += self.paddle_speed
                    if self.paddle.right > self.screen_width:
                        self.paddle.right = self.screen_width

                # 공의 위치 업데이트
                self.ball.left += self.dx
                self.ball.top += self.dy

                # 공과 패들, 블록 간의 충돌 검사
                if self.ball.left < 0 or self.ball.right > self.screen_width:
                    self.dx *= -1
                if self.ball.top < 0:
                    self.dy *= -1
                if self.ball.bottom > self.screen_height:
                    if self.lives > 0:
                        self.reset_ball()
                    else:
                        self.is_gameover = True
                        continue

                ball_rect = pygame.draw.circle(self.screen, self.ball_color, self.ball.center, self.ball_radius)
                paddle_rect = pygame.draw.rect(self.screen, self.paddle_color, self.paddle)

                if paddle_rect.colliderect(ball_rect):
                    self.dy *= -1

                hit_index = self.ball.collidelist([block['rect'] for block in self.blocks])
                if hit_index != -1:
                    hit_rect = self.blocks.pop(hit_index)
                    self.dx *= -1.1 if self.ball.centerx < hit_rect['rect'].left or self.ball.centerx > hit_rect['rect'].right else 1
                    self.dy *= -1.1 if self.ball.centery < hit_rect['rect'].top or self.ball.centery > hit_rect['rect'].bottom else 1

                # 화면 초기화
                self.screen.fill((0, 0, 0))

                # 공, 패들, 블록 그리기
                pygame.draw.circle(self.screen, self.ball_color, self.ball.center, self.ball_radius)
                pygame.draw.rect(self.screen, self.paddle_color, self.paddle)
                for block in self.blocks:
                    pygame.draw.rect(self.screen, block['color'], block['rect'])

                # 남은 라이프 표시
                lives_text = str(self.lives)
                font_size = 24
                font_color = (255, 255, 255)
                font = pygame.font.Font(None, font_size)
                text_surface = font.render(f'Life: {lives_text}', True, font_color)
                text_rect = text_surface.get_rect()
                text_rect.topleft = (10, 260)
                self.screen.blit(text_surface, text_rect)

                # 블록을 모두 깼을 때 축하 메시지 표시
                if len(self.blocks) == 0:
                    self.is_congratulation = True
                    continue

                # 화면 업데이트
                pygame.display.flip()
                self.clock.tick(60)

            elif self.is_congratulation:
                self.screen.fill((0, 0, 0))

                text = self.font.render("Congratulation!", True, (255, 255, 255))
                self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, self.screen_height // 2 - text.get_height() // 2))

                exit_button = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 50, 100, 30)
                pygame.draw.rect(self.screen, (255, 0, 0), exit_button)

                exit_text = self.button_font.render("Exit", True, (255, 255, 255))
                self.screen.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2, exit_button.centery - exit_text.get_height() // 2))

                if exit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (255, 255, 255), exit_button, 2)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and exit_button.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

                pygame.display.flip()

            elif self.is_gameover:
                self.screen.fill((0, 0, 0))

                text = self.font.render("Game Over", True, (255, 255, 255))
                self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, self.screen_height // 2 - text.get_height() // 2))

                exit_button = pygame.Rect(self.screen_width // 2 - 50, self.screen_height // 2 + 50, 100, 30)
                pygame.draw.rect(self.screen, (255, 0, 0), exit_button)

                exit_text = self.button_font.render("Exit", True, (255, 255, 255))
                self.screen.blit(exit_text, (exit_button.centerx - exit_text.get_width() // 2, exit_button.centery - exit_text.get_height() // 2))

                if exit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (255, 255, 255), exit_button, 2)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1 and exit_button.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

                pygame.display.flip()

if __name__ == "__main__":
    BreakoutGame().run()
