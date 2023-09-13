# import typer
# from typing import Optional

# app = typer.Typer()

# # @app.command()
# # def hello(name: str):
# #     print(f"Hello {name}!")

# # def goodbye(name: str, formal: bool = False):
# #     if formal:
# #         print(f"Goodbye {name}. Have a goog day!")
# #     else:
# #         print(f'Bye {name}!')


# # if __name__ == '__main__':
# #     app()
# # def type_example(name: str, formal: bool = False, intro: Optional[str] = None):
# #     pass
# @app.command()
# def main(name: str, lastname: str = "", formal: bool = False):
#     """
#     Say hi to NAME, optionally with a --lastname.

#     If --formal is used, say hi very formally.
#     """
#     if formal:
#         print(f"Good day Ms. {name} {lastname}.")
#     else:
#         print(f"Hello {name} {lastname}")


# if __name__ == '__main__':
#     typer.run(main)
import typer
# import hydra
# from omegaconf import DictConfig, OmegaConf
from config import settings
from prober import scan
import asyncio


app = typer.Typer()
loop = None
def test_dynaconf() -> None:
    print(settings.db.host)
    print(settings.app.name)
    print(settings.password)


@app.command()
def create():
    print("Creating user: Hiro Hamada")
    test_dynaconf()


@app.command('scan')
def scan_web():
    subnet = settings.scan.network
    nums = settings.scan.nums
    asyncio.run(scan.scan_network(nums, subnet))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app()
