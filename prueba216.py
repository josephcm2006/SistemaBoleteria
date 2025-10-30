from tkinter import *
from tkinter import messagebox
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import threading





Correos = []
Contrase = []



presentacion = None
registro = None
registro2 = None
iniciosesion = None
paginaprincipal = None


entradacontra2=None
entradacorreo2=None

emailaenviar = None
codigo = None

miemail = "User2442E@gmail.com"
micontra = "skhf cwfc yclf fhzl"

entradacontra1=None
entradacorreo1 = None
botonenviar1 = None
bloquedespues = None
entradacodigo = None





def enviarmeil():
    global codigo, emailaenviar, entradacorreo1, botonenviar1,correounovariable
    
        
    emailaenviar = entradacorreo1.get()

    if not emailaenviar or "@" not in emailaenviar:
        messagebox.showerror("ERROR", "Debe ingresar un email válido")
        correounovariable.set("")
        return

    codigo = str(random.randint(100000, 999999))
    botonenviar1.config(state="disabled")
    threading.Thread(target=enviar_email, daemon=True).start()

def enviar_email():
    global botonenviar1,bloquedespues
    try:
        mensaje = MIMEMultipart()
        mensaje["From"] = miemail
        mensaje["To"] = emailaenviar
        mensaje["Subject"] = "Código de verificación"

        escrito = f"""
        Código de verificación
        
        Este es su código: {codigo}"""
        mensaje.attach(MIMEText(escrito, "plain"))

        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(miemail, micontra)
        servidor.send_message(mensaje)
        servidor.quit()
        
        botonenviar1.config(state="normal")
        bloquedespues.place(relx=0.2, rely=0.7, width=300, height=150)
        messagebox.showinfo("Éxito", "Código enviado correctamente")

    except Exception as e:
        print(f"Error enviando email: {e}")
        botonenviar1.config(state="normal")
        messagebox.showerror("ERROR", "Error enviando el correo")
        
def verificar():
    global entradacodigo, codigo,codigovairable
    if entradacodigo.get() == codigo:
        messagebox.showinfo("Éxito", "Código verificado correctamente")
        haciaregistro2()
    else:
        messagebox.showerror("ERROR", "Código incorrecto")
        codigovairable.set("")



def reinicio():
    global correounovariable,contraunovariable,correodosvariable,contradosvariable
    correounovariable.set("")
    contraunovariable.set("")
    correodosvariable.set("")
    contradosvariable.set("")
    codigovairable.set("")



















def haciaregistro():
    global registro, presentacion, registro2, entradacorreo1, botonenviar1, bloquedespues, entradacodigo,correounovariable

    if presentacion is not None:
        presentacion.withdraw()
    if registro2 is not None:
        registro2.withdraw()
        
    if registro is None:
        registro = Toplevel()  
        registro.title("Registro")
        registro.geometry("500x500+450+100")
        registro.resizable(False, False)
        registro.config(bg="gray10")


        Label(registro,text="Ingrese su Correo:",bg="gray10",fg="white"
            ,font=("Arial",18,"bold")).place(relx=0.3,rely=0.2)

        bloquedecorreo1=Frame(registro,bg="darkorchid4",width=300,height=28)
        bloquedecorreo1.place(relx=0.24,rely=0.30)
        bloquedecorreo1.pack_propagate(False)

        entradacorreo1 = Entry(bloquedecorreo1,textvariable=correounovariable ,bg="gray6", fg="white",
            justify="center",font=("Arial",13,"bold"))
        entradacorreo1.pack(fill=BOTH,expand=True,padx=2,pady=2)
        botonenviar1 = Button(registro, text="Enviar email", command=enviarmeil, fg="white",
            bg="gray20",font=("Arial",9,"bold"),bd=5,relief="raised")
        botonenviar1.place(relx=0.4,rely=0.4)
        
        volver1 = Button(registro, text="Volver", command=confirmar_volver,
            fg="white",bg="gray20",font=("Arial",9,"bold"),bd=5,relief="raised")
        volver1.place(relx=0.45,rely=0.50)

        bloquedespues = Frame(registro, bg="gray10")
        texto = Label(bloquedespues, text="Ingrese su código:",bg="gray10",fg="white",font=("Arial",7,"bold"))
        texto.pack(side="left", padx=5)
        
        entradacodigo = Entry(bloquedespues,textvariable=codigovairable,fg="white",bg="gray20",
            justify="center",font=("Arial",7,"bold"))
        entradacodigo.pack(side="left", padx=5)
        
        botonenviar2 = Button(bloquedespues, text="Verificar", command=verificar,
            fg="white",bg="gray20",bd=5,relief="raised")
        botonenviar2.pack(side="left", padx=5)
        
    registro.deiconify()

