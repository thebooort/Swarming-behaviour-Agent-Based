
import sys, pygame, random, math

pygame.init()

size = width, height = 1200, 800
black = 0, 1, 10

maxVel = 8
maxVel2 = 0.5
numBoids = 100
boids = []

class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velX = random.randint(1, 10) / 10.0
        self.velY = random.randint(1, 10) / 10.0

    "funcion distancia"
    def distance(self, boid):
        distX = self.x - boid.x
        distY = self.y - boid.y        
        return math.sqrt(distX * distX + distY * distY)

    def distance2(self):
        distX = self.x - 0
        distY = self.y - 0        
        return math.sqrt(distX * distX + distY * distY)

    "moverse al punto medio"
    def moveCloser(self, boids):
        if len(boids) < 1: return
            
        #distancia media
        avgX = 0
        avgY = 0
        for boid in boids:
            if boid.x == self.x and boid.y == self.y:
                continue
                
            avgX += (self.x - boid.x)
            avgY += (self.y - boid.y)

        avgX /= len(boids)
        avgY /= len(boids)

        #velocidad segun el resto
        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0
       
        self.velX -= (avgX / 100) 
        self.velY -= (avgY / 100) 
        
    "bandada"
    def moveWith(self, boids):
        if len(boids) < 1: return
        
        avgX = 0
        avgY = 0
                
        for boid in boids:
            avgX += boid.velX
            avgY += boid.velY

        avgX /= len(boids)
        avgY /= len(boids)

        
        self.velX += (avgX / 40)
        self.velY += (avgY / 40)
    

    def moveAway(self, boids, minDistance):
        if len(boids) < 1: return
        
        distanceX = 0
        distanceY = 0
        numClose = 0

        for boid in boids:
            distance = self.distance(boid)
            if  distance < minDistance:
                numClose += 1
                xdiff = (self.x - boid.x) 
                ydiff = (self.y - boid.y) 
                
                if xdiff >= 0: xdiff = math.sqrt(minDistance) - xdiff
                elif xdiff < 0: xdiff = -math.sqrt(minDistance) - xdiff
                
                if ydiff >= 0: ydiff = math.sqrt(minDistance) - ydiff
                elif ydiff < 0: ydiff = -math.sqrt(minDistance) - ydiff

                distanceX += xdiff 
                distanceY += ydiff 
        
        if numClose == 0:
            return
            
        self.velX -= distanceX / 5
        self.velY -= distanceY / 5

    def moveAwayPre(self,boids,predator,minDistance):
        
        distanceX = 0
        distanceY = 0
        for boid in boids:
	    distX = self.x - predator.x
            distY = self.y - predator.y       
            distance = math.sqrt(distX * distX + distY * distY)
            if  distance < minDistance:
                xdiff = (self.x - predator.x) 
                ydiff = (self.y - predator.y) 
                
                if xdiff >= 0: xdiff = math.sqrt(minDistance) - xdiff
                elif xdiff < 0: xdiff = -math.sqrt(minDistance) - xdiff
                
                if ydiff >= 0: ydiff = math.sqrt(minDistance) - ydiff
                elif ydiff < 0: ydiff = -math.sqrt(minDistance) - ydiff

                distanceX += xdiff 
                distanceY += ydiff 
        
            
        self.velX -= distanceX / 2
        self.velY -= distanceY / 2
        
    
    def move(self):
        if abs(self.velX) > maxVel or abs(self.velY) > maxVel:
            scaleFactor = maxVel / max(abs(self.velX), abs(self.velY))
            self.velX *= scaleFactor
            self.velY *= scaleFactor
        
        self.x += self.velX
        self.y += self.velY
"mata pollos"
class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velX = random.randint(1, 10) / 10.0
        self.velY = random.randint(1, 10) / 10.0
    
    def moveCloser2(self, boids):
        
            
        #distancia media
        avgX = 0
        avgY = 0
        for boid in boids:
            if boid.x == self.x and boid.y == self.y:
                continue
                
            avgX += (self.x - boid.x)
            avgY += (self.y - boid.y)

        avgX /= len(boids)
        avgY /= len(boids)
        #velocidad segun el resto
        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0
       
        self.velX -= (avgX / 250) 
        self.velY -= (avgY / 250) 
    def move2(self):
        if abs(self.velX) > maxVel2 or abs(self.velY) > maxVel2:
            scaleFactor = maxVel2 / max(abs(self.velX), abs(self.velY))
            self.velX *= scaleFactor
            self.velY *= scaleFactor
        
        self.x += self.velX
        self.y += self.velY
screen = pygame.display.set_mode(size)

ball = pygame.image.load("twitter1.png")
ballrect = ball.get_rect()
ball2 = pygame.image.load("offline.png")
ball2rect = ball2.get_rect()


for i in range(numBoids):
    boids.append(Boid(random.randint(0, width), random.randint(0, height))) 

predator=Predator(random.randint(0, width), random.randint(0, height))	
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for boid in boids:
        closeBoids = []
        for otherBoid in boids:
            if otherBoid == boid: continue
            distance = boid.distance(otherBoid)
            if distance < 200:
                closeBoids.append(otherBoid)

        
        boid.moveCloser(closeBoids)
        boid.moveWith(closeBoids)  
        boid.moveAway(closeBoids, 17)  
	boid.moveAwayPre(closeBoids,predator,90)        
	
        border = 25
        if boid.x < border and boid.velX < 0:
            boid.velX = -boid.velX * random.random()
        if boid.x > width - border and boid.velX > 0:
            boid.velX = -boid.velX * random.random()
        if boid.y < border and boid.velY < 0:
            boid.velY = -boid.velY * random.random()
        if boid.y > height - border and boid.velY > 0:
            boid.velY = -boid.velY * random.random()
        boids2=[boids[1],boids[2],boids[3],boids[4],boids[5],boids[10],boids[20],boids[11]]        
	predator.moveCloser2(boids2)    
        boid.move()
        predator.move2()

    screen.fill(black)
      
    for boid in boids:
        boidRect = pygame.Rect(ballrect)
        boidRect.x = boid.x
        boidRect.y = boid.y
        screen.blit(ball, boidRect)
    preRect = pygame.Rect(ball2rect)
    preRect.x = predator.x
    preRect.y = predator.y
    screen.blit(ball2, preRect)
    pygame.display.flip()
    pygame.time.delay(10)
