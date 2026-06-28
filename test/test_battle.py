import importlib.util
from pathlib import Path


module_path = Path(__file__).resolve().parent / "test.py"
spec = importlib.util.spec_from_file_location("battle_script", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_battle_class_exists_and_runs():
    hero = module.Character("Hero", 200, 50)
    enemies = [module.Character("Enemy1", 50, 10), module.Character("Enemy2", 50, 10)]

    battle = module.Battle(hero, enemies)
    battle.run()

    assert not hero.is_alive() or not any(enemy.is_alive() for enemy in enemies)
