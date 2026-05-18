"""Punto de entrada principal del proyecto Price Manager."""

from price_manager.ui.console import ConsolaPriceManager

desactivar_git_push = True


def main() -> None:
  """Ejecuta la aplicación principal."""
  app = ConsolaPriceManager()
  app.ejecutar()


if __name__ == "__main__":
  main()
