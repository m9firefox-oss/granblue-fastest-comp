import random


class Character:
    def __init__(self, name, hp, atk, crit_rate=0.15, dodge_rate=0.2, crit_bonus=20):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.crit_rate = crit_rate
        self.dodge_rate = dodge_rate
        self.crit_bonus = crit_bonus

    def attack(self, target):
        if random.random() < self.crit_rate:
            damage = self.atk + random.randint(self.crit_bonus - 10, self.crit_bonus)
            print(f"{self.name} lands a critical hit on {target.name} for {damage} damage!")
        else:
            damage = self.atk + random.randint(0, 10)
            print(f"{self.name} attacks {target.name} for {damage} damage!")

        target.take_damage(damage)

    def take_damage(self, damage):
        if random.random() < self.dodge_rate:
            print(f"{self.name} dodged the attack!")
            return

        self.hp -= damage
        print(f"{self.name} takes {damage} damage!")
        if self.hp <= 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def status(self):
        print(f"{self.name} has {self.hp} HP.")


class Battle:
    def __init__(self, hero, enemies):
        self.hero = hero
        self.enemies = enemies
        self.turn = 1

    def run(self):
        while self.hero.is_alive() and any(enemy.is_alive() for enemy in self.enemies):
            print(f"\n--- Turn {self.turn} ---")

            self.hero_turn()
            self.enemy_turn()
            self.show_status()

            self.turn += 1

        print("\nBattle Finished!")

    def hero_turn(self):
        if not self.hero.is_alive():
            return

        target = self.get_next_target()
        if target is not None:
            self.hero.attack(target)

    def enemy_turn(self):
        for enemy in self.enemies:
            if enemy.is_alive() and self.hero.is_alive():
                enemy.attack(self.hero)

    def get_next_target(self):
        alive_enemies = [enemy for enemy in self.enemies if enemy.is_alive()]
        if not alive_enemies:
            return None
        return random.choice(alive_enemies)

    def show_status(self):
        print("\nStatus:")
        characters = [self.hero, *self.enemies]
        for character in characters:
            character.status()


if __name__ == "__main__":
    hero = Character("Hero", 220, 55, crit_rate=0.2, dodge_rate=0.2, crit_bonus=20)
    enemies = [
        Character("Enemy1", 130, 22, crit_rate=0.08, dodge_rate=0.12, crit_bonus=15),
        Character("Enemy2", 130, 22, crit_rate=0.08, dodge_rate=0.12, crit_bonus=15),
    ]
    battle = Battle(hero, enemies)
    battle.run()


