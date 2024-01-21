import pet
import asyncio
import pynput
import queue

class PetManager:
    def __init__(self):
        self.pet = pet.Pet()
        self.queue = queue.Queue()
        listener = pynput.keyboard.Listener(on_press=self.on_press)
        listener.start()

    def on_press(self, key):
        self.queue.put(key)

    async def update(self):
        while not self.queue.empty():
            key = self.queue.get()
            if key == pynput.keyboard.Key.space:
                if self.pet.current_animation == self.pet.idle_animation:
                    self.pet.play_animation(self.pet.run_animation)
                    self.pet.window.after(0, self.pet.say, "According to all known laws of aviation, there is no way a bee should be able to fly")
                else:
                    self.pet.play_animation(self.pet.idle_animation)
                    self.pet.window.after(0, self.pet.say, "Bye!")

            # right arrow
            elif key == pynput.keyboard.Key.right:
                self.pet.set_velocity([10, self.pet.velocity[1]])
            # left arrow
            elif key == pynput.keyboard.Key.left:
                self.pet.set_velocity([-10, self.pet.velocity[1]])
            # up arrow
            elif key == pynput.keyboard.Key.up:
                self.pet.set_velocity([self.pet.velocity[0], -40])
        
        self.pet.update()
        await asyncio.sleep(0.001)

async def main():
    pet_manager = PetManager()
    while True:
        await pet_manager.update()

asyncio.run(main())



