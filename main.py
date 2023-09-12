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
import hydra
from omegaconf import DictConfig, OmegaConf


app = typer.Typer()


@app.command()
def create():
    print("Creating user: Hiro Hamada")


@app.command()
def delete():
    print("Deleting user: Hiro Hamada")


if __name__ == "__main__":
    app()