def haciaregistro2():
    global registro, registro2, Correos, Contrase, entradacorreo1,entradacontra1,contraunovariable,bloquedespues
    bloquedespues.place_forget()
    if registro is not None:
        registro.withdraw()
        
    if registro2 is None:
        registro2 = Toplevel()
        registro2.title("Completar Registro")
        registro2.geometry("500x500+450+100")
        registro2.config(bg="gray10")

        Label(registro2, text="Complete su registro", font=("Arial", 14,"bold"),bg="gray10",
            fg="white").pack(pady=20)

        Label(registro2,text="Ingrese una contraseña:",font=("Arial",13,"bold"),bg="gray10",
            fg="white").place(relx=0.3,rely=0.3)

        bloqueentradacontra1=Frame(registro2,bg="darkorchid4",width=300,height=28)
        bloqueentradacontra1.place(relx=0.24,rely=0.4)
        bloqueentradacontra1.pack_propagate(False)
        entradacontra1 = Entry(bloqueentradacontra1,textvariable=contraunovariable, show="*",
            bg="gray20",fg="white",justify="center",font=("Arial",9,"bold"))
        entradacontra1.pack(fill=BOTH,expand=True,padx=2,pady=2)

        def guardar_registro():
            correo = entradacorreo1.get()
            contra = entradacontra1.get()
            Correos.append(correo)
            Contrase.append(contra)
            print("Correos:", Correos)
            print("Contraseñas:", Contrase)
            hacialogin()

        botonenviar4 = Button(registro2, text="Terminar registro", command=guardar_registro,
            fg="white",bg="gray20",bd=5,relief="raised")
        botonenviar4.place(relx=0.4,rely=0.6)
    
        regresarhacia1 = Button(registro2, text="Volver", command=confirmar_volver,
            fg="white",bg="gray20",bd=5,relief="raised")
        regresarhacia1.place(relx=0.45,rely=0.7)
        
    registro2.deiconify()

def hacialogin():
    global presentacion, registro2, registro, paginaprincipal, iniciosesion,entradacontra2,entradacorreo2,correodosvariable,contradosvariable
    if registro2 is not None:
        registro2.withdraw()
    if presentacion is not None:
        presentacion.withdraw()
    if registro is not None:
        registro.withdraw()

    if iniciosesion is None:
        iniciosesion = Toplevel()
        iniciosesion.title("Inicio de sesión")
        iniciosesion.geometry("500x500+450+100")
        iniciosesion.resizable(False, False)
        iniciosesion.config(bg="gray10")

        Label(iniciosesion, text="Iniciar Sesión", fg="white", bg="gray10", 
              font=("Arial", 15, "bold")).pack(pady=30)

        Label(iniciosesion, text="Correo:", fg="white", bg="gray10",font=("Arial",13,"bold")).place(relx=0.45, rely=0.25)
        bloquedecorreo2 = Frame(iniciosesion, width=300, height=28,bg="darkorchid4")
        bloquedecorreo2.place(relx=0.24, rely=0.3)
        bloquedecorreo2.pack_propagate(False)

        entradacorreo2 = Entry(bloquedecorreo2,textvariable=correodosvariable,font=("Arial",13,"bold"),
            justify="center",bg="gray6",fg="white")
        entradacorreo2.pack(fill=BOTH, expand=True, padx=2, pady=2)

        Label(iniciosesion, text="Contraseña:", fg="white", bg="gray10",font=("Arial",13,"bold")).place(relx=0.43, rely=0.37)
        bloquecontra2 = Frame(iniciosesion, width=300, height=28,bg="darkorchid4")
        bloquecontra2.place(relx=0.24, rely=0.44)
        bloquecontra2.pack_propagate(False)

        entradacontra2 = Entry(bloquecontra2,textvariable=contradosvariable, show="*",font=("Arial",13,"bold")
            ,justify="center",fg="white",bg="gray6")
        entradacontra2.pack(fill=BOTH, expand=True, padx=2, pady=2)

        bloquedebtones1 = Frame(iniciosesion, bg="gray10",width=200,height=23)
        bloquedebtones1.place(relx=0.44, rely=0.6)
        bloquedebtones1.pack_propagate(False)
        
        haciapagina = Button(bloquedebtones1, text="Iniciar sesion", command=haciaprincipal,
            bd=5,relief="raised",bg="gray20",fg="white")
        haciapagina.pack(side="left", padx=5)
        
        voler3 = Button(bloquedebtones1, text="Volver", command=confirmar_volver,
            bd=5,relief="raised",bg="gray20",fg="white")
        voler3.pack(side="right", padx=5)
    else:        
        iniciosesion.deiconify()

