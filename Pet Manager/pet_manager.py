import pet
import asyncio
import numpy as np

class PetManager:
    def __init__(self):
        self.pet = pet.Pet()
        self.i = 0

    async def update(self):
        if self.i % 100 == 0:
            self.roam()
        elif self.i % 302 == 0:
            self.pet.idle()
            self.compliment()
        print(self.i)
        self.pet.update()
        await asyncio.sleep(0.001)
        self.i = self.i + 1

    def roam(self):
        # makes the pet randomly roam/idle across the screen

        # randomly choose whether to roam or idle
        if not self.pet.isDragged and not self.pet.isTalking:
            roam = np.random.choice([True, False])

            if roam:
                # randomly choose a direction
                direction = np.random.choice([-1, 1])

                # randomly choose a speed
                speed = np.random.randint(1, 5)

                # set the pet's velocity
                self.pet.set_velocity([direction * speed, self.pet.velocity[1]])

                # set the pet's acceleration
                self.pet.set_acceleration([0, self.pet.acceleration[1]])
            else:
                self.pet.idle()

    def compliment(self):
        # makes the pet compliment the user
        if not self.pet.isDragged:
            self.pet.say(np.random.choice(["You're awesome!", "You're the best!", "You're looking great today!", "a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a"]))

async def main():
    pet_manager = PetManager()
    while True:
        await pet_manager.update()

asyncio.run(main())



