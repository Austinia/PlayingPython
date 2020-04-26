import pygame
import random
from time import sleep

WHITE = (255, 255, 255)  # 흰색을 표현하는 값
pad_width = 1024  # 게임판 폭
pad_height = 512  # 게임판 높이
background_width = 1024
bat_width = 110
aircraft_width = 90
aircraft_height = 55


def drawobject(obj, x, y):  # 자리 지정 함수
    global gamepad
    gamepad.blit(obj, (x, y))


'''def back(background, x, y):  # 배경 이미지를 게임판 위에 그려주는 함수
    global gamepad
    gamepad.blit(background, (x, y)) : 함수 중복으로 삭제'''


'''def airplane(x, y):  # 조정할 비행기를 (x,y)에 지정
    global gamepad, aircraft
    gamepad.blit(aircraft, (x, y)) : 함수 중복으로 삭제'''


def rungame():
    global gamepad, aircraft, clock, background1, background2  # 전역 변수 선언
    global bat, fires, bullet

    bullet_xy = []

    x = pad_width * 0.05  # 비행기 최초 위치 지정
    y = pad_height * 0.8
    y_change = 0

    background1_x = 0  # 배경 이미지의 좌상단 모시리의 X좌표 초기화
    background2_x = background_width  # 배경 이미지 복사본을 원본 바로 다음에 위치 시키도록 지정

    bat_x = pad_width  # 박쥐가 날아올 위치
    bat_y = random.randrange(0, pad_height)

    fire_x = pad_width  # 불덩어리가 날아올 위치
    fire_y = random.randrange(0, pad_height)
    random.shuffle(fires)
    fire = fires[0]

    crashed = False  # 게임종료 플래그
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 이벤트 타입이 창을 닫는 것이면
                crashed = True  # 빠져 나와라

            if event.type == pygame.KEYDOWN:  # 키를 누를경우 움직일 픽셀 지정
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5

                elif event.key == pygame.K_LCTRL:  # 컨트롤 키 누르면 비행기에서 총알 발사
                    bullet_x = x + aircraft_width
                    bullet_y = y + aircraft_height/2
                    bullet_xy.append([bullet_x, bullet_y])  # 불렛 리스트에 좌표 추가

                elif event.key == pygame.K_SPACE:
                    sleep(5)
                    
            if event.type == pygame.KEYUP:  # 키를 누르지 않을 경우 이벤트 지정
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        # Clear gamepad
        gamepad.fill(WHITE)

        # Draw Background
        background1_x -= 2  # 배경 이미지와 복사본을 왼쪽으로 2픽셀 이동
        background2_x -= 2

        if background1_x == -background_width:  # 배경이미지가 게임판에서 사라지면 그 위치를 배경 이미지 본사본 오른쪽으로 위치
            background1_x = background_width

        if background2_x == -background_width:  # 복사본도 사라지면 원본 오른쪽에 위치
            background2_x = background_width

        # back(background1, background1_x, 0)  # 배경 이미지 게임판에 그리기 위해 X, y 좌표 전달
        # back(background2, background2_x, 0)  함수 중복으로 삭제

        drawobject(background1, background1_x, 0)
        drawobject(background2, background2_x, 0)

        # Aircraft Position
        y += y_change  # 좌표 변경
        if y < 0:  # 비행기 Y 좌표 제한
            y = 0
        elif y > pad_height - aircraft_height:
            y = pad_height - aircraft_height
        # airplane(x, y)  # 새로운 위치 호출: 함수 중복으로 삭제

        # Bat Position
        bat_x -= 7  # 박쥐 속도
        if bat_x <= 0:
            bat_x = pad_width
            bat_y = random.randrange(0, pad_height)

        # Fireball Position
        if fire == None:  # fire가 None일때 속도
            fire_x -= 30
        else:
            fire_x -= 15  # fire가 None이 아닐때 속도 (불덩어리 속도)

        if fire_x <= 0:
            fire_x = pad_width
            fire_y = random.randrange(0, pad_height)
            random.shuffle(fires)
            fire = fires[0]

        # Bullet Position
        if len(bullet_xy) != 0:  # 리스트에 좌표가 있으면 하나씩 추출해서 좌표 갱신 (총알 속도)
            for i, bxy in enumerate(bullet_xy):
                bxy[0] += 15
                bullet_xy[i][0] = bxy[0]
                if bxy[0] >= pad_width:  # 맵 끝까지 가면 삭제
                    bullet_xy.remove(bxy)

        drawobject(aircraft, x, y)
        drawobject(bat, bat_x, bat_y)

        if fire != None:
            drawobject(fire, fire_x, fire_y)

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawobject(bullet, bx, by)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()  # 초기화한 PyGame종료
    quit()


def initgame():  # 게임 초기화 함수
    global gamepad, aircraft, clock, background1, background2  # 전역 변수 선언
    global bat, fires, bullet

    fires = []  # 불덩어리 2개와 객체 5개를 담을 리스트

    pygame.init()  # PyGame 라이브러리 초기화(항상 해야한다)
    gamepad = pygame.display.set_mode((pad_width, pad_height))  # 놀이판 크기를 설정
    pygame.display.set_caption('PyFlying')  # 타이틀 지정
    aircraft = pygame.image.load('/Users/Austin/PycharmProjects/pygame/plane.png')
    background1 = pygame.image.load('/Users/Austin/PycharmProjects/pygame/background.png')  # 배경 이미지 할당
    background2 = background1.copy()
    bat = pygame.image.load('/Users/Austin/PycharmProjects/pygame/bat.png')
    fires.append(pygame.image.load('/Users/Austin/PycharmProjects/pygame/fireball.png'))
    fires.append(pygame.image.load('/Users/Austin/PycharmProjects/pygame/fireball2.png'))

    for i in range(5):
        fires.append(None)

    bullet = pygame.image.load('/Users/Austin/PycharmProjects/pygame/bullet.png')

    clock = pygame.time.Clock()  # 초당 프레임 지정 (FPS)
    rungame()  # 게임 구동


if __name__ == '__main__':
    initgame()
