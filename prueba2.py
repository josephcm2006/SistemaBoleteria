from tkinter import *
import random
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import threading


codigo=None
Enviaremaila=None

correomio="User2442E@gmail.com"
contramia="skhf cwfc yclf fhzl"
#skhf cwfc yclf fhzl
def enviarcodigo():
	global Enviaremaila,codigo
	Enviaremaila=entradadeemail.get()

	if not Enviaremaila or "@" not in Enviaremaila:
		messagebox.showerror("ERROR","Email no es validoo!!!")
		return

	codigo=str(random.randint(100000,999999))
	EnviandoElcodigo.config(text="Enviando el codigo.....")
	botonenviar.config(state="disabled")
	threading.Thread(target=enviandoemail,daemon=True).start()


def enviandoemail():
	try:
		mensaje=MIMEMultipart()
		mensaje["From"]=correomio
		mensaje["to"]=Enviaremaila
		mensaje["Subject"]="Mire su codigo e verificacion"

		escrito=f"""
		Codigo de verificacion............

		Tu codigo es {codigo}

		Ingresa este codigo en la opcion de ingresar: PLEASEEEE"""

		mensaje.attach(MIMEText(escrito,"plain"))

		Dedonde=smtplib.SMTP("smtp.gmail.com",587)
		Dedonde.starttls()
		Dedonde.login(correomio,contramia)
		Dedonde.send_message(mensaje)
		Dedonde.quit()
		pagina.after(0,fueexitoso)
	except Exception as e:
		pagina.after(0,erroralenviar)


def fueexitoso():
	EnviandoElcodigo.config(text=f"codigo enviado exitosamente a: {Enviaremaila}")
	botonenviar.config(state="normal")
	Bloquedeverificacion.place(relx=0.2,rely=0.7,width=300,height=150)

def erroralenviar():
	EnviandoElcodigo.config(text="Error al enviarse")
	botonenviar.config(state="normal")



def verificado():
	if entradadelcodigo.get()==codigo:
		messagebox.showinfo("Exito","Codigo correcto!!!")
		continuar()
	else:
		messagebox.showerror("ERRROR","Codigo incorrecto")

def continuar():
	pagina.destroy()
	segundopag=Tk()
	segundopag.geometry("500x500+450+100")
	segundopag.resizable(False,False)

	segundopag.mainloop()
















pagina=Tk()
pagina.geometry("500x500+450+100")
pagina.title("Validacion")
pagina.resizable(False,False)
pagina.config(bg="gray20")

presentacion=Label(pagina,text="Verificacion de email",font=("Arial",18,"bold"),bg="gray20",fg="white")
presentacion.pack(pady=20)


bloqueEmail=Frame(pagina,bg="black",width=250,height=30)
bloqueEmail.place(relx=0.25,rely=0.3)
bloqueEmail.pack_propagate(False)

entradadeemail=Entry(bloqueEmail,font=("Arial",13,"bold"))
entradadeemail.pack(fill=BOTH,expand=True,padx=2,pady=2)

entradadeemail.bind("<Return>", lambda event: enviarcodigo())

botonenviar=Button(pagina,text="Enviar",width=7,height=1,command=enviarcodigo)
botonenviar.place(relx=0.80,rely=0.3)


Bloquedeverificacion=Frame(pagina,bg="gray20")
Bloquedeverificacion.pack_propagate(False)
etiqueta=Label(Bloquedeverificacion,text="Ingrese el codigo recibido",bg="gray20",font=("Arial",14,"bold"))
etiqueta.pack(pady=5)
entradadelcodigo=Entry(Bloquedeverificacion,width=20)
entradadelcodigo.pack(pady=10)
botondos=Button(Bloquedeverificacion,text="Verificar",command=verificado)
botondos.pack(pady=10)


EnviandoElcodigo=Label(pagina,text="",fg="white",bg="gray20",font=("Arial",12,"bold"))
EnviandoElcodigo.pack(pady=180)








pagina.mainloop()


