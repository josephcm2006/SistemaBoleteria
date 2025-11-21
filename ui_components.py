"""
Componentes de interfaz reutilizables
"""
import tkinter as tk
from tkinter import Frame, Entry, Button, Label, BOTH
from config import *


def crear_frame_entrada(parent, textvariable, show=None):
    """Crea un frame con entrada estilizada"""
    frame = Frame(parent, bg=COLOR_FRAME_BORDER, width=300, height=28)
    frame.pack_propagate(False)
    
    entry = Entry(
        frame,
        textvariable=textvariable,
        bg=COLOR_ENTRY_BG,
        fg=COLOR_FG_TEXTO,
        justify="center",
        font=FUENTE_ENTRY,
        show=show
    )
    entry.pack(fill=BOTH, expand=True, padx=2, pady=2)
    
    return frame, entry


def crear_boton_estandar(parent, texto, comando):
    """Crea un botón con estilo estándar"""
    return Button(
        parent,
        text=texto,
        command=comando,
        fg=COLOR_FG_TEXTO,
        bg=COLOR_BG_SECUNDARIO,
        font=("Arial", 9, "bold"),
        bd=5,
        relief="raised"
    )


def crear_label_titulo(parent, texto, font=FUENTE_LABEL):
    """Crea una etiqueta de título"""
    return Label(
        parent,
        text=texto,
        bg=COLOR_BG_PRINCIPAL,
        fg=COLOR_FG_TEXTO,
        font=font
    )


def crear_texto_clickeable(canvas, x, y, texto, comando, font=FUENTE_BOTON):
    """Crea un texto clickeable en el canvas con efecto hover"""
    texto_id = canvas.create_text(
        x, y,
        text=texto,
        fill=COLOR_FG_TEXTO,
        font=font,
        justify="center"
    )
    
    # Hacer clickeable
    canvas.tag_bind(texto_id, "<Button-1>", lambda e: comando())
    
    # Efecto hover
    canvas.tag_bind(
        texto_id,
        "<Enter>",
        lambda e: [
            canvas.itemconfig(texto_id, fill=COLOR_HOVER),
            canvas.config(cursor="hand2")
        ]
    )
    
    canvas.tag_bind(
        texto_id,
        "<Leave>",
        lambda e: [
            canvas.itemconfig(texto_id, fill=COLOR_FG_TEXTO),
            canvas.config(cursor="")
        ]
    )
    
    return texto_id


def configurar_ventana_base(ventana, titulo, geometria=GEOMETRIA_SECUNDARIA):
    """Configura una ventana con estilos base"""
    ventana.iconbitmap(ICONO_PRINCIPAL)
    ventana.title(titulo)
    ventana.geometry(geometria)
    ventana.resizable(False, False)
    ventana.config(bg=COLOR_BG_PRINCIPAL)