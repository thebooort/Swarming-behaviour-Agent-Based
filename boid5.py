
# Based pn the original code made by Ben Dowling - www.coderholic.com

import sys, pygame, random, math

pygame.init()

size = width, height = 1200, 800
black = 0, 1, 10

maxVelocity = 5
numBoids = 80
boids = []

class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0

    "Return the distance from another boid"
    def distance(self, boid):
        distX = self.x - boid.x
        distY = self.y - boid.y        
        return math.sqrt(distX * distX + distY * distY)

    "Move closer to a set of boids"
    def moveCloser(self, boids):
        if len(boids) < 1: return
            
        # calculate the average distances from the other boids
        avgX = 0
        avgY = 0
        b=0.1
        
        for boid in boids:
            boid1x=self.x
            boid1y=self.y
            dist=math.sqrt((boid1x - boid.x)**2 + (boid1y - boid.y)**2)
	    if dist<10:
                if boid.x == self.x and boid.y == self.y:
                    continue
                
            avgX += (self.x - boid.x)
            avgY += (self.y - boid.y)
            b=b+1

        avgX /= b
        avgY /= b

        # set our velocity towards the others
        distance = math.sqrt((avgX * avgX) + (avgY * avgY)) * -1.0
       
        self.velocityX -= (avgX / 100) 
        self.velocityY -= (avgY / 100) 
        
    "Move with a set of boids"
    def moveWith(self, boids):
        if len(boids) < 1: return
        # calculate the average velocities of the other boids
        avgX = 0
        avgY = 0
        b=0.1        
        for boid in boids:
            boid1x=self.x
            boid1y=self.y
            dist=math.sqrt((boid1x - boid.x)**2 + (boid1y - boid.y)**2)
            if dist<20:
                avgX += boid.velocityX
                avgY += boid.velocityY
                b=b+1

        avgX /= b
        avgY /= b

        # set our velocity towards the others
        self.velocityX += (avgX / 40)
        self.velocityY += (avgY / 40)
    
    "Move away from a set of boids. This avoids crowding"
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
            
        self.velocityX -= distanceX / 5
        self.velocityY -= distanceY / 5
        
    "Perform actual movement based on our velocity"
    def move(self):
        if abs(self.velocityX) > maxVelocity or abs(self.velocityY) > maxVelocity:
            scaleFactor = maxVelocity / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor
        
        self.x += self.velocityX
        self.y += self.velocityY

screen = pygame.display.set_mode(size)

ball = pygame.image.load("twitter1.png")
ballrect = ball.get_rect()

# create boids at random positions
for i in range(numBoids):
    boids.append(Boid(random.randint(0, width), random.randint(0, height)))   

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
        boid.moveAway(closeBoids, 20)  

        # ensure they stay within the screen space
        # if we roubound we can lose some of our velocity
        border = 25
        if boid.x < border and boid.velocityX < 0:
            boid.velocityX = -boid.velocityX * random.random()
        if boid.x > width - border and boid.velocityX > 0:
            boid.velocityX = -boid.velocityX * random.random()
        if boid.y < border and boid.velocityY < 0:
            boid.velocityY = -boid.velocityY * random.random()
        if boid.y > height - border and boid.velocityY > 0:
            boid.velocityY = -boid.velocityY * random.random()
            
        boid.move()

       
    screen.fill(black)
    for i in range(numBoids):
        boid1=boids[i]
        for j in range(numBoids):
            boid2=boids[j]
            dist=math.sqrt((boid1.x - boid2.x)**2 + (boid1.y - boid2.y)**2)
            if dist<50.0:
                pygame.draw.line(screen, 0xff0000, (boid1.x, boid1.y), (boid2.x, boid2.y), 1)     
    for boid in boids:
        boidRect = pygame.Rect(ballrect)
        boidRect.x = boid.x
        boidRect.y = boid.y
        screen.blit(ball, boidRect)
    num=numBoids-1

    pygame.display.flip()
    pygame.time.delay(10)
