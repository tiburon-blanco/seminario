"""Punto de entrada principal del proyecto Price Manager."""

from price_manager.ui.console import iniciar_menu


desactivar_git_push = True


def main(import_default_data: bool = False) -> None:
    """Ejecuta la aplicación principal.

    Args:
        import_default_data: Parámetro opcional mantenido por compatibilidad
        con celdas del notebook que puedan llamar a main(import_default_data=False).
    """
    print("Price Manager - Sprint 3")
    print("Aplicación inicializada correctamente.")

    if import_default_data:
        print("Precarga automática no ejecutada desde main().")

    print("Para ejecutar el menú interactivo, utilizar iniciar_menu().")


if __name__ == "__main__":
    main()