def haciaprincipal():
    global paginaprincipal, iniciosesion, Correos, Contrase,entradacorreo2,entradacontra2,correodosvariable,contradosvariable
    correo_ingresado = entradacorreo2.get()  
    contra_ingresada = entradacontra2.get()  
    
    aceptado = False
    
    for i in range(len(Correos)):
        if Correos[i] == correo_ingresado and Contrase[i] == contra_ingresada:
            aceptado = True
            break
    
    if aceptado:
        if iniciosesion is not None:
            iniciosesion.withdraw()
        
        if paginaprincipal is None:
            paginaprincipal = Toplevel()
            paginaprincipal.title("Boleteria")
            paginaprincipal.geometry("500x500+450+100")
            paginaprincipal.resizable(False, False)
            paginaprincipal.config(bg="gray10")

            Label(paginaprincipal, text="BIENVENIDOS", fg="white", bg="gray20", 
                  font=("Arial", 15, "bold")).pack(pady=20)

            messagebox.showinfo("Accedido", "Su inicio de sesión fue exitoso")
            
            cerrarsesion = Button(paginaprincipal, text="Cerrar sesión", command=confirmar_volver,
                fg="white",bg="gray20",bd=5,relief="raised")
            cerrarsesion.pack(pady=30)
        else:
            paginaprincipal.deiconify()
            messagebox.showinfo("Accedido", "Su inicio de sesión fue exitoso")
    else:

        messagebox.showerror("ERROR", "Credenciales incorrectas")
        correodosvariable.set("")
        contradosvariable.set("")










def confirmar_volver():
    global presentacion,registro,registro2,iniciosesion,paginaprincipal
    
    if paginaprincipal is not None:
        paginaprincipal.withdraw()
    if registro is not None:
        registro.withdraw()
    if registro2 is not None:
        registro2.withdraw()
    if iniciosesion is not None:
        iniciosesion.withdraw()
    
    if presentacion is not None:
        presentacion.deiconify()
        reinicio()

def nad():
    return









presentacion = Tk()



correounovariable=StringVar(value="")
contraunovariable=StringVar(value="")
correodosvariable=StringVar(value="")
contradosvariable=StringVar(value="")
codigovairable=StringVar(value="")





presentacion.geometry("500x500+450+100")
presentacion.resizable(False, False)
presentacion.title("BoleteriaOficial")
presentacion.config(bg="gray10")

titulo = Label(presentacion, text="""
    Bienvenidos!
    Esperemos nuestra boletería
    pueda ofrecerles un buen servicio""", 
    font=("Arial", 18, "bold"), justify="center", fg="white", bg="gray10")
titulo.place(relx=0.07, rely=0.10)

botonaregistro = Button(presentacion, text="Registrarse",fg="ghost white" ,font=("Arial",9,"bold"),
    command=haciaregistro,bd=5,relief="raised",bg="gray20")
botonaregistro.place(relx=0.3, rely=0.4)

botonalogin = Button(presentacion, text="Iniciar sesion",fg="ghost white",font=("Arial",9,"bold"),
 command=hacialogin,bd=5,relief="raised",bg="gray20")
botonalogin.place(relx=0.55, rely=0.4)

presentacion.mainloop()