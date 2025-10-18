#!/usr/bin/env python
"""Point d’entrée des commandes Django."""

import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jo_tickets.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Impossible d'importer Django. Assurez-vous qu'il est installé et "
            "accessible dans votre environnement."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()